import * as vscode from 'vscode';
import { MongoClient, Db } from 'mongodb';

let client: MongoClient | null = null;
let db: Db | null = null;
let outputChannel: vscode.OutputChannel;

export function activate(context: vscode.ExtensionContext) {
    outputChannel = vscode.window.createOutputChannel('MongoDB Expert');

    // Register commands
    const runQueryCommand = vscode.commands.registerCommand('mongodb.runQuery', runQuery);
    const connectCommand = vscode.commands.registerCommand('mongodb.connect', connectToMongoDB);
    const showCollectionsCommand = vscode.commands.registerCommand('mongodb.showCollections', showCollections);
    const explainQueryCommand = vscode.commands.registerCommand('mongodb.explainQuery', explainQuery);

    context.subscriptions.push(runQueryCommand, connectCommand, showCollectionsCommand, explainQueryCommand);

    // Register document formatting provider
    vscode.languages.registerDocumentFormattingEditProvider('mongodb', {
        provideDocumentFormattingEdits(document) {
            const edits: vscode.TextEdit[] = [];
            const text = document.getText();
            try {
                const formatted = JSON.stringify(JSON.parse(text), null, 2);
                const range = new vscode.Range(
                    document.positionAt(0),
                    document.positionAt(text.length)
                );
                edits.push(vscode.TextEdit.replace(range, formatted));
            } catch (e) {
                // Invalid JSON, skip formatting
            }
            return edits;
        }
    });

    outputChannel.appendLine('MongoDB Expert extension activated');
}

async function connectToMongoDB() {
    const config = vscode.workspace.getConfiguration('mongodb');
    const uri = config.get<string>('connectionUri', 'mongodb://localhost:27017');
    const database = config.get<string>('defaultDatabase', 'test');

    try {
        client = new MongoClient(uri);
        await client.connect();
        db = client.db(database);

        // Test connection
        await db.admin().command({ ping: 1 });

        vscode.window.showInformationMessage(`Connected to MongoDB: ${database}`);
        outputChannel.appendLine(`Connected to ${uri}/${database}`);

        // Refresh collections tree view
        vscode.commands.executeCommand('mongodb.collections.refresh');
    } catch (error: any) {
        vscode.window.showErrorMessage(`Failed to connect: ${error.message}`);
        outputChannel.appendLine(`Connection error: ${error.message}`);
    }
}

async function runQuery() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showWarningMessage('No active editor');
        return;
    }

    const selection = editor.selection;
    const queryText = editor.document.getText(selection.isEmpty ? undefined : selection);

    if (!queryText.trim()) {
        vscode.window.showWarningMessage('No query to run');
        return;
    }

    if (!db) {
        const connect = await vscode.window.showWarningMessage(
            'Not connected to MongoDB',
            'Connect'
        );
        if (connect === 'Connect') {
            await connectToMongoDB();
        }
        if (!db) {
            return;
        }
    }

    try {
        outputChannel.show(true);
        outputChannel.appendLine('Running query...');

        const parsed = parseMongoQuery(queryText);
        const results = await executeQuery(parsed);

        // Display results
        outputChannel.appendLine('\nResults:');
        outputChannel.appendLine(JSON.stringify(results, null, 2));
        outputChannel.appendLine(`\nReturned ${results.length || results.result?.length || 0} document(s)`);

        // Show in webview for better formatting
        showResultsPanel(results);
    } catch (error: any) {
        vscode.window.showErrorMessage(`Query error: ${error.message}`);
        outputChannel.appendLine(`Error: ${error.message}`);
    }
}

async function explainQuery() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        return;
    }

    const queryText = editor.document.getText(editor.selection);

    if (!db) {
        vscode.window.showWarningMessage('Not connected to MongoDB');
        return;
    }

    try {
        const parsed = parseMongoQuery(queryText);
        const collection = db.collection(parsed.collection);

        const explainResult = await collection.find(parsed.query || {})
            .project(parsed.projection || {})
            .explain('executionStats');

        showResultsPanel(explainResult, true);
    } catch (error: any) {
        vscode.window.showErrorMessage(`Explain error: ${error.message}`);
    }
}

async function showCollections() {
    if (!db) {
        await connectToMongoDB();
        if (!db) {
            return;
        }
    }

    try {
        const collections = await db.listCollections().toArray();
        const collectionNames = collections.map(c => c.name);

        const selected = await vscode.window.showQuickPick(collectionNames, {
            placeHolder: 'Select a collection'
        });

        if (selected) {
            showCollectionStats(selected);
        }
    } catch (error: any) {
        vscode.window.showErrorMessage(`Error: ${error.message}`);
    }
}

async function showCollectionStats(collectionName: string) {
    if (!db) return;

    try {
        const stats = await db.collection(collectionName).stats();
        const indexes = await db.collection(collectionName).indexes();

        const message = `
Collection: ${collectionName}
Documents: ${stats.count || 0}
Size: ${(stats.size / 1024).toFixed(2)} KB
Avg Doc Size: ${(stats.avgObjSize || 0).toFixed(2)} bytes
Indexes: ${stats.nindexes || 0}
Index Size: ${(stats.totalIndexSize / 1024).toFixed(2)} KB

Indexes: ${indexes.map(i => i.name).join(', ')}
        `.trim();

        vscode.window.showInformationMessage(message, 'OK');
    } catch (error: any) {
        vscode.window.showErrorMessage(`Error: ${error.message}`);
    }
}

function parseMongoQuery(query: string): any {
    // Simple parser for common MongoDB query patterns
    // Supports: db.collection.find({ query }, { projection })
    // and: db.collection.aggregate([...])

    const findMatch = query.match(/db\.(\w+)\.find\(([^)]+)\)/);
    if (findMatch) {
        const collection = findMatch[1];
        const args = findMatch[2].split(',').map(s => s.trim());
        const queryObj = args[0] ? JSON.parse(args[0]) : {};
        const projection = args[1] ? JSON.parse(args[1]) : {};

        return { type: 'find', collection, query: queryObj, projection };
    }

    const aggMatch = query.match(/db\.(\w+)\.aggregate\((\[.*\])\)/);
    if (aggMatch) {
        const collection = aggMatch[1];
        const pipeline = JSON.parse(aggMatch[2]);
        return { type: 'aggregate', collection, pipeline };
    }

    throw new Error('Could not parse MongoDB query');
}

async function executeQuery(parsed: any): Promise<any> {
    if (!db) {
        throw new Error('Not connected to database');
    }

    const collection = db.collection(parsed.collection);
    const config = vscode.workspace.getConfiguration('mongodb');
    const maxResults = config.get<number>('maxResults', 100);

    if (parsed.type === 'find') {
        const cursor = collection
            .find(parsed.query || {})
            .project(parsed.projection || {})
            .limit(maxResults);
        return cursor.toArray();
    } else if (parsed.type === 'aggregate') {
        const cursor = collection.aggregate(parsed.pipeline).limit(maxResults);
        return cursor.toArray();
    }

    throw new Error('Unknown query type');
}

function showResultsPanel(results: any, isExplain: boolean = false) {
    const panel = vscode.window.createWebviewPanel(
        'mongodb.results',
        isExplain ? 'Query Explain' : 'Query Results',
        vscode.ViewColumn.Two,
        { enableScripts: true }
    );

    panel.webview.html = getResultsHtml(results, isExplain);
}

function getResultsHtml(results: any, isExplain: boolean): string {
    const json = JSON.stringify(results, null, 2);
    const title = isExplain ? 'Query Execution Plan' : 'Query Results';

    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title}</title>
    <style>
        body { font-family: var(--vscode-font-family); padding: 10px; color: var(--vscode-foreground); background: var(--vscode-editor-background); }
        pre { background: var(--vscode-textCodeBlock-background); padding: 10px; border-radius: 4px; overflow-x: auto; }
        .count { margin-bottom: 10px; color: var(--vscode-textLink-foreground); }
    </style>
</head>
<body>
    <h2>${title}</h2>
    <div class="count">${Array.isArray(results) ? results.length + ' documents' : 'Result'}</div>
    <pre>${json}</pre>
</body>
</html>`;
}

export function deactivate() {
    if (client) {
        client.close();
    }
    if (outputChannel) {
        outputChannel.dispose();
    }
}

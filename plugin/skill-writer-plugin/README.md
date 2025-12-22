# Skill Writer Plugin

A Claude Code plugin that helps you create well-structured Agent Skills following best practices and validation requirements.

## Features

- **Skill Writer Skill**: Comprehensive guidance for creating Agent Skills
- **Create Skill Command**: Quick command to scaffold new skills with proper structure

## Installation

1. Clone or download this plugin
2. Enable it in Claude Code:
   ```bash
   cc --plugin-dir /path/to/skill-writer-plugin
   ```

## Usage

### Using the Skill

When you want to create a new Agent Skill, simply ask:
- "Help me create a skill for..."
- "I want to write a new skill for..."
- "Can you guide me through creating a skill for..."

### Using the Command

Create a new skill quickly:
```
/create-skill my-skill-name
```

This will:
- Create the skill directory structure
- Generate a template SKILL.md file
- Provide guidance on customization

## Plugin Structure

```
skill-writer-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── commands/
│   └── create-skill.md      # Create skill command
├── skills/
│   └── skill-writer/        # Skill Writer skill
│       └── SKILL.md
└── README.md
```

## Contributing

Feel free to submit issues and enhancement requests!
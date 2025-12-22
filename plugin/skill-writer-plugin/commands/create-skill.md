---
name: create-skill
description: Create a new Agent Skill with proper directory structure and template files
argument-hint: <skill-name>
allowed-tools: Write, Bash
---

# Create Skill Command

Creates a new Agent Skill with the proper directory structure and a template SKILL.md file.

## Usage

```
/create-skill <skill-name>
```

- `<skill-name>`: The name for your skill (kebab-case, e.g., "pdf-processor" or "data-analyzer")

## Instructions for Claude

1. **Validate skill name**:
   - Check if skill name follows kebab-case format (lowercase, hyphens only)
   - Ensure it's not empty and doesn't contain invalid characters
   - If invalid, ask user for a corrected name

2. **Determine skill location**:
   - Check if in a git repository (look for .git directory)
   - If in git repo: create in `.claude/skills/`
   - If not in git repo: create in `~/.claude/skills/`
   - Inform user where the skill will be created

3. **Create directory structure**:
   ```bash
   mkdir -p <location>/skills/<skill-name>
   mkdir -p <location>/skills/<skill-name>/scripts
   mkdir -p <location>/skills/<skill-name>/examples
   mkdir -p <location>/skills/<skill-name>/templates
   ```

4. **Create template SKILL.md** with the following structure:
   ```yaml
   ---
   name: <skill-name>
   description: [Brief description of what this skill does and when to use it]
   ---

   # <Skill Name>

   Brief overview of what this Skill does.

   ## Quick start

   Provide a simple example to get started immediately.

   ## Instructions

   Step-by-step guidance for Claude:
   1. First step with clear action
   2. Second step with expected outcome
   3. Handle edge cases

   ## Examples

   Show concrete usage examples with code or commands.

   ## Requirements

   List any dependencies or prerequisites:
   ```bash
   pip install package-name
   ```
   ```

5. **Create optional supporting files**:
   - Create an empty `examples.md` with placeholder content
   - Create an empty `reference.md` with placeholder content
   - Add a simple placeholder script in `scripts/helper.py`

6. **Verify creation**:
   - List created files
   - Show the path to the main SKILL.md file
   - Provide next steps for customization

7. **Provide guidance**:
   - Explain that the user should edit the description in SKILL.md
   - Mention the importance of specific, trigger-rich descriptions
   - Suggest using the skill-writer skill for detailed guidance

## Example Output

When creating `/create-skill pdf-processor`, the output should be:

```
✅ Created skill: pdf-processor
📁 Location: /path/to/.claude/skills/pdf-processor/

📝 Created files:
- SKILL.md (main skill file)
- examples.md (for usage examples)
- reference.md (for advanced documentation)
- scripts/helper.py (utility script template)

Next steps:
1. Edit SKILL.md to update the description with specific triggers
2. Replace placeholder content with your skill's functionality
3. Test by asking Claude questions that match your description

Pro tip: Use the skill-writer skill for detailed guidance on crafting effective skills!
```

## Tips

- **Naming**: Use descriptive, kebab-case names (e.g., "api-tester" not "skill1")
- **Description**: Include both what the skill does AND when to use it
- **Location**: Skills in project directories (.claude/skills/) are shared with team
- **Testing**: Restart Claude Code after creating a new skill
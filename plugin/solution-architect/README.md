# Solution Architect

AI-powered solution architect plugin for Claude Code that decodes ideas, explores multiple solution approaches, and generates implementation roadmaps.

## Features

- **Idea Decoding**: Extract clarity from vague ideas and identify requirements
- **Solution Exploration**: Discover multiple implementation approaches
- **Gap Detection**: Find missing information before implementation
- **Tech Stack Advisory**: Get recommendations based on requirements

## Commands

| Command | Description |
|---------|-------------|
| `/analyze` | Deep analysis of an idea/problem with full decoding |
| `/brainstorm` | Quick exploration of multiple solution approaches |
| `/compare` | Side-by-side comparison of different implementation methods |
| `/roadmap` | Generates step-by-step implementation plan |

## Skills (Auto-Activating)

- **Idea Decoder** - Activates when user describes vague ideas
- **Solution Explorer** - Suggests approaches for "how to build" questions
- **Gap Detector** - Identifies missing requirements
- **Tech Stack Advisor** - Recommends tools/frameworks

## Agents

- **Architecture Expert** - System design, scalability, patterns
- **Automation Specialist** - n8n workflows, scripting, low-code solutions
- **Backend Architect** - Full backend systems, databases, APIs
- **Implementation Planner** - Roadmaps, task breakdown, priorities

## Installation

1. Copy to your project's `.claude-plugins/` directory
2. Or add to your marketplace configuration
3. Restart Claude Code

## Usage Examples

```
/analyze I want to build a real-time chat application

/brainstorm How can I automate user onboarding?

/compare n8n vs custom backend for email processing

/roadmap Build a REST API for task management
```

## Output Format

Each command generates a comprehensive analysis including:

1. **Problem Decoding** - Requirements, constraints, gaps
2. **Solution Approaches** - Multiple options with trade-offs
3. **Comparison Matrix** - Complexity, time, cost, scalability
4. **Recommended Approach** - Detailed rationale
5. **Implementation Roadmap** - Priority-ordered tasks

## License

MIT

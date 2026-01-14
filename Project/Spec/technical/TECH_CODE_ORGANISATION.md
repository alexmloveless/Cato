# Code Organisation Technical Specification

## Overview
Cato's codebase must be organised to minimise the effort required for any developer or AI model to understand, navigate, and modify the system.

## Directory Structure

### Root Level
- `agent.txt` - Navigation file for AI models/agents explaining codebase structure and common tasks
- `README.md` - Standard project readme
- `pyproject.toml` / `setup.py` - Package configuration
- `cato/` - Main package directory

### Module Directories
Each significant module directory must contain:
- `README.md` explaining:
  - Purpose of the module
  - Key classes/functions and their roles
  - How to extend the module (e.g., adding new commands)
  - Dependencies and relationships with other modules

### Command System Organisation
Commands should be organised for easy addition:
- Individual command files or grouped by functional area
- Clear registration mechanism (decorator-based)
- Adding a new command should require:
  1. Creating/editing one file
  2. No manual registration in other files

## agent.txt Specification
The root `agent.txt` file should provide:
1. Brief description of Cato
2. Directory structure overview
3. Quick navigation to common tasks:
   - Adding a new command
   - Modifying configuration
   - Adding vector store functionality
   - Modifying display/UI
4. Pointers to relevant documentation
5. List of approved dependencies

## File Organisation Principles

### Single Responsibility
- Each file should have a clear, single purpose
- Avoid monolithic files with mixed concerns

### Logical Grouping
- Group related functionality in directories
- Use clear, descriptive names

### Import Structure
- Use relative imports within package
- Avoid circular imports through proper layering

## Code Documentation

### Module-Level Docstrings
Every module should have a docstring explaining:
- What the module does
- Key classes/functions exported
- Usage examples where helpful

### Function/Class Documentation
- All public functions and classes must have docstrings (numpy format)
- Type hints required for all function signatures
- Inline comments for non-obvious logic

## Extensibility Patterns

### Command Registration
```python
# Example pattern - commands register themselves
@command(name="example", aliases=["ex"])
class ExampleCommand(BaseCommand):
    """Docstring explaining the command."""
    async def execute(self, args: list[str]) -> CommandResult:
        ...
```

### Strategy Pattern for Pluggable Components
- Vector store retrieval strategies
- Chunking strategies
- Similarity algorithms
- All should follow a common interface for easy swapping

## Configuration Integration
- No hard-coded defaults in code
- All configurable values loaded from config system
- Config values accessed through typed config objects

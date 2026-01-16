"""
Validation tests for help system consistency.

Tests cover:
- All registered commands have help entries
- Help index is consistent
- Command documentation completeness
"""

from pathlib import Path

import pytest
import yaml

from cato.commands.registry import CommandRegistry


class TestHelpSystemValidation:
    """Validate help system consistency."""

    def test_help_index_exists(self):
        """Test that help index file exists."""
        index_path = Path("cato/resources/help/index.yaml")
        assert index_path.exists(), "Help index should exist"

    def test_help_index_is_valid_yaml(self):
        """Test that help index is valid YAML."""
        index_path = Path("cato/resources/help/index.yaml")

        with index_path.open() as f:
            data = yaml.safe_load(f)

        assert data is not None
        assert isinstance(data, dict)
        assert "commands" in data

    def test_all_commands_have_help_entries(self):
        """Test that all registered commands have help entries."""
        # Load help index
        index_path = Path("cato/resources/help/index.yaml")
        with index_path.open() as f:
            help_index = yaml.safe_load(f)

        # Get registered commands
        registry = CommandRegistry()
        registered_commands = registry.list_commands()

        # Get command IDs from help index
        help_command_ids = {cmd["id"] for cmd in help_index["commands"]}

        # Check each registered command
        for name, desc, aliases in registered_commands:
            # Command or one of its aliases should be in help
            has_help = (
                name in help_command_ids
                or any(alias in help_command_ids for alias in aliases)
            )

            assert has_help, f"Command '{name}' missing from help system"

    def test_help_files_exist(self):
        """Test that referenced help files actually exist."""
        index_path = Path("cato/resources/help/index.yaml")
        with index_path.open() as f:
            help_index = yaml.safe_load(f)

        help_base = Path("cato/resources/help")

        # Check all command help files
        for cmd in help_index["commands"]:
            if "path" in cmd:
                help_file = help_base / cmd["path"]
                assert help_file.exists(), f"Help file missing: {help_file}"

    def test_help_index_structure(self):
        """Test that help index has expected structure."""
        index_path = Path("cato/resources/help/index.yaml")
        with index_path.open() as f:
            data = yaml.safe_load(f)

        # Should have topics and commands
        assert "topics" in data
        assert "commands" in data
        assert "categories" in data

        # Each command should have required fields
        for cmd in data["commands"]:
            assert "id" in cmd
            assert "title" in cmd
            assert "summary" in cmd
            assert "usage" in cmd
            assert "category" in cmd

    def test_no_orphaned_help_files(self):
        """Test that all help files in commands/ directory are referenced."""
        help_dir = Path("cato/resources/help/commands")

        if not help_dir.exists():
            pytest.skip("Help commands directory not found")

        # Get all .md files
        help_files = list(help_dir.glob("*.md"))

        # Load index
        index_path = Path("cato/resources/help/index.yaml")
        with index_path.open() as f:
            help_index = yaml.safe_load(f)

        # Get referenced files
        referenced_files = {
            Path(cmd["path"]).name
            for cmd in help_index["commands"]
            if "path" in cmd
        }

        # Check each file is referenced
        for help_file in help_files:
            assert help_file.name in referenced_files, \
                f"Orphaned help file: {help_file.name}"

    def test_categories_match_commands(self):
        """Test that all categories reference valid commands."""
        index_path = Path("cato/resources/help/index.yaml")
        with index_path.open() as f:
            help_index = yaml.safe_load(f)

        # Get all command IDs
        command_ids = {cmd["id"] for cmd in help_index["commands"]}

        # Check each category
        for category in help_index["categories"]:
            for cmd_id in category["commands"]:
                assert cmd_id in command_ids, \
                    f"Category references unknown command: {cmd_id}"

    def test_continue_command_in_help(self):
        """Test that /continue command has help documentation."""
        # This is a specific test for Phase 14 implementation
        index_path = Path("cato/resources/help/index.yaml")
        with index_path.open() as f:
            help_index = yaml.safe_load(f)

        command_ids = {cmd["id"] for cmd in help_index["commands"]}
        assert "continue" in command_ids, "/continue command should have help entry"

        # Check help file exists
        continue_help = Path("cato/resources/help/commands/continue.md")
        assert continue_help.exists(), "/continue help file should exist"


class TestCommandDocumentationCompleteness:
    """Test that command documentation is complete and useful."""

    def test_help_files_not_empty(self):
        """Test that help files contain actual content."""
        help_dir = Path("cato/resources/help/commands")

        if not help_dir.exists():
            pytest.skip("Help commands directory not found")

        for help_file in help_dir.glob("*.md"):
            content = help_file.read_text()

            # Should have more than just a title
            assert len(content) > 50, f"Help file too short: {help_file.name}"

            # Should contain usage section
            assert "usage" in content.lower() or "##" in content, \
                f"Help file should have structure: {help_file.name}"

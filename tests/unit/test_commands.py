"""
Unit tests for command parsing and registry.

Tests cover:
- Command input parsing
- Quoted string handling
- Edge cases and malformed input
- Command registration
- Alias resolution
"""

import pytest

from cato.commands.parser import parse_command_input
from cato.commands.registry import CommandRegistry, command


class TestCommandParsing:
    """Test command input parsing."""

    def test_simple_command(self):
        """Test parsing simple command without arguments."""
        result = parse_command_input("/help")
        assert result == ("help", [])

    def test_command_with_args(self):
        """Test parsing command with arguments."""
        result = parse_command_input("/model gpt-4")
        assert result == ("model", ["gpt-4"])

    def test_command_with_multiple_args(self):
        """Test parsing command with multiple arguments."""
        result = parse_command_input("/speak nova tts-1")
        assert result == ("speak", ["nova", "tts-1"])

    def test_command_with_quoted_arg(self):
        """Test parsing command with quoted string argument."""
        result = parse_command_input('/web "search query"')
        assert result == ("web", ["search query"])

    def test_command_with_quoted_and_unquoted(self):
        """Test mixing quoted and unquoted arguments."""
        result = parse_command_input('/web "search query" google')
        assert result == ("web", ["search query", "google"])

    def test_command_with_single_quotes(self):
        """Test parsing with single quotes."""
        result = parse_command_input("/web 'single quoted'")
        assert result == ("web", ["single quoted"])

    def test_non_command_input(self):
        """Test that regular text is not parsed as command."""
        result = parse_command_input("hello world")
        assert result is None

    def test_empty_input(self):
        """Test empty input."""
        result = parse_command_input("")
        assert result is None

    def test_just_slash(self):
        """Test input with only slash."""
        result = parse_command_input("/")
        assert result is None

    def test_command_case_insensitive(self):
        """Test that command names are converted to lowercase."""
        result = parse_command_input("/HELP")
        assert result == ("help", [])

        result = parse_command_input("/Help")
        assert result == ("help", [])

    def test_leading_trailing_whitespace(self):
        """Test handling of whitespace."""
        result = parse_command_input("  /help  ")
        assert result == ("help", [])

        result = parse_command_input("  /model   gpt-4  ")
        assert result == ("model", ["gpt-4"])

    def test_unbalanced_quotes(self):
        """Test handling of unbalanced quotes."""
        result = parse_command_input('/web "unclosed quote')
        assert result is not None
        assert result[0] == "web"
        # Should handle gracefully

    def test_escaped_quotes(self):
        """Test escaped quotes in arguments."""
        result = parse_command_input(r'/echo "He said \"hello\""')
        assert result is not None
        assert result[0] == "echo"

    def test_multiple_spaces_between_args(self):
        """Test multiple spaces between arguments."""
        result = parse_command_input("/command    arg1    arg2")
        assert result == ("command", ["arg1", "arg2"])

    def test_numeric_arguments(self):
        """Test numeric arguments remain as strings."""
        result = parse_command_input("/delete 5")
        assert result == ("delete", ["5"])
        assert isinstance(result[1][0], str)

    def test_special_characters_in_args(self):
        """Test special characters in arguments."""
        result = parse_command_input("/url https://example.com/path?key=value")
        assert result == ("url", ["https://example.com/path?key=value"])

    def test_hyphenated_args(self):
        """Test arguments with hyphens."""
        result = parse_command_input("/st -s pending -o priority")
        assert result == ("st", ["-s", "pending", "-o", "priority"])

    def test_empty_quoted_string(self):
        """Test empty quoted string."""
        result = parse_command_input('/web ""')
        assert result == ("web", [""])


class TestCommandRegistry:
    """Test command registration system."""

    def test_register_simple_command(self):
        """Test registering a command with decorator."""
        @command(name="test_cmd")
        async def test_command(ctx, *args):
            return "test"

        registry = CommandRegistry()
        cmd = registry.get("test_cmd")
        assert cmd is not None
        assert cmd._cmd_name == "test_cmd"

    def test_register_with_aliases(self):
        """Test registering command with aliases."""
        @command(name="test_alias", aliases=["ta", "test"])
        async def test_command(ctx, *args):
            return "test"

        registry = CommandRegistry()

        # Main command
        cmd = registry.get("test_alias")
        assert cmd is not None

        # Aliases
        assert registry.get("ta") == cmd
        assert registry.get("test") == cmd

    def test_get_with_slash_prefix(self):
        """Test that get() works with or without slash."""
        @command(name="slash_test")
        async def test_command(ctx, *args):
            return "test"

        registry = CommandRegistry()

        assert registry.get("slash_test") is not None
        assert registry.get("/slash_test") is not None
        assert registry.get("slash_test") == registry.get("/slash_test")

    def test_get_nonexistent_command(self):
        """Test getting command that doesn't exist."""
        registry = CommandRegistry()
        cmd = registry.get("nonexistent")
        assert cmd is None

    def test_resolve_alias(self):
        """Test alias resolution."""
        @command(name="primary", aliases=["alias1", "alias2"])
        async def test_command(ctx, *args):
            return "test"

        registry = CommandRegistry()

        assert registry.resolve_alias("alias1") == "primary"
        assert registry.resolve_alias("alias2") == "primary"
        assert registry.resolve_alias("primary") == "primary"
        assert registry.resolve_alias("nonexistent") == "nonexistent"

    def test_list_commands(self):
        """Test listing all registered commands."""
        @command(name="cmd1", aliases=["c1"], description="First command")
        async def command1(ctx, *args):
            pass

        @command(name="cmd2", aliases=["c2"], description="Second command")
        async def command2(ctx, *args):
            pass

        registry = CommandRegistry()
        commands = registry.list_commands()

        # Should include our test commands (and possibly others from imports)
        cmd_names = [name for name, _, _ in commands]
        assert "cmd1" in cmd_names
        assert "cmd2" in cmd_names

        # Check format: list of (name, description, aliases) tuples
        for name, desc, aliases in commands:
            assert isinstance(name, str)
            assert isinstance(desc, str)
            assert isinstance(aliases, list)


class TestCommandDecorator:
    """Test command decorator functionality."""

    def test_decorator_attaches_metadata(self):
        """Test that decorator attaches metadata to function."""
        @command(
            name="meta_test",
            aliases=["mt"],
            description="Test command",
            usage="/meta_test [arg]"
        )
        async def test_command(ctx, *args):
            return "test"

        assert hasattr(test_command, "_cmd_name")
        assert test_command._cmd_name == "meta_test"
        assert test_command._cmd_aliases == ["mt"]
        assert test_command._cmd_description == "Test command"
        assert test_command._cmd_usage == "/meta_test [arg]"

    def test_decorator_without_optional_params(self):
        """Test decorator with only required parameters."""
        @command(name="minimal")
        async def test_command(ctx, *args):
            return "test"

        assert test_command._cmd_name == "minimal"
        assert test_command._cmd_aliases == []
        assert test_command._cmd_description == ""
        assert test_command._cmd_usage == ""


class TestCommandIntegration:
    """Test integration between parser and registry."""

    def test_parse_and_lookup(self):
        """Test parsing input and looking up command."""
        @command(name="lookup_test", aliases=["lt"])
        async def test_command(ctx, *args):
            return "success"

        # Parse command input
        result = parse_command_input("/lookup_test arg1 arg2")
        assert result is not None

        cmd_name, args = result

        # Lookup in registry
        registry = CommandRegistry()
        cmd = registry.get(cmd_name)
        assert cmd is not None
        assert args == ["arg1", "arg2"]

    def test_parse_alias_and_lookup(self):
        """Test parsing alias and resolving to main command."""
        @command(name="alias_main", aliases=["am"])
        async def test_command(ctx, *args):
            return "success"

        # Parse using alias
        result = parse_command_input("/am test")
        assert result is not None

        cmd_name, args = result

        # Lookup in registry (should resolve alias)
        registry = CommandRegistry()
        cmd = registry.get(cmd_name)
        assert cmd is not None
        assert cmd._cmd_name == "alias_main"


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_parse_command_with_only_whitespace(self):
        """Test command with only whitespace after slash."""
        result = parse_command_input("/   ")
        assert result is None

    def test_parse_very_long_command(self):
        """Test parsing very long command input."""
        long_arg = "a" * 1000
        result = parse_command_input(f"/cmd {long_arg}")
        assert result is not None
        assert result[0] == "cmd"
        assert result[1][0] == long_arg

    def test_parse_unicode_in_arguments(self):
        """Test Unicode characters in arguments."""
        result = parse_command_input("/echo 你好世界")
        assert result == ("echo", ["你好世界"])

    def test_parse_emoji_in_arguments(self):
        """Test emoji in arguments."""
        result = parse_command_input("/echo 🚀✨")
        assert result == ("echo", ["🚀✨"])

    def test_multiple_consecutive_slashes(self):
        """Test input with multiple slashes."""
        result = parse_command_input("//help")
        # Should parse '/help' as command
        assert result == ("/help", [])

    def test_command_with_equals_sign(self):
        """Test argument with equals sign."""
        result = parse_command_input("/config key=value")
        assert result == ("config", ["key=value"])

    def test_tabs_in_input(self):
        """Test handling of tab characters."""
        result = parse_command_input("/cmd\targ1\targ2")
        assert result is not None
        # Tabs should be treated as whitespace
        assert result[0] == "cmd"

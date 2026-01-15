"""Help system service for loading and rendering help content."""

import logging
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


class HelpService:
    """
    Service for loading and rendering help documentation.
    
    Loads help index and resolves topics, categories, and commands to markdown files.
    
    Parameters
    ----------
    help_dir : Path
        Path to help resources directory.
    """
    
    def __init__(self, help_dir: Path | None = None) -> None:
        if help_dir is None:
            # Default to package resources
            help_dir = Path(__file__).parent.parent / "resources" / "help"
        
        self._help_dir = help_dir
        self._index = self._load_index()
        logger.info(f"HelpService initialized with {len(self._index['commands'])} commands")
    
    def _load_index(self) -> dict[str, Any]:
        """
        Load help index from YAML file.
        
        Returns
        -------
        dict[str, Any]
            Parsed index with topics, categories, and commands.
        
        Raises
        ------
        FileNotFoundError
            If index.yaml not found.
        """
        index_path = self._help_dir / "index.yaml"
        if not index_path.exists():
            raise FileNotFoundError(f"Help index not found: {index_path}")
        
        with index_path.open() as f:
            return yaml.safe_load(f)
    
    def get_help_content(self, query: str | None = None) -> str | None:
        """
        Get help content for a query.
        
        Parameters
        ----------
        query : str | None, optional
            Topic, category, or command to get help for.
            If None, returns overview.
        
        Returns
        -------
        str | None
            Help content as markdown, or None if not found.
        """
        if not query:
            # Show overview
            return self._load_topic("overview")
        
        # Try as topic
        topic = self._find_topic(query)
        if topic:
            return self._load_topic(topic["id"])
        
        # Try as category
        category = self._find_category(query)
        if category:
            return self._generate_category_page(category)
        
        # Try as command (including aliases)
        command = self._find_command(query)
        if command:
            return self._load_command(command["id"])
        
        return None
    
    def get_all_help_files(self) -> list[tuple[str, str]]:
        """
        Get all help content for /help model context.
        
        Returns
        -------
        list[tuple[str, str]]
            List of (file_path, content) tuples.
        """
        files = []
        
        # Add index
        index_path = self._help_dir / "index.yaml"
        if index_path.exists():
            files.append((str(index_path), index_path.read_text()))
        
        # Add all topics
        for topic in self._index.get("topics", []):
            topic_path = self._help_dir / topic["path"]
            if topic_path.exists():
                files.append((str(topic_path), topic_path.read_text()))
        
        # Add all command pages
        for command in self._index.get("commands", []):
            cmd_path = self._help_dir / command["path"]
            if cmd_path.exists():
                content = cmd_path.read_text()
                # Only add unique paths (some commands share files)
                if not any(f[0] == str(cmd_path) for f in files):
                    files.append((str(cmd_path), content))
        
        return files
    
    def _find_topic(self, topic_id: str) -> dict[str, Any] | None:
        """Find topic by ID."""
        for topic in self._index.get("topics", []):
            if topic["id"] == topic_id:
                return topic
        return None
    
    def _find_category(self, category_id: str) -> dict[str, Any] | None:
        """Find category by ID."""
        for category in self._index.get("categories", []):
            if category["id"] == category_id:
                return category
        return None
    
    def _find_command(self, query: str) -> dict[str, Any] | None:
        """
        Find command by ID or alias.
        
        Parameters
        ----------
        query : str
            Command ID or alias to search for.
        
        Returns
        -------
        dict[str, Any] | None
            Command entry or None if not found.
        """
        for command in self._index.get("commands", []):
            # Check ID
            if command["id"] == query:
                return command
            # Check aliases
            if query in command.get("aliases", []):
                return command
        return None
    
    def _load_topic(self, topic_id: str) -> str | None:
        """Load topic markdown file."""
        topic = self._find_topic(topic_id)
        if not topic:
            return None
        
        topic_path = self._help_dir / topic["path"]
        if not topic_path.exists():
            logger.warning(f"Topic file not found: {topic_path}")
            return None
        
        return topic_path.read_text()
    
    def _load_command(self, command_id: str) -> str | None:
        """Load command markdown file."""
        for command in self._index.get("commands", []):
            if command["id"] == command_id:
                cmd_path = self._help_dir / command["path"]
                if not cmd_path.exists():
                    logger.warning(f"Command help file not found: {cmd_path}")
                    return None
                return cmd_path.read_text()
        return None
    
    def _generate_category_page(self, category: dict[str, Any]) -> str:
        """
        Generate category page listing commands.
        
        Parameters
        ----------
        category : dict[str, Any]
            Category entry from index.
        
        Returns
        -------
        str
            Generated markdown content.
        """
        lines = [f"# {category['title']}\n"]
        
        # Get commands in this category
        command_ids = category.get("commands", [])
        commands = [
            cmd for cmd in self._index.get("commands", [])
            if cmd["id"] in command_ids
        ]
        
        for cmd in commands:
            aliases = cmd.get("aliases", [])
            alias_str = f" (aliases: {', '.join(aliases)})" if aliases else ""
            lines.append(f"- `{cmd['usage']}` - {cmd['summary']}{alias_str}")
        
        lines.append("\n---\n")
        lines.append("Use `/help <command>` for detailed help on any command.")
        
        return "\n".join(lines)
    
    def get_suggestions(self, query: str) -> list[str]:
        """
        Get suggestions for unknown query.
        
        Parameters
        ----------
        query : str
            Failed query.
        
        Returns
        -------
        list[str]
            List of similar command/topic names.
        """
        suggestions = []
        
        # Check topics
        for topic in self._index.get("topics", []):
            if query.lower() in topic["id"].lower():
                suggestions.append(topic["id"])
        
        # Check categories
        for category in self._index.get("categories", []):
            if query.lower() in category["id"].lower():
                suggestions.append(category["id"])
        
        # Check commands
        for command in self._index.get("commands", []):
            if query.lower() in command["id"].lower():
                suggestions.append(command["id"])
            # Check aliases
            for alias in command.get("aliases", []):
                if query.lower() in alias.lower():
                    suggestions.append(command["id"])
        
        return list(set(suggestions))[:5]  # Return up to 5 unique suggestions

#!/usr/bin/env python3
"""Contact Book CLI - Main entry point."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from textual.app import App, ComposeResult
from contactbook.ui import ContactBookApp
from contactbook.models import ContactBook
from contactbook.storage import ContactBookStorage


class ContactBookApplication(App):
    """Main Textual application for Contact Book."""
    
    TITLE = "📇 Contact Book CLI"
    BINDINGS = []
    
    CSS = """
    Screen {
        background: $surface;
        color: $text;
    }
    """

    def __init__(self):
        """Initialize the application."""
        super().__init__()
        # Initialize contact book data
        self.storage = ContactBookStorage("data/contacts.json")
        self.contact_book = self.storage.load()

    def compose(self) -> ComposeResult:
        """Compose the application."""
        yield ContactBookApp()

    def on_mount(self) -> None:
        """On mount, set up the app."""
        # Get the ContactBookApp screen and set its contact_book
        screen = self.screen
        if hasattr(screen, 'contact_book'):
            screen.contact_book = self.contact_book
            screen.storage = self.storage


def main():
    """Run the application."""
    app = ContactBookApplication()
    app.run()


if __name__ == "__main__":
    main()

"""Main TUI application using Textual framework."""

from textual.app import ComposeResult
from textual.widgets import (
    Header, Footer, Static, Input, Button, Label
)
from textual.containers import Horizontal, Container
from textual.screen import ModalScreen, Screen
from textual.binding import Binding
from rich.table import Table
from datetime import datetime
from typing import Optional

from contactbook.models import Contact
from contactbook.storage import ContactBookStorage


class ContactDetailModal(ModalScreen):
    """Modal for viewing/editing contact details."""

    CSS = """
    ContactDetailModal {
        align: center middle;
    }

    ContactDetailModal > Container {
        width: 80;
        height: auto;
        border: solid $accent;
        background: $surface;
    }
    """

    def __init__(self, contact: Optional[Contact] = None):
        """Initialize with optional contact to edit."""
        super().__init__()
        self.contact = contact
        self.is_new = contact is None

    def compose(self) -> ComposeResult:
        """Compose the modal layout."""
        contact = self.contact or Contact(name="")
        
        with Container():
            yield Label("✏️  [bold cyan]CONTACT DETAILS[/bold cyan]" if not self.is_new else "✏️  [bold green]NEW CONTACT[/bold green]")
            yield Input(value=contact.name, id="name", placeholder="Name *")
            yield Input(value=contact.email or "", id="email", placeholder="Email")
            yield Input(value=contact.phone or "", id="phone", placeholder="Phone")
            yield Input(value=contact.address or "", id="address", placeholder="Address")
            yield Input(value=contact.birthday or "", id="birthday", placeholder="Birthday (YYYY-MM-DD)")
            yield Input(value=contact.notes or "", id="notes", placeholder="Notes")
            yield Input(value=",".join(contact.tags), id="tags", placeholder="Tags (comma-separated)")
            
            with Horizontal():
                yield Button("💾 Save", id="save", variant="success")
                yield Button("❌ Cancel", id="cancel", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button actions."""
        if event.button.id == "save":
            self._save_contact()
        elif event.button.id == "cancel":
            self.app.pop_screen()

    def _save_contact(self) -> None:
        """Save contact from form inputs."""
        name_input = self.query_one("#name", Input)
        
        if not name_input.value.strip():
            self.app.notify("Name is required!", severity="error")
            return

        email_input = self.query_one("#email", Input)
        phone_input = self.query_one("#phone", Input)
        address_input = self.query_one("#address", Input)
        birthday_input = self.query_one("#birthday", Input)
        notes_input = self.query_one("#notes", Input)
        tags_input = self.query_one("#tags", Input)

        if self.contact:
            # Update existing contact
            self.contact.name = name_input.value
            self.contact.email = email_input.value or None
            self.contact.phone = phone_input.value or None
            self.contact.address = address_input.value or None
            self.contact.birthday = birthday_input.value or None
            self.contact.notes = notes_input.value or None
            self.contact.tags = set(t.strip() for t in tags_input.value.split(',') if t.strip())
            self.contact.updated_at = datetime.now().isoformat()
        else:
            # Create new contact
            self.contact = Contact(
                name=name_input.value,
                email=email_input.value or None,
                phone=phone_input.value or None,
                address=address_input.value or None,
                birthday=birthday_input.value or None,
                notes=notes_input.value or None,
                tags=set(t.strip() for t in tags_input.value.split(',') if t.strip())
            )

        self.app.dismiss(self.contact)


class SearchBar(Static):
    """Search bar with live filtering."""
    
    DEFAULT_CSS = """
    SearchBar {
        height: 3;
        border: solid $accent;
        background: $panel;
    }
    """

    def compose(self) -> ComposeResult:
        """Compose search bar."""
        yield Input(id="search-input", placeholder="🔍 Search by name, email, phone, or tags...")

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle search input changes."""
        try:
            contact_list = self.app.query_one("#contact-list", ContactListWidget)
            contact_list.filter_contacts(event.value)
        except:
            pass


class ContactListWidget(Static):
    """Widget displaying the list of contacts."""
    
    DEFAULT_CSS = """
    ContactListWidget {
        height: 1fr;
        border: solid $success;
        background: $panel;
    }
    """

    def __init__(self, **kwargs):
        """Initialize contact list."""
        super().__init__(**kwargs)
        self.contacts = []
        self.filtered_contacts = []

    def render(self) -> str:
        """Render contact list as table."""
        if not self.filtered_contacts:
            if not self.contacts:
                return "[dim]No contacts yet. Press [bold]Ctrl+N[/bold] to add one.[/dim]"
            return "[dim]No contacts match your search.[/dim]"

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Name", style="cyan")
        table.add_column("Email", style="green")
        table.add_column("Phone", style="yellow")
        table.add_column("Tags", style="magenta")
        
        for contact in self.filtered_contacts[:20]:  # Show first 20
            tags_str = ", ".join(contact.tags) if contact.tags else "-"
            birthday_marker = "🎂" if contact.is_birthday_today() else ""
            name = f"{contact.name} {birthday_marker}"
            table.add_row(
                name,
                contact.email or "-",
                contact.phone or "-",
                tags_str
            )

        return str(table)

    def update_contacts(self, contacts: list) -> None:
        """Update the contact list."""
        self.contacts = contacts
        self.filtered_contacts = contacts
        self.refresh()

    def filter_contacts(self, query: str) -> None:
        """Filter contacts by search query."""
        if not query:
            self.filtered_contacts = self.contacts
        else:
            self.filtered_contacts = [c for c in self.contacts if self._matches_query(c, query)]
        self.refresh()

    def _matches_query(self, contact: Contact, query: str) -> bool:
        """Check if contact matches search query."""
        query_lower = query.lower()
        return (
            query_lower in contact.name.lower() or
            (contact.email and query_lower in contact.email.lower()) or
            (contact.phone and query_lower in contact.phone) or
            any(query_lower in tag.lower() for tag in contact.tags)
        )


class StatsPanel(Static):
    """Panel showing contact statistics."""
    
    DEFAULT_CSS = """
    StatsPanel {
        width: 40;
        height: auto;
        border: solid $accent;
        background: $boost;
        text-align: center;
    }
    """

    def render(self) -> str:
        """Render statistics."""
        try:
            # Try to get from the screen first
            screen = self.screen
            if hasattr(screen, 'contact_book'):
                contact_book = screen.contact_book
            elif hasattr(self.app, 'contact_book'):
                contact_book = self.app.contact_book
            else:
                return "[dim]Loading...[/dim]"
            
            total = len(contact_book.contacts)
            with_tags = len([c for c in contact_book.contacts if c.tags])
            with_birthdays = len([c for c in contact_book.contacts if c.birthday])
            upcoming = len(contact_book.get_upcoming_birthdays(7))

            stats = f"""
📊 [bold cyan]STATISTICS[/bold cyan]
━━━━━━━━━━━━━━━━━━━━━━
👥 Total: {total}
🏷️  Tagged: {with_tags}
🎂 Birthdays: {with_birthdays}
🎉 Upcoming: {upcoming}
            """
            return stats
        except Exception as e:
            return f"[red]Error: {e}[/red]"


class ContactBookApp(Screen):
    """Main contact book application screen."""

    TITLE = "📇 Contact Book CLI"
    BINDINGS = [
        Binding("ctrl+n", "new_contact", "New"),
        Binding("ctrl+f", "focus_search", "Search"),
        Binding("ctrl+e", "export", "Export"),
        Binding("ctrl+i", "import_contacts", "Import"),
        Binding("ctrl+q", "quit", "Quit"),
    ]

    DEFAULT_CSS = """
    ContactBookApp {
        layout: vertical;
    }

    Horizontal {
        height: 1fr;
    }

    SearchBar {
        margin: 0 1;
    }

    ContactListWidget {
        margin: 0 1 1 1;
    }

    StatsPanel {
        margin: 1;
    }
    """

    def __init__(self):
        """Initialize the application."""
        super().__init__()
        self.storage = ContactBookStorage("data/contacts.json")
        self.contact_book = self.storage.load()

    def compose(self) -> ComposeResult:
        """Compose the application layout."""
        yield Header(show_clock=True)
        yield Label("[bold cyan]📇 CONTACT BOOK CLI[/bold cyan]", id="title")
        yield SearchBar(id="search-bar")
        
        with Horizontal():
            yield ContactListWidget(id="contact-list")
            yield StatsPanel(id="stats")

        yield Footer()

    def on_mount(self) -> None:
        """Initialize the app on mount."""
        # Make sure parent app has contact_book
        if hasattr(self.app, 'contact_book'):
            self.contact_book = self.app.contact_book
            self.storage = self.app.storage
        self.load_contacts()
        self.app.notify("Welcome! Press Ctrl+N to add a contact.", timeout=3)

    def load_contacts(self) -> None:
        """Load and display contacts."""
        contact_list = self.query_one("#contact-list", ContactListWidget)
        contact_list.update_contacts(
            sorted(self.contact_book.contacts, key=lambda c: c.name)
        )
        
        stats_panel = self.query_one("#stats", StatsPanel)
        stats_panel.refresh()

    def action_new_contact(self) -> None:
        """Create a new contact."""
        def add_contact(contact: Contact) -> None:
            self.contact_book.add_contact(contact)
            self.storage.save(self.contact_book)
            self.load_contacts()
            self.app.notify(f"✅ Contact '{contact.name}' added!", timeout=2)

        modal = ContactDetailModal()
        self.app.push_screen(modal, add_contact)

    def action_focus_search(self) -> None:
        """Focus on search bar."""
        search_input = self.query_one("#search-input", Input)
        self.app.set_focus(search_input)

    def action_export(self) -> None:
        """Export contacts."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_file = f"data/export_contacts_{timestamp}.csv"
        json_file = f"data/export_contacts_{timestamp}.json"
        
        csv_success = self.storage.export_csv(self.contact_book, csv_file)
        json_success = self.storage.export_json(self.contact_book, json_file)
        
        if csv_success and json_success:
            self.app.notify(f"✅ Exported to CSV and JSON!", timeout=2)
        else:
            self.app.notify("❌ Export failed!", severity="error", timeout=2)

    def action_import_contacts(self) -> None:
        """Import contacts."""
        # Simple import from CSV
        import_file = "data/import_contacts.csv"
        try:
            if self.storage.import_csv(self.contact_book, import_file):
                self.storage.save(self.contact_book)
                self.load_contacts()
                self.app.notify(f"✅ Imported contacts successfully!", timeout=2)
            else:
                self.app.notify("❌ No import file found at data/import_contacts.csv", severity="error", timeout=2)
        except Exception as e:
            self.app.notify(f"❌ Import failed: {e}", severity="error", timeout=2)

    def action_quit(self) -> None:
        """Quit the application."""
        self.app.exit()

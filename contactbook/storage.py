"""Storage and persistence for the contact book."""

import json
from pathlib import Path
from typing import Optional
from .models import ContactBook, Contact


class ContactBookStorage:
    """Handles file-based persistence for contact book data."""

    def __init__(self, filepath: str = "data/contacts.json"):
        """Initialize storage with a file path."""
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> ContactBook:
        """Load contact book from file."""
        if self.filepath.exists():
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return ContactBook(**data)
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error loading contacts: {e}")
                return ContactBook()
        return ContactBook()

    def save(self, contact_book: ContactBook) -> bool:
        """Save contact book to file."""
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(contact_book.model_dump(), f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving contacts: {e}")
            return False

    def export_csv(self, contact_book: ContactBook, filepath: str) -> bool:
        """Export contacts to CSV format."""
        try:
            import csv
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['Name', 'Email', 'Phone', 'Address', 'Birthday', 'Notes', 'Tags']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for contact in contact_book.contacts:
                    writer.writerow({
                        'Name': contact.name,
                        'Email': contact.email or '',
                        'Phone': contact.phone or '',
                        'Address': contact.address or '',
                        'Birthday': contact.birthday or '',
                        'Notes': contact.notes or '',
                        'Tags': ','.join(contact.tags)
                    })
            return True
        except Exception as e:
            print(f"Error exporting CSV: {e}")
            return False

    def import_csv(self, contact_book: ContactBook, filepath: str) -> bool:
        """Import contacts from CSV format."""
        try:
            import csv
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    contact = Contact(
                        name=row.get('Name', ''),
                        email=row.get('Email') or None,
                        phone=row.get('Phone') or None,
                        address=row.get('Address') or None,
                        birthday=row.get('Birthday') or None,
                        notes=row.get('Notes') or None,
                        tags=set(t.strip() for t in row.get('Tags', '').split(',') if t.strip())
                    )
                    contact_book.add_contact(contact)
            return True
        except Exception as e:
            print(f"Error importing CSV: {e}")
            return False

    def export_json(self, contact_book: ContactBook, filepath: str) -> bool:
        """Export contacts to JSON format."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(contact_book.model_dump(), f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error exporting JSON: {e}")
            return False

    def import_json(self, contact_book: ContactBook, filepath: str) -> bool:
        """Import contacts from JSON format."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict) and 'contacts' in data:
                    for contact_data in data['contacts']:
                        contact = Contact(**contact_data)
                        contact_book.add_contact(contact)
                    return True
            return False
        except Exception as e:
            print(f"Error importing JSON: {e}")
            return False

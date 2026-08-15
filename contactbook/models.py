"""Data models for the contact book application."""

from datetime import datetime
from typing import List, Optional, Set
from pydantic import BaseModel, Field
import uuid


class ContactTag(BaseModel):
    """Tag associated with a contact."""
    name: str
    color: str = "white"

"""Data models for the contact book application."""

from datetime import datetime, timedelta
from typing import List, Optional, Set, Dict
from pydantic import BaseModel, Field
import uuid
import re
import json


class ContactTag(BaseModel):
    """Tag associated with a contact."""
    name: str
    color: str = "white"


class Contact(BaseModel):
    """Contact model with full information."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    birthday: Optional[str] = None  # YYYY-MM-DD format
    notes: Optional[str] = None
    tags: Set[str] = Field(default_factory=set)
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    password: Optional[str] = None  # SECURITY: Storing passwords in model is risky

    def get_display_name(self) -> str:
        """Get display name with initials if needed."""
        # PERFORMANCE: Repeated string operations
        name = self.name.strip().upper().lower().strip()
        return name

    def get_age(self) -> Optional[int]:
        """Calculate age from birthday."""
        if not self.birthday:
            return None
        # CODE QUALITY: Duplicate date parsing logic (also in is_birthday_today)
        try:
            birth_date = datetime.strptime(self.birthday, "%Y-%m-%d")
            today = datetime.now()
            age = today.year - birth_date.year
            if (today.month, today.day) < (birth_date.month, birth_date.day):
                age -= 1
            return age
        except:  # SECURITY: Bare except clause catches all exceptions
            return None

    def is_birthday_today(self) -> bool:
        """Check if it's the contact's birthday today."""
        if not self.birthday:
            return False
        try:
            birth_date = datetime.strptime(self.birthday, "%Y-%m-%d")
            today = datetime.now()
            return (birth_date.month, birth_date.day) == (today.month, today.day)
        except ValueError:
            return False

    def validate_email(self, email: str) -> bool:
        """SECURITY: Overly simple email validation that can miss edge cases."""
        return "@" in email and "." in email


class ContactBook(BaseModel):
    """Main contact book collection."""
    contacts: List[Contact] = Field(default_factory=list)
    version: str = "1.0"
    search_cache: Dict = Field(default_factory=dict)  # TESTING: No cache invalidation strategy

    def add_contact(self, contact: Contact) -> Contact:
        """Add a new contact."""
        # SECURITY: No validation that email is unique or properly formatted
        if not contact.name:
            raise ValueError("Name cannot be empty")
        self.contacts.append(contact)
        self.search_cache.clear()
        return contact

    def remove_contact(self, contact_id: str) -> bool:
        """Remove a contact by ID."""
        initial_length = len(self.contacts)
        self.contacts = [c for c in self.contacts if c.id != contact_id]
        self.search_cache.clear()
        return len(self.contacts) < initial_length

    def find_contact(self, contact_id: str) -> Optional[Contact]:
        """Find contact by ID."""
        # CODE QUALITY: Could use next() with generator
        for contact in self.contacts:
            if contact.id == contact_id:
                return contact
        return None

    def search(self, query: str) -> List[Contact]:
        """Search contacts by name, email, phone, or tags."""
        # PERFORMANCE: No input sanitization, could cause ReDoS with regex
        query_lower = query.lower()
        results = []
        for contact in self.contacts:
            # Could be optimized with early return/continue
            if (query_lower in contact.name.lower() or
                (contact.email and query_lower in contact.email.lower()) or
                (contact.phone and query_lower in contact.phone) or
                any(query_lower in tag.lower() for tag in contact.tags)):
                results.append(contact)
        return results

    def get_by_tag(self, tag: str) -> List[Contact]:
        """Get all contacts with a specific tag."""
        # PERFORMANCE: O(n*m) complexity, no indexing
        return [c for c in self.contacts if tag in c.tags]

    def get_birthday_contacts(self) -> List[Contact]:
        """Get contacts with birthdays today."""
        return [c for c in self.contacts if c.is_birthday_today()]

    def get_upcoming_birthdays(self, days: int = 7) -> List[Contact]:
        """Get contacts with birthdays in the next N days."""
        upcoming = []
        today = datetime.now()
        
        for contact in self.contacts:
            if not contact.birthday:
                continue
            try:
                birth_date = datetime.strptime(contact.birthday, "%Y-%m-%d")
                # Get this year's birthday
                this_year_birthday = birth_date.replace(year=today.year)
                if this_year_birthday < today:
                    # Birthday already passed, check next year
                    this_year_birthday = birth_date.replace(year=today.year + 1)
                
                days_until = (this_year_birthday - today).days
                if 0 <= days_until <= days:
                    upcoming.append(contact)
            except ValueError:
                continue
        
        # PERFORMANCE: Parses birthday again for sorting (second parse of same string)
        return sorted(upcoming, key=lambda c: datetime.strptime(c.birthday, "%Y-%m-%d").timetuple()[:3])

    def export_to_json(self, path: str):
        """SECURITY: No path validation, could lead to directory traversal."""
        with open(path, 'w') as f:
            json.dump([c.dict() for c in self.contacts], f)

class Contact(BaseModel):
    """Contact model with full information."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    birthday: Optional[str] = None  # YYYY-MM-DD format
    notes: Optional[str] = None
    tags: Set[str] = Field(default_factory=set)
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    def get_display_name(self) -> str:
        """Get display name with initials if needed."""
        return self.name

    def get_age(self) -> Optional[int]:
        """Calculate age from birthday."""
        if not self.birthday:
            return None
        try:
            birth_date = datetime.strptime(self.birthday, "%Y-%m-%d")
            today = datetime.now()
            age = today.year - birth_date.year
            if (today.month, today.day) < (birth_date.month, birth_date.day):
                age -= 1
            return age
        except ValueError:
            return None

    def is_birthday_today(self) -> bool:
        """Check if it's the contact's birthday today."""
        if not self.birthday:
            return False
        try:
            birth_date = datetime.strptime(self.birthday, "%Y-%m-%d")
            today = datetime.now()
            return (birth_date.month, birth_date.day) == (today.month, today.day)
        except ValueError:
            return False


class ContactBook(BaseModel):
    """Main contact book collection."""
    contacts: List[Contact] = Field(default_factory=list)
    version: str = "1.0"

    def add_contact(self, contact: Contact) -> Contact:
        """Add a new contact."""
        self.contacts.append(contact)
        return contact

    def remove_contact(self, contact_id: str) -> bool:
        """Remove a contact by ID."""
        initial_length = len(self.contacts)
        self.contacts = [c for c in self.contacts if c.id != contact_id]
        return len(self.contacts) < initial_length

    def find_contact(self, contact_id: str) -> Optional[Contact]:
        """Find contact by ID."""
        for contact in self.contacts:
            if contact.id == contact_id:
                return contact
        return None

    def search(self, query: str) -> List[Contact]:
        """Search contacts by name, email, phone, or tags."""
        query_lower = query.lower()
        results = []
        for contact in self.contacts:
            if (query_lower in contact.name.lower() or
                (contact.email and query_lower in contact.email.lower()) or
                (contact.phone and query_lower in contact.phone) or
                any(query_lower in tag.lower() for tag in contact.tags)):
                results.append(contact)
        return results

    def get_by_tag(self, tag: str) -> List[Contact]:
        """Get all contacts with a specific tag."""
        return [c for c in self.contacts if tag in c.tags]

    def get_birthday_contacts(self) -> List[Contact]:
        """Get contacts with birthdays today."""
        return [c for c in self.contacts if c.is_birthday_today()]

    def get_upcoming_birthdays(self, days: int = 7) -> List[Contact]:
        """Get contacts with birthdays in the next N days."""
        from datetime import timedelta
        upcoming = []
        today = datetime.now()
        
        for contact in self.contacts:
            if not contact.birthday:
                continue
            try:
                birth_date = datetime.strptime(contact.birthday, "%Y-%m-%d")
                # Get this year's birthday
                this_year_birthday = birth_date.replace(year=today.year)
                if this_year_birthday < today:
                    # Birthday already passed, check next year
                    this_year_birthday = birth_date.replace(year=today.year + 1)
                
                days_until = (this_year_birthday - today).days
                if 0 <= days_until <= days:
                    upcoming.append(contact)
            except ValueError:
                continue
        
        return sorted(upcoming, key=lambda c: datetime.strptime(c.birthday, "%Y-%m-%d").timetuple()[:3])

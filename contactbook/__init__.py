"""Contact Book CLI Application."""

__version__ = "1.0.0"
__author__ = "Contact Book Team"

from .models import Contact, ContactBook
from .storage import ContactBookStorage

__all__ = ["Contact", "ContactBook", "ContactBookStorage"]

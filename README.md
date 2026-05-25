# Contact Book CLI 📇

A modern, feature-rich terminal-based contact management application built with Python and Textual. Manage your contacts with a beautiful graphical overlay in your terminal!

## Features ✨

- **Add, Edit, Delete, Search Contacts** - Full CRUD operations with an intuitive interface
- **Contact Organization** - Tag your contacts for easy categorization
- **Birthday Reminders** - Track birthdays and get upcoming birthday notifications
- **Import/Export** - Backup and restore contacts in CSV and JSON formats
- **Search & Filter** - Real-time search across all contact fields
- **Beautiful TUI** - Modern terminal UI with colors, animations, and statistics
- **Persistent Storage** - Automatically saves all changes

## Installation 🚀

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Navigate to the project directory:
```bash
cd contactbook-cli-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage 📖

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | Create new contact |
| `Ctrl+F` | Focus search bar |
| `Ctrl+E` | Export contacts (CSV + JSON) |
| `Ctrl+I` | Import contacts from CSV |
| `Ctrl+Q` | Quit application |

### Creating a Contact

1. Press `Ctrl+N` to open the new contact dialog
2. Fill in the contact details (Name is required)
3. Press `Tab` to move between fields
4. Add tags separated by commas (e.g., "work, friend, family")
5. Enter birthday in YYYY-MM-DD format for birthday tracking
6. Click Save or press Enter

### Searching Contacts

1. Press `Ctrl+F` to focus the search bar
2. Type to search by:
   - Contact name
   - Email address
   - Phone number
   - Tags

3. Results update in real-time

### Birthday Tracking

- Contacts with birthdays today show a 🎂 emoji
- View upcoming birthdays in the statistics panel
- Birthdays should be in YYYY-MM-DD format

### Data Storage

All contacts are automatically saved to:
- **Local storage**: `data/contacts.json`

### Export/Import

**Export:**
- Press `Ctrl+E` to export contacts
- Files are saved with timestamps:
  - CSV: `data/export_contacts_YYYYMMDD_HHMMSS.csv`
  - JSON: `data/export_contacts_YYYYMMDD_HHMMSS.json`

**Import:**
- Place your CSV file at: `data/import_contacts.csv`
- Press `Ctrl+I` to import
- CSV should have headers: Name, Email, Phone, Address, Birthday, Notes, Tags

## Project Structure 📂

```
contactbook-cli-ai/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── contactbook/
│   ├── __init__.py        # Package initialization
│   ├── models.py          # Data models (Contact, ContactBook)
│   ├── storage.py         # File persistence (JSON, CSV)
│   └── ui.py              # Textual UI components
└── data/
    └── contacts.json      # Contact storage (auto-created)
```

## Contact Model 📋

Each contact can store:
- **Name** (required)
- **Email** (optional)
- **Phone** (optional)
- **Address** (optional)
- **Birthday** (YYYY-MM-DD format)
- **Notes** (text)
- **Tags** (comma-separated)
- **Metadata** (creation and update timestamps)

## Example CSV Import Format

```csv
Name,Email,Phone,Address,Birthday,Notes,Tags
John Doe,john@example.com,555-1234,123 Main St,1990-05-15,My best friend,friend
Jane Smith,jane@work.com,555-5678,456 Office Ave,1985-03-22,My colleague,work,friend
```

## Technologies Used 🛠️

- **[Textual](https://textualize.io/)** - Modern TUI framework for Python
- **[Rich](https://rich.readthedocs.io/)** - Beautiful terminal formatting
- **[Pydantic](https://docs.pydantic.dev/)** - Data validation and parsing
- **Python 3.8+** - Core language

## Future Ideas 💡

- Categories/Groups for better organization
- Phone call history tracking
- Photo/Avatar support
- Contact sync to cloud services
- Backup automation
- Advanced filtering and sorting
- Contact duplication detection
- Email integration
- Social media profile links

## Troubleshooting 🔧

### Port Already in Use
If you encounter issues, try running with a different terminal emulator or check if another instance is running.

### Import Issues
- Ensure CSV file has proper headers
- Check that file is saved as UTF-8 encoding
- Place file at `data/import_contacts.csv`

### Display Issues
- Try resizing your terminal window
- Ensure your terminal supports 256 colors
- Update Textual: `pip install --upgrade textual`

## License 📄

MIT License - Feel free to use, modify, and distribute!

## Support 📞

For issues or suggestions, create documentation or reach out to the development team.

---

**Enjoy managing your contacts! 📇✨**

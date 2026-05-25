#!/usr/bin/env python3
"""Setup and installation script for Contact Book CLI."""

import subprocess
import sys
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8+ required. You have {sys.version_info.major}.{sys.version_info.minor}")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")


def install_dependencies():
    """Install required packages."""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)


def create_data_directory():
    """Ensure data directory exists."""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    print(f"✅ Data directory ready at {data_dir.absolute()}")


def main():
    """Run setup process."""
    print("╔═══════════════════════════════════╗")
    print("║  📇 Contact Book CLI Setup       ║")
    print("╚═══════════════════════════════════╝\n")
    
    check_python_version()
    create_data_directory()
    
    response = input("\n📥 Install dependencies? (yes/no): ").lower().strip()
    if response in ("yes", "y"):
        install_dependencies()
    
    print("\n✨ Setup complete!")
    print("\n🚀 To run the application:")
    print("   python main.py")
    print("\n📖 Check README.md for usage instructions")


if __name__ == "__main__":
    main()

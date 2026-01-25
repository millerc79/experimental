"""
PDF Automation Tool - A Smart Alternative to Hazel

This tool automatically processes PDF files by:
1. Reading the content of PDFs
2. Matching content against rules (keywords)
3. Extracting dates and years from the PDF
4. Renaming files with smart patterns
5. Moving files to organized folders

KEY ADVANTAGE over Hazel: No need to update rules each year!
The tool automatically detects years from PDF content.
"""

import os
import re
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# PDF reading library - you'll need to install this
# Run: pip install PyPDF2
try:
    import PyPDF2
except ImportError:
    print("⚠️  PyPDF2 not installed. Run: pip install PyPDF2")
    exit(1)


class PDFAutomation:
    """Main class that handles PDF automation rules and processing"""

    def __init__(self, rules_file: str = "pdf_rules.json"):
        """
        Initialize the PDF automation tool

        Args:
            rules_file: Path to the JSON file containing automation rules
        """
        self.rules_file = rules_file
        self.rules = self.load_rules()

    def load_rules(self) -> List[Dict]:
        """Load automation rules from JSON file"""
        if not os.path.exists(self.rules_file):
            print(f"⚠️  Rules file '{self.rules_file}' not found!")
            print("Creating a sample rules file...")
            self.create_sample_rules()

        with open(self.rules_file, 'r') as f:
            return json.load(f)

    def create_sample_rules(self):
        """Create a sample rules file based on the Hazel screenshot"""
        sample_rules = [
            {
                "name": "App Store Receipts",
                "description": "Organizes App Store/iCloud receipts",
                "conditions": {
                    "extension": "pdf",
                    "content_contains": ["receipt", "icloud"]
                },
                "actions": {
                    "rename_pattern": "App Store_{date}_{year}{ext}",
                    "move_to": "Receipts"
                }
            },
            {
                "name": "Bank Statements",
                "description": "Organizes bank statements",
                "conditions": {
                    "extension": "pdf",
                    "content_contains": ["statement", "account"]
                },
                "actions": {
                    "rename_pattern": "Bank_Statement_{date}{ext}",
                    "move_to": "Banking/Statements"
                }
            },
            {
                "name": "Invoices",
                "description": "Organizes invoices",
                "conditions": {
                    "extension": "pdf",
                    "content_contains": ["invoice"]
                },
                "actions": {
                    "rename_pattern": "Invoice_{date}_{year}{ext}",
                    "move_to": "Invoices"
                }
            }
        ]

        with open(self.rules_file, 'w') as f:
            json.dump(sample_rules, f, indent=2)

        print(f"✓ Created sample rules file: {self.rules_file}")

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract all text content from a PDF file

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Extracted text as a string
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""

                # Read text from all pages
                for page in pdf_reader.pages:
                    text += page.extract_text()

                return text
        except Exception as e:
            print(f"⚠️  Error reading PDF {pdf_path}: {e}")
            return ""

    def extract_dates_from_text(self, text: str) -> Tuple[Optional[str], Optional[int]]:
        """
        Extract date and year from PDF text

        Args:
            text: Text content from PDF

        Returns:
            Tuple of (date_string, year)
            Example: ("2025-01-15", 2025)
        """
        # Common date patterns
        date_patterns = [
            r'\b(\d{4})[/-](\d{1,2})[/-](\d{1,2})\b',  # 2025-01-15 or 2025/01/15
            r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b',  # 01/15/2025 or 01-15-2025
            r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* (\d{1,2}),? (\d{4})\b',  # Jan 15, 2025
        ]

        found_date = None
        found_year = None

        # Try to find dates in the text
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Use the first match found
                match = matches[0]

                # Extract year (it's always 4 digits)
                year_match = re.search(r'\b(20\d{2})\b', str(match))
                if year_match:
                    found_year = int(year_match.group(1))
                    # Create a standardized date string
                    found_date = year_match.group(1)
                    break

        # If no specific date found, try to find any year
        if not found_year:
            year_match = re.search(r'\b(20\d{2})\b', text)
            if year_match:
                found_year = int(year_match.group(1))
                found_date = year_match.group(1)

        # If still no year found, use current year
        if not found_year:
            found_year = datetime.now().year
            found_date = str(found_year)

        return found_date, found_year

    def matches_rule(self, pdf_path: str, pdf_text: str, rule: Dict) -> bool:
        """
        Check if a PDF matches the conditions of a rule

        Args:
            pdf_path: Path to PDF file
            pdf_text: Extracted text from PDF
            rule: Rule dictionary to check against

        Returns:
            True if PDF matches all conditions
        """
        conditions = rule.get("conditions", {})

        # Check extension
        if "extension" in conditions:
            ext = Path(pdf_path).suffix[1:].lower()  # Remove the dot
            if ext != conditions["extension"].lower():
                return False

        # Check content contains (case-insensitive)
        if "content_contains" in conditions:
            pdf_text_lower = pdf_text.lower()
            keywords = conditions["content_contains"]

            # All keywords must be present
            for keyword in keywords:
                if keyword.lower() not in pdf_text_lower:
                    return False

        return True

    def apply_rename_pattern(self, original_path: str, pattern: str,
                           date: str, year: int) -> str:
        """
        Apply a rename pattern to create a new filename

        Args:
            original_path: Original PDF path
            pattern: Rename pattern (e.g., "Invoice_{date}_{year}{ext}")
            date: Date string extracted from PDF
            year: Year extracted from PDF

        Returns:
            New filename
        """
        file_path = Path(original_path)

        # Get file creation/modification date
        file_created = datetime.fromtimestamp(os.path.getctime(original_path))

        # Replace pattern placeholders
        new_name = pattern
        new_name = new_name.replace("{date}", date)
        new_name = new_name.replace("{year}", str(year))
        new_name = new_name.replace("{ext}", file_path.suffix)
        new_name = new_name.replace("{date_created}", file_created.strftime("%Y-%m-%d"))
        new_name = new_name.replace("{original_name}", file_path.stem)

        return new_name

    def process_pdf(self, pdf_path: str, source_folder: str, dry_run: bool = False) -> bool:
        """
        Process a single PDF file against all rules

        Args:
            pdf_path: Path to PDF file
            source_folder: Source folder being processed
            dry_run: If True, only show what would happen without actually moving files

        Returns:
            True if PDF was processed, False otherwise
        """
        print(f"\n📄 Processing: {Path(pdf_path).name}")

        # Extract text from PDF
        pdf_text = self.extract_text_from_pdf(pdf_path)
        if not pdf_text:
            print("   ⚠️  Could not extract text from PDF")
            return False

        # Extract date and year from PDF content
        date, year = self.extract_dates_from_text(pdf_text)
        print(f"   📅 Detected date: {date}, year: {year}")

        # Try to match against each rule
        for rule in self.rules:
            if self.matches_rule(pdf_path, pdf_text, rule):
                print(f"   ✓ Matched rule: '{rule['name']}'")

                actions = rule.get("actions", {})

                # Apply renaming
                new_filename = Path(pdf_path).name  # Default: keep original name
                if "rename_pattern" in actions:
                    new_filename = self.apply_rename_pattern(
                        pdf_path,
                        actions["rename_pattern"],
                        date,
                        year
                    )
                    print(f"   📝 New name: {new_filename}")

                # Apply moving
                if "move_to" in actions:
                    dest_folder = Path(source_folder) / actions["move_to"]
                    dest_path = dest_folder / new_filename

                    if dry_run:
                        print(f"   🔄 Would move to: {dest_path}")
                    else:
                        # Create destination folder if it doesn't exist
                        dest_folder.mkdir(parents=True, exist_ok=True)

                        # Check if file already exists
                        if dest_path.exists():
                            print(f"   ⚠️  File already exists at destination: {dest_path}")
                            # Add a number to make it unique
                            counter = 1
                            while dest_path.exists():
                                name_parts = new_filename.rsplit('.', 1)
                                if len(name_parts) == 2:
                                    numbered_name = f"{name_parts[0]}_{counter}.{name_parts[1]}"
                                else:
                                    numbered_name = f"{new_filename}_{counter}"
                                dest_path = dest_folder / numbered_name
                                counter += 1
                            print(f"   📝 Using unique name: {dest_path.name}")

                        # Move the file
                        shutil.move(pdf_path, dest_path)
                        print(f"   ✅ Moved to: {dest_path}")

                return True

        print(f"   ℹ️  No matching rules found")
        return False

    def process_folder(self, folder_path: str, dry_run: bool = False):
        """
        Process all PDF files in a folder

        Args:
            folder_path: Path to folder containing PDFs
            dry_run: If True, show what would happen without actually moving files
        """
        folder = Path(folder_path)

        if not folder.exists():
            print(f"❌ Folder not found: {folder_path}")
            return

        print("=" * 70)
        print("PDF AUTOMATION TOOL")
        print("=" * 70)
        print(f"📁 Processing folder: {folder_path}")
        print(f"📋 Loaded {len(self.rules)} rules")

        if dry_run:
            print("🔍 DRY RUN MODE - No files will be moved")

        # Find all PDF files
        pdf_files = list(folder.glob("*.pdf"))

        if not pdf_files:
            print("\nℹ️  No PDF files found in folder")
            return

        print(f"\n📊 Found {len(pdf_files)} PDF file(s)")

        processed_count = 0
        for pdf_file in pdf_files:
            if self.process_pdf(str(pdf_file), folder_path, dry_run):
                processed_count += 1

        print("\n" + "=" * 70)
        print(f"✅ Processed {processed_count} out of {len(pdf_files)} PDFs")
        print("=" * 70)


def main():
    """Main function to run the PDF automation tool"""
    print("\n🚀 PDF Automation Tool - Smart Alternative to Hazel\n")

    # Initialize the automation tool
    automation = PDFAutomation()

    # Ask user for folder to process
    folder = input("Enter folder path to process (or press Enter for current directory): ").strip()

    if not folder:
        folder = "."

    # Ask if this is a dry run
    dry_run_input = input("\nDo you want to do a dry run first? (y/n): ").strip().lower()
    dry_run = dry_run_input == 'y'

    print()

    # Process the folder
    automation.process_folder(folder, dry_run)

    if dry_run:
        print("\n💡 This was a dry run. Run again without dry run mode to actually move files.")


if __name__ == "__main__":
    main()

"""
File Organizer - Your First Python Automation Script!

This script organizes files in a folder by moving them into subfolders
based on their file type (extension).

For example:
- .jpg and .png files go into an "Images" folder
- .pdf and .docx files go into a "Documents" folder
- etc.
"""

import os
import shutil

def organize_files(folder_path):
    """
    Organizes files in the given folder by their type.

    Args:
        folder_path: The path to the folder you want to organize
    """

    # This dictionary maps file extensions to folder names
    # You can add more categories here!
    file_categories = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.pptx'],
        'Videos': ['.mp4', '.avi', '.mov', '.mkv'],
        'Music': ['.mp3', '.wav', '.flac', '.m4a'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
        'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp']
    }

    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"Error: The folder '{folder_path}' doesn't exist!")
        return

    print(f"Starting to organize files in: {folder_path}")
    print("-" * 50)

    # Counter to track how many files we moved
    files_moved = 0

    # Loop through all items in the folder
    for filename in os.listdir(folder_path):
        # Get the full path of the file
        file_path = os.path.join(folder_path, filename)

        # Skip if it's a folder (we only want to organize files)
        if os.path.isdir(file_path):
            continue

        # Get the file extension (like .jpg, .pdf, etc.)
        _, file_extension = os.path.splitext(filename)
        file_extension = file_extension.lower()  # Make it lowercase for comparison

        # Find which category this file belongs to
        moved = False
        for category, extensions in file_categories.items():
            if file_extension in extensions:
                # Create the category folder if it doesn't exist
                category_path = os.path.join(folder_path, category)
                if not os.path.exists(category_path):
                    os.makedirs(category_path)
                    print(f"Created folder: {category}")

                # Move the file into the category folder
                destination = os.path.join(category_path, filename)

                # Check if file already exists at destination
                if os.path.exists(destination):
                    print(f"⚠️  Skipped '{filename}' (already exists in {category})")
                else:
                    shutil.move(file_path, destination)
                    print(f"✓ Moved '{filename}' → {category}/")
                    files_moved += 1

                moved = True
                break

        # If we didn't find a category, move to "Other"
        if not moved:
            other_path = os.path.join(folder_path, 'Other')
            if not os.path.exists(other_path):
                os.makedirs(other_path)
                print(f"Created folder: Other")

            destination = os.path.join(other_path, filename)
            if not os.path.exists(destination):
                shutil.move(file_path, destination)
                print(f"✓ Moved '{filename}' → Other/")
                files_moved += 1

    print("-" * 50)
    print(f"Done! Organized {files_moved} files.")


# This runs when you execute the script
if __name__ == "__main__":
    print("=" * 50)
    print("FILE ORGANIZER - Python Automation")
    print("=" * 50)
    print()

    # Ask the user which folder to organize
    folder_to_organize = input("Enter the folder path to organize (or press Enter for 'test_folder'): ")

    # If user just pressed Enter, use the test folder
    if folder_to_organize.strip() == "":
        folder_to_organize = "test_folder"

    print()
    organize_files(folder_to_organize)
    print()
    print("All done! Check your folder to see the organized files.")

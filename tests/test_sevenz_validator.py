import sys
import os
import py7zr  # Import py7zr for creating 7z files

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from validators.sevenz_validator import validate_sevenz

def test_validate_sevenz():
    # Create test 7z files
    valid_sevenz = "test_files/valid.7z"
    invalid_sevenz = "test_files/invalid.7z"

    # Create a valid 7z file
    os.makedirs("test_files", exist_ok=True)
    with open("test_files/test_file.txt", "w") as f:
        f.write("Test content")
    with py7zr.SevenZipFile(valid_sevenz, mode='w') as archive:
        archive.writeall("test_files/test_file.txt", arcname="test_file.txt")

    # Create a corrupted 7z file
    with open(valid_sevenz, "rb") as f:
        data = f.read()
    with open(invalid_sevenz, "wb") as f:
        f.write(data[:50])  # Truncate the file to simulate corruption

    # Test valid 7z file
    assert validate_sevenz(valid_sevenz) == True, "Valid 7z file should pass validation."

    # Test invalid 7z file
    assert validate_sevenz(invalid_sevenz) == False, "Invalid 7z file should fail validation."


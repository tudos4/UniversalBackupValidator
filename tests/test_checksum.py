import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from checksum import calculate_checksum, validate_checksum

def test_checksum():
    # Create a small file for testing
    file_path = "test_files/test_file.txt"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure the directory exists
    with open(file_path, "w") as f:
        f.write("This is a test file.")

    # Expected checksum for the file content
    expected_checksum = "3de8f8b0dc94b8c2230fab9ec0ba0506"  # Correct MD5 checksum of "This is a test file."

    # Test checksum calculation
    assert calculate_checksum(file_path, "md5") == expected_checksum, "Checksum calculation failed."

    # Test checksum validation
    assert validate_checksum(file_path, expected_checksum, "md5") == True, "Checksum validation failed."


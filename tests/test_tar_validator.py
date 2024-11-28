import sys
import os
import tarfile  # Import the tarfile module

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from validators.tar_validator import validate_tar

def test_validate_tar():
    # Create test TAR files
    valid_tar = "test_files/valid.tar"
    invalid_tar = "test_files/invalid.tar"

    # Create a valid TAR file
    os.makedirs("test_files", exist_ok=True)
    with tarfile.open(valid_tar, "w") as tar:
        with open("test_files/test_file.txt", "w") as f:
            f.write("Test content")
        tar.add("test_files/test_file.txt", arcname="test_file.txt")

    # Create a corrupted TAR file
    with open(valid_tar, "rb") as f:
        data = f.read()
    with open(invalid_tar, "wb") as f:
        f.write(data[:50])  # Truncate the file to simulate corruption

    # Test valid TAR file
    assert validate_tar(valid_tar) == True, "Valid TAR file should pass validation."

    # Test invalid TAR file
    assert validate_tar(invalid_tar) == False, "Invalid TAR file should fail validation."


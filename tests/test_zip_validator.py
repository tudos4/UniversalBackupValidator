from src.validators.zip_validator import validate_zip

def test_validate_zip():
    valid_zip = "test_files/valid.zip"  # Path to a valid ZIP file
    invalid_zip = "test_files/invalid.zip"  # Path to a corrupted ZIP file

    # Test valid ZIP
    assert validate_zip(valid_zip) == True, "The valid ZIP file should pass validation."

    # Test invalid ZIP
    assert validate_zip(invalid_zip) == False, "The invalid ZIP file should fail validation."


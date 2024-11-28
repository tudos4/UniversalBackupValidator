import zipfile

def validate_zip(file_path):
    """
    Validates the integrity of a ZIP file by checking its structure and contents.

    Args:
        file_path (str): The path to the ZIP file.

    Returns:
        bool: True if the ZIP file is valid, False otherwise.
    """
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            # Check if the archive has corrupt files
            corrupt_file = zip_ref.testzip()
            if corrupt_file is not None:
                print(f"Validation Failed: Corrupt file found: {corrupt_file}")
                return False

            # Attempt to read and extract all files
            for file_info in zip_ref.infolist():
                try:
                    zip_ref.read(file_info.filename)
                except Exception as e:
                    print(f"Validation Failed: Error reading file '{file_info.filename}': {e}")
                    return False

            print(f"Validation Passed: {file_path} is valid.")
            return True
    except zipfile.BadZipFile:
        print(f"Validation Failed: {file_path} is not a valid ZIP file.")
        return False
    except Exception as e:
        print(f"Validation Failed: Unexpected error occurred: {e}")
        return False


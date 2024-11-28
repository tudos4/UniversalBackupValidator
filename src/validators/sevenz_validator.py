import py7zr

def validate_sevenz(file_path):
    """
    Validates the integrity of a 7z file.

    Args:
        file_path (str): The path to the 7z file.

    Returns:
        bool: True if the 7z file is valid, False otherwise.
    """
    try:
        with py7zr.SevenZipFile(file_path, mode='r') as archive:
            # Test the archive's integrity by listing all files
            archive.list()
        print(f"Validation Passed: {file_path} is a valid 7z file.")
        return True
    except py7zr.exceptions.Bad7zFile as e:
        print(f"Validation Failed: {file_path} is not a valid 7z file - {e}")
        return False
    except FileNotFoundError:
        print(f"Validation Failed: File '{file_path}' not found.")
        return False
    except Exception as e:
        print(f"Validation Failed: Unexpected error occurred: {e}")
        return False


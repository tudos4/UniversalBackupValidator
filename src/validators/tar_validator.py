import tarfile

def validate_tar(file_path):
    """
    Validates the integrity of a TAR file.

    Args:
        file_path (str): The path to the TAR file.

    Returns:
        bool: True if the TAR file is valid, False otherwise.
    """
    try:
        with tarfile.open(file_path, 'r') as tar:
            tar.getmembers()  # Attempt to read all members
        print(f"Validation Passed: {file_path} is a valid TAR file.")
        return True
    except tarfile.ReadError as e:
        print(f"Validation Failed: {file_path} is not a valid TAR file - {str(e)}")
        return False
    except FileNotFoundError:
        print(f"Validation Failed: File '{file_path}' not found.")
        return False
    except Exception as e:
        print(f"Validation Failed: Unexpected error occurred: {e}")
        return False


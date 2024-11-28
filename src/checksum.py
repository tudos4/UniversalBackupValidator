import hashlib

def calculate_checksum(file_path, algorithm="sha256"):
    """
    Calculate the checksum of a file.

    Args:
        file_path (str): Path to the file.
        algorithm (str): Hashing algorithm ('md5', 'sha256').

    Returns:
        str: The checksum as a hexadecimal string.
    """
    hasher = hashlib.new(algorithm)
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error: Unable to calculate checksum - {e}")
        return None

def validate_checksum(file_path, expected_checksum, algorithm="sha256"):
    """
    Validate a file's checksum against an expected value.

    Args:
        file_path (str): Path to the file.
        expected_checksum (str): Expected checksum value.
        algorithm (str): Hashing algorithm ('md5', 'sha256').

    Returns:
        bool: True if the checksum matches, False otherwise.
    """
    calculated_checksum = calculate_checksum(file_path, algorithm)
    return calculated_checksum == expected_checksum


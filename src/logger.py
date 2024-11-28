import os
import json
from datetime import datetime
from threading import Lock

# Global lock for log rotation
log_rotation_lock = Lock()

def rotate_logs(log_file, max_logs=5):
    """
    Rotates log files to maintain a maximum number of logs.

    Args:
        log_file (str): The base log file name (e.g., 'validation_log').
        max_logs (int): Maximum number of log files to keep.
    """
    log_dir = os.path.dirname(log_file)
    log_base = os.path.basename(log_file).split(".")[0]

    # Ensure thread safety
    with log_rotation_lock:
        # Gather all rotated logs
        rotated_logs = [
            f for f in os.listdir(log_dir)
            if f.startswith(log_base) and f.endswith(".json")
        ]
        rotated_logs.sort()

        # Remove oldest logs if the limit is exceeded
        while len(rotated_logs) >= max_logs:
            oldest_log = os.path.join(log_dir, rotated_logs.pop(0))
            try:
                os.remove(oldest_log)
                print(f"Rotated out old log file: {oldest_log}")
            except FileNotFoundError:
                print(f"Warning: Log file already removed: {oldest_log}")

def log_validation_result(file_path, validation_results, output_dir="logs", max_logs=5):
    """
    Logs the validation results to a JSON file and manages log rotation.

    Args:
        file_path (str): The path to the file being validated.
        validation_results (dict): A dictionary of validation results.
        output_dir (str): Directory where logs will be saved.
        max_logs (int): Maximum number of log files to keep.

    Returns:
        str: The path to the current log file.
    """
    os.makedirs(output_dir, exist_ok=True)  # Ensure the logs directory exists
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
    log_file = os.path.join(output_dir, f"validation_log_{timestamp}.json")

    # Prepare the log entry
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "file": file_path,
        "results": validation_results,
    }

    # Write to the new log file
    with open(log_file, "w") as f:
        json.dump([log_entry], f, indent=4)

    print(f"Validation results logged to {log_file}")

    # Rotate logs to maintain max_logs count
    rotate_logs(log_file, max_logs)

    return log_file


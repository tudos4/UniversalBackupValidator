import argparse
import os
import json
import csv
from colorama import Fore, Style, init
from validators.zip_validator import validate_zip
from validators.tar_validator import validate_tar
from validators.sevenz_validator import validate_sevenz
from checksum import validate_checksum
from logger import log_validation_result
from concurrent.futures import ThreadPoolExecutor

SUPPORTED_EXTENSIONS = ['.zip', '.tar', '.7z']

# Initialize colorama
init(autoreset=True)

def validate_file(file_path, checksum=None, algorithm="sha256"):
    """
    Validates a single file and returns the results.

    Args:
        file_path (str): The path to the file.
        checksum (str, optional): Expected checksum value.
        algorithm (str, optional): Checksum algorithm.

    Returns:
        dict: Validation results.
    """
    results = {"file": file_path}

    if file_path.endswith('.zip'):
        results["zip_validation"] = validate_zip(file_path)
    elif file_path.endswith('.tar'):
        results["tar_validation"] = validate_tar(file_path)
    elif file_path.endswith('.7z'):
        results["7z_validation"] = validate_sevenz(file_path)
    else:
        print(Fore.YELLOW + f"Unsupported File Format: {file_path}")
        results["validation_status"] = "Unsupported format"
        return results

    if checksum:
        results["checksum_validation"] = validate_checksum(file_path, checksum, algorithm)
        results["checksum_algorithm"] = algorithm

    return results

def load_config(config_path):
    """
    Loads configuration from a JSON file.

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        dict: Configuration options as a dictionary.
    """
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(Fore.RED + f"Error: Configuration file not found at {config_path}.")
    except json.JSONDecodeError as e:
        print(Fore.RED + f"Error: Failed to parse configuration file {config_path}: {e}")
    return {}

def write_csv_report(report_path, results):
    """
    Writes the consolidated validation results to a CSV file.

    Args:
        report_path (str): Path to the report file.
        results (list): List of validation results.
    """
    try:
        with open(report_path, "w", newline="") as f:
            writer = csv.writer(f)
            headers = ["File", "Validation Type", "Result", "Details"]
            writer.writerow(headers)

            for result in results:
                file_path = result.get("file", "Unknown")
                for key, value in result.items():
                    if key.endswith("_validation"):
                        writer.writerow([file_path, key, value, ""])
                    elif key == "validation_status":
                        writer.writerow([file_path, "Overall Status", value, ""])

        print(Fore.GREEN + f"CSV report saved to {report_path}")
    except Exception as e:
        print(Fore.RED + f"Error writing CSV report to {report_path}: {e}")

def write_html_report(report_path, results):
    """
    Writes the consolidated validation results to an HTML file.

    Args:
        report_path (str): Path to the report file.
        results (list): List of validation results.
    """
    try:
        with open(report_path, "w") as f:
            f.write("<html><body><h1>Validation Report</h1><table border='1'>")
            f.write("<tr><th>File</th><th>Validation Type</th><th>Result</th><th>Details</th></tr>")

            for result in results:
                file_path = result.get("file", "Unknown")
                for key, value in result.items():
                    if key.endswith("_validation"):
                        f.write(f"<tr><td>{file_path}</td><td>{key}</td><td>{value}</td><td></td></tr>")
                    elif key == "validation_status":
                        f.write(f"<tr><td>{file_path}</td><td>Overall Status</td><td>{value}</td><td></td></tr>")

            f.write("</table></body></html>")
        print(Fore.GREEN + f"HTML report saved to {report_path}")
    except Exception as e:
        print(Fore.RED + f"Error writing HTML report to {report_path}: {e}")

def write_report(report_path, results, format="json"):
    """
    Writes the consolidated validation results to a report file.

    Args:
        report_path (str): Path to the report file.
        results (list): List of validation results.
        format (str): Format of the report (json, csv, html).
    """
    if format == "json":
        try:
            with open(report_path, "w") as f:
                json.dump(results, f, indent=4)
            print(Fore.GREEN + f"JSON report saved to {report_path}")
        except Exception as e:
            print(Fore.RED + f"Error writing JSON report to {report_path}: {e}")
    elif format == "csv":
        write_csv_report(report_path, results)
    elif format == "html":
        write_html_report(report_path, results)
    else:
        print(Fore.RED + f"Unsupported report format: {format}")

def validate_file_thread(file_path, checksum, algorithm, log_directory, max_logs, consolidated_results):
    """
    Threaded function to validate a file.

    Args:
        file_path (str): Path to the file.
        checksum (str): Expected checksum value.
        algorithm (str): Checksum algorithm.
        log_directory (str): Directory for logs.
        max_logs (int): Maximum logs to retain.
        consolidated_results (list): Shared list to store validation results.
    """
    if any(file_path.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
        print(Fore.CYAN + f"Validating: {file_path}")
        validation_results = validate_file(file_path, checksum, algorithm)
        log_validation_result(file_path, validation_results, output_dir=log_directory, max_logs=max_logs)
        consolidated_results.append(validation_results)
    else:
        print(Fore.YELLOW + f"Warning: Unsupported file type skipped: {file_path}")

def main():
    parser = argparse.ArgumentParser(description="Universal Backup Validator")
    parser.add_argument('--file', type=str, help="Path to a file to validate.")
    parser.add_argument('--directory', type=str, help="Path to a directory containing files to validate.")
    parser.add_argument('--checksum', type=str, help="Expected checksum value for validation.")
    parser.add_argument('--algorithm', type=str, default="sha256", help="Checksum algorithm (default: sha256).")
    parser.add_argument('--max-logs', type=int, default=5, help="Maximum number of logs to retain.")
    parser.add_argument('--log-directory', type=str, default="logs", help="Directory to store logs.")
    parser.add_argument('--config', type=str, help="Path to a configuration JSON file.")
    parser.add_argument('--report', type=str, help="Path to save the consolidated validation report.")
    parser.add_argument('--report-format', type=str, default="json", choices=["json", "csv", "html"],
                        help="Format of the report (json, csv, html). Default is json.")
    args = parser.parse_args()

    # Load configuration from file
    config = {}
    if args.config:
        config = load_config(args.config)

    # Determine settings, prioritizing CLI arguments over config
    max_logs = args.max_logs if args.max_logs is not None else config.get("max_logs", 5)
    algorithm = args.algorithm if args.algorithm is not None else config.get("default_algorithm", "sha256")
    log_directory = args.log_directory if args.log_directory else config.get("log_directory", "logs")
    report_path = args.report if args.report else config.get("report_path", "validation_report.json")

    consolidated_results = []

    if args.file:
        print(Fore.CYAN + f"Validating file: {args.file}")
        validation_results = validate_file(args.file, args.checksum, algorithm)
        log_validation_result(args.file, validation_results, output_dir=log_directory, max_logs=max_logs)

        if validation_results.get("validation_status") == "Unsupported format":
            print(Fore.YELLOW + f"Warning: {args.file} has an unsupported format.")
        elif all(validation_results.get(key, True) for key in validation_results if key.endswith("_validation")):
            print(Fore.GREEN + f"Validation Passed: {args.file}")
        else:
            print(Fore.RED + f"Validation Failed: {args.file}")

        consolidated_results.append(validation_results)

    elif args.directory:
        print(Fore.CYAN + f"Validating all supported files in directory: {args.directory}")
        with ThreadPoolExecutor() as executor:
            futures = []
            for root, _, files in os.walk(args.directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    futures.append(executor.submit(validate_file_thread, file_path, args.checksum, algorithm, log_directory, max_logs, consolidated_results))
            for future in futures:
                future.result()

    if consolidated_results:
        write_report(report_path, consolidated_results, format=args.report_format)

if __name__ == "__main__":
    main()


# Universal Backup Validator

Universal Backup Validator is an open-source tool designed to ensure the integrity of your backup files. It validates `.zip`, `.tar`, and `.7z` files, performs checksum verification, and generates comprehensive reports in multiple formats.

---

## **Features**
- Validate the integrity of `.zip`, `.tar`, and `.7z` files.
- Checksum verification using popular algorithms like `sha256` and `md5`.
- Multi-threaded directory validation for improved performance.
- Generate reports in multiple formats: JSON, CSV, and HTML.
- Configurable log rotation to manage log storage.

---

## **Installation**

### Prerequisites
- Python 3.7 or later.

### Clone the Repository
```bash
git clone https://github.com/tudos4/UniversalBackupValidator.git
cd UniversalBackupValidator

Set Up a Virtual Environment

python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
pip install -r requirements.txt

Usage
Validate a Single File

To validate a single .zip file:

python src/cli.py --file test_files/valid.zip --checksum <checksum> --algorithm sha256

Validate Files in a Directory

To validate all supported files in a directory:

python src/cli.py --directory test_files_batch --report validation_report.json --report-format json

CLI Options

--file            Path to a file to validate.
--directory       Path to a directory containing files to validate.
--checksum        Expected checksum value for validation.
--algorithm       Checksum algorithm (default: sha256).
--report          Path to save the consolidated report.
--report-format   Format of the report (json, csv, html). Default is json.
--config          Path to a configuration JSON file.
--max-logs        Maximum number of logs to retain (default: 5).
--log-directory   Directory to store logs.

Examples
Validate a .tar file with a checksum:

python src/cli.py --file test_files/valid.tar --checksum <checksum_value> --algorithm md5

Generate a CSV Report for a Directory:

python src/cli.py --directory test_files_batch --report validation_report.csv --report-format csv

Generate an HTML Report:

python src/cli.py --directory test_files_batch --report validation_report.html --report-format html

Contribution

We welcome contributions to improve Universal Backup Validator! Follow these steps to contribute:

    Fork the Repository:
        Go to the GitHub repository.
        Click the "Fork" button.

    Create a New Branch:

git checkout -b my-feature-branch

Make Your Changes:

    Add your feature or fix bugs.

Commit Your Changes:

git commit -m "Describe your changes"

Push the Changes:

    git push origin my-feature-branch

    Open a Pull Request:
        Go to the original repository on GitHub.
        Open a pull request describing your changes.

License

This project is licensed under the MIT License. See the LICENSE file for more details.
Acknowledgments

    Developed by tudos4.
    Inspired by the need for robust backup file validation.
    Powered by Python and the colorama library for enhanced CLI output.


---

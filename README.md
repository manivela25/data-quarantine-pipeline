# Data Quality & Quarantine Pipeline

![CI Pipeline](https://github.com/manivela25/data-quarantine-pipeline/actions/workflows/ci.yml/badge.svg)

A lightweight, robust data validation and ETL pipeline built with Python. It processes raw CSV records, segregates clean
data from invalid records, tags errors with specific violation reasons into a quarantine dataset, and outputs execution
summary metrics.

---

## 📌 Architecture Overview

```text
[ data/raw/users.csv ]
          │
          ▼
   [ src/pipeline.py ] 
   (Stream read via DictReader)
          │
          ▼
  [ Validation Layer ] ─── (src/validator.py: Custom Exceptions + Regex)
     ├── validate_email()
     └── validate_phone()
          │
     ┌────┴───────────────────────────┐
     │ (Valid)                        │ (ValidationError)
     ▼                                ▼
[ data/clean/clean_users.csv ]   [ data/quarantine/quarantine_users.csv ]
                                 (Includes 'error_reason' column)

✨ Features
Decoupled Architecture: Clean separation of business logic (src/validator.py), ETL execution (src/pipeline.py), and test automation (tests/).

Data Quarantine Pattern: Faulty rows are never discarded silently; they are stored alongside actionable root-cause descriptions.

Custom Exception Hierarchy: Domain-specific exceptions (ValidationError, InvalidEmailError, InvalidPhoneError) for precise error capture and reporting.

Domain Business Rules: Implements strict regex-based Turkish mobile phone validation (+90 5xx, 05xx, 5xx), disallowing landline prefixes and irregular lengths.

Real-Time Reporting: Console metrics summarizing throughput, clean rates, and categorical error breakdowns via collections.Counter.

Zero Runtime Dependencies: Built strictly using Python's standard library (pathlib, csv, re, collections, unittest).

📁 Project Structure
Plaintext
data-quarantine-pipeline/
├── data/
│   ├── raw/                 # Input dataset (users.csv)
│   ├── clean/               # Validated clean records
│   └── quarantine/          # Rejected records with error reasons
├── src/
│   ├── __init__.py
│   ├── validator.py         # Validation logic & custom exceptions
│   └── pipeline.py          # ETL workflow & metrics reporting
├── tests/
│   ├── __init__.py
│   └── test_validator.py    # Unit tests for validation logic
├── .gitignore
└── README.md
🚀 Quick Start & Reproduction
Prerequisites
Python 3.10+

Git

1. Clone the Repository
Bash
git clone [https://github.com/USER_NAME/data-quarantine-pipeline.git](https://github.com/USER_NAME/data-quarantine-pipeline.git)
cd data-quarantine-pipeline
(Replace USER_NAME with your actual GitHub username)

2. Run Automated Unit Tests
Verify regex validation rules, exception handling, and edge cases before running the pipeline:

Bash
python3 -m unittest discover tests
Expected output:

Plaintext
....
----------------------------------------------------------------------
Ran 4 tests in 0.001s

OK
3. Execute the Pipeline
Process the raw data and generate the output datasets:

Bash
python3 -m src.pipeline
Sample console output:

Plaintext
========================================
       PIPELINE EXECUTION REPORT       
========================================
Total Rows Processed : 6
Clean Records        : 2 (33.3%)
Quarantined Records  : 4

Quarantine Reasons Breakdown:
  - Invalid email format: gecersiz-email: 1
  - Invalid phone number: 02129998877: 1
  - Email address cannot be empty.: 1
  - Invalid phone number: 12345: 1
========================================

Pipeline executed successfully!
4. Inspect Generated Artifacts
Once executed, check the generated output CSVs:

Clean data: data/clean/clean_users.csv

Quarantined data: data/quarantine/quarantine_users.csv



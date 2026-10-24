# Data Quality & Quarantine Pipeline

A lightweight, robust data validation and ETL pipeline built with Python. It processes raw CSV records, segregates clean data from invalid records, tags errors with specific violation reasons into a quarantine dataset, and outputs execution summary metrics.

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

Data Quarantine Pattern: Faulty rows are never discarded silently; they are saved alongside actionable root-cause descriptions.

Custom Exceptions: Domain-specific hierarchy (ValidationError, InvalidEmailError, InvalidPhoneError) for precise error capture.

Domain Business Rules: Includes strict regex-based Turkish mobile phone validation (+90 5xx, 05xx, 5xx), disallowing landline prefixes and irregular lengths.

Metrics & Reporting: Real-time console metrics summarizing throughput, clean rates, and categorical error breakdowns via collections.Counter.

Zero Third-Party Runtime Dependencies: Implemented entirely using Python standard libraries (pathlib, csv, re, collections, unittest).

data-quarantine-pipeline/
├── data/
│   ├── raw/                 # Input datasets
│   ├── clean/               # Validated records
│   └── quarantine/          # Rejected records with error reasons
├── src/
│   ├── __init__.py
│   ├── validator.py         # Validation rules & custom exceptions
│   └── pipeline.py          # ETL workflow & metrics reporting
├── tests/
│   ├── __init__.py
│   └── test_validator.py    # Unit tests for validation logic
├── .gitignore
└── README.md


🚀 Getting Started
Prerequisites
Python 3.10+

Execution
To run the pipeline and generate clean/quarantined datasets:

python3 -m src.pipeline


Sample output:

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

🧪 Running Unit Tests
Automated test suites ensure regex coverage, edge-case validation, and boundary conditions:

python3 -m unittest discover tests

import csv
from collections import Counter
from pathlib import Path

from .validator import validate_email, validate_phone, ValidationError


def process_pipeline():
    base_dir = Path(__file__).resolve().parent.parent

    raw_file = base_dir / "data" / "raw" / "users.csv"
    clean_file = base_dir / "data" / "clean" / "clean_users.csv"
    quarantine_file = base_dir / "data" / "quarantine" / "quarantine_users.csv"

    clean_file.parent.mkdir(parents=True, exist_ok=True)
    quarantine_file.parent.mkdir(parents=True, exist_ok=True)

    clean_records = []
    quarantine_records = []

    with open(raw_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = row.get("name", "").strip()
            email = row.get("email", "").strip()
            phone = row.get("phone", "").strip()
            try:
                validate_email(email)
                validate_phone(phone)
                clean_records.append({
                    "name": name,
                    "email": email,
                    "phone": phone
                })
            except ValidationError as error:
                quarantine_records.append({
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "error_reason": str(error)
                })
    with open(clean_file, mode="w", encoding="utf-8", newline="") as file:
        fieldnames = ["name", "email", "phone"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(clean_records)

    with open(quarantine_file, mode="w", encoding="utf-8", newline="") as file:
        fieldnames = ["name", "email", "phone", "error_reason"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(quarantine_records)
    total_processed = len(clean_records) + len(quarantine_records)
    success_rate = (len(clean_records) / total_processed * 100) if total_processed > 0 else 0

    error_counts = Counter(row["error_reason"] for row in quarantine_records)

    print("\n" + "=" * 40)
    print("       PIPELINE EXECUTION REPORT       ")
    print("=" * 40)
    print(f"Total Rows Processed : {total_processed}")
    print(f"Clean Records        : {len(clean_records)} ({success_rate:.1f}%)")
    print(f"Quarantined Records  : {len(quarantine_records)}")

    if error_counts:
        print("\nQuarantine Reasons Breakdown:")
        for reason, count in error_counts.items():
            print(f"  - {reason}: {count} ")
    print("=" * 40 + "\n")


if __name__ == "__main__":
    process_pipeline()
    print("Pipeline executed successfully!")

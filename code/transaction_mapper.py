import sys
import csv
from decimal import Decimal, InvalidOperation

for line in sys.stdin:

    try:
        row = next(csv.reader([line.strip()]))

        # Skip empty or incomplete records
        if len(row) < 6:
            continue

        # Skip CSV header
        if row[0].strip().lstrip('\ufeff').lower() == "transaction id":
            continue

        # Extract required fields
        customer_id = row[1].strip()
        quantity = int(row[3].strip())
        unit_price = Decimal(row[4].strip())
        status = row[5].strip().lower()

        # Validate data
        if not customer_id or quantity < 0 or unit_price < 0:
            continue

        # Calculate transaction amount
        amount = quantity * unit_price

        # Calculate transaction statistics
        success_count = 1 if status in ["success", "successful"] else 0

        failed_count = 1 if status in ["failed", "failure"] else 0

        high_value_count = 1 if amount >= Decimal("50000") else 0

        successful_amount = amount if success_count == 1 else Decimal("0")

        # Emit customer ID as key and statistics as value
        print(
            f"{customer_id}\t"
            f"1,{amount},{success_count},"
            f"{failed_count},{high_value_count},"
            f"{successful_amount}"
        )

    except (ValueError, InvalidOperation, StopIteration, IndexError):
        # Skip malformed records
        continue

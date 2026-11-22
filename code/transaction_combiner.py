import sys
from decimal import Decimal, InvalidOperation

current_customer = None

# Initialize aggregation variables
transactions = 0
total_amount = Decimal("0")
success_count = 0
failed_count = 0
high_value_count = 0
successful_amount = Decimal("0")


for line in sys.stdin:

    try:
        # Separate key and value
        customer_id, values = line.strip().split("\t", 1)

        # Extract statistics
        t, amount, success, failed, high, success_amt = values.split(",")

        t = int(t)
        amount = Decimal(amount)
        success = int(success)
        failed = int(failed)
        high = int(high)
        success_amt = Decimal(success_amt)

        # Validate statistics
        if min(t, success, failed, high) < 0:
            continue

    except (ValueError, InvalidOperation):
        continue

    # Check whether the customer is the same
    if current_customer == customer_id:

        # Add statistics
        transactions += t
        total_amount += amount
        success_count += success
        failed_count += failed
        high_value_count += high
        successful_amount += success_amt

    else:

        # Emit previous customer's aggregated values
        if current_customer is not None:

            print(
                f"{current_customer}\t"
                f"{transactions},{total_amount},"
                f"{success_count},{failed_count},"
                f"{high_value_count},{successful_amount}"
            )

        # Initialize new customer
        current_customer = customer_id

        transactions = t
        total_amount = amount
        success_count = success
        failed_count = failed
        high_value_count = high
        successful_amount = success_amt


# Emit the last customer's values
if current_customer is not None:

    print(
        f"{current_customer}\t"
        f"{transactions},{total_amount},"
        f"{success_count},{failed_count},"
        f"{high_value_count},{successful_amount}"
    )

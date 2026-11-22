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

grand_transaction = 0
grand_amount = Decimal("0")
grand_success = 0
grand_failed = 0
grand_high_value = 0
grand_successful_amount = Decimal("0")

def print_result(customer_id):

    # Customer classification
    if successful_amount >= Decimal("100000") and success_count >= 4:

        classification = "PREMIUM_FREQUENT"

    elif successful_amount >= Decimal("100000"):

        classification = "PREMIUM"

    elif success_count >= 4:

        classification = "FREQUENT"

    else:

        classification = "NORMAL"

    # Print customer-wise result
    print(
        f"Customer: {customer_id} | "
        f"Successful Transaction: {success_count} | "
        f"Successful Amount: Rs. {successful_amount} | "
        f"Classification: {classification}"
        )


for line in sys.stdin:

    try:
        # Separate customer ID and statistics
        customer_id, values = line.strip().split("\t", 1)

        # Extract values
        t, amount, success, failed, high, success_amt = values.split(",")

        t = int(t)
        amount = Decimal(amount)
        success = int(success)
        failed = int(failed)
        high = int(high)
        success_amt = Decimal(success_amt)

        if not customer_id:
            continue
        if min(t, success, failed, high) < 0:
            continue

    except (ValueError, InvalidOperation):
        continue

    grand_transaction += t
    grand_amount += amount
    grand_success += success
    grand_failed += failed
    grand_high_value += high
    grand_successful_amount += success_amt


    # Check whether the customer is the same
    if current_customer == customer_id:

        # Aggregate statistics
        transactions += t
        total_amount += amount
        success_count += success
        failed_count += failed
        high_value_count += high
        successful_amount += success_amt

    else:

        # Print previous customer's result
        if current_customer is not None:

            print_result(current_customer)

        # Initialize new customer
        current_customer = customer_id

        transactions = t
        total_amount = amount
        success_count = success
        failed_count = failed
        high_value_count = high
        successful_amount = success_amt


# Print the last customer's result
if current_customer is not None:

    print_result(current_customer)
    
print("\n===============OVERALL TRANSACTION SUMMARY===============")
print(f"Failed Transaction: {grand_failed}")
print(f"High value Transaction: {grand_high_value}")
print(f"Successful Purchase Amount: Rs. {grand_successful_amount}")
print(f"Successful Transaction {grand_success}")
print(f"Total Purchase Amount: Rs. {grand_amount}")
print(f"Total Transaction {grand_transaction}")
print("============================================================")

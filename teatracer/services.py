from decimal import Decimal

def calculate_transaction_total_cost(transaction):
    
    if transaction.quantity and transaction.unit_price:
        transaction.total_cost = (
            Decimal(transaction.quantity) * Decimal(transaction.unit_price)
        )
    else:
        transaction.total_cost = None

    transaction.save(update_fields=["total_cost"])
    return transaction

from decimal import Decimal

def calculate_total_cost(quantity, unit_price):
    if quantity is None or unit_price is None:
        return None
    return quantity * unit_price

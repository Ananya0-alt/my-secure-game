from collections import namedtuple
from decimal import Decimal

Order = namedtuple('Order', 'id, items')
Item = namedtuple('Item', 'type, description, amount, quantity')

def validorder(order: Order):
    balance = Decimal('0')
    try:
        for item in order.items:
            # 1. Validate item type
            if item.type not in ('payment', 'product'):
                return "Invalid item type: %s" % item.type

            # 2. Validate quantity - must be int, not bool, not float
            if type(item.quantity) != int:
                return "Invalid quantity"
            if item.quantity < 1 or item.quantity > 100:
                return "Invalid quantity"

            # 3. Validate amount - must be convertible to Decimal, not bool
            try:
                if isinstance(item.amount, bool):
                    raise ValueError()
                amt = Decimal(str(item.amount))
            except:
                return "Invalid amount"

            if amt < 0 or amt > Decimal('100000'):
                return "Invalid amount"

            # 4. Calculate with Decimal (fixes float bug like 0.1+0.2 != 0.3)
            if item.type == 'payment':
                balance += amt
            else:
                balance -= amt * item.quantity

            # 5. Check total exceeded - order independent
            if abs(balance) > Decimal('1000000'):
                return "Total amount payable for an order exceeded"

    except Exception:
        return "Invalid order"

    if balance != 0:
        return "Order ID: %s - Payment imbalance: $%0.2f" % (order.id, float(balance))
    else:
        return "Order ID: %s - Full payment received!" % order.id
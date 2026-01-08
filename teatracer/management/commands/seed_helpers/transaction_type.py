from teatracer.models import TransactionType

def create_or_link_transaction_type(name, stdout):
    transaction_type, created = TransactionType.objects.get_or_create(name=name)
    if created:
        stdout.write(f'TransactionType "{name}" created')
    return transaction_type


def create_transaction_types(transaction_types_list, stdout):
    return {name: create_or_link_transaction_type(name, stdout) for name in transaction_types_list}

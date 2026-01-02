from teatracer.models import Currency

def create_or_link_currency(name, ratio, stdout):
    currency, created = Currency.objects.get_or_create(name=name, ratio=ratio)
    if created:
        stdout.write(f'MovementType "{name}" created')
    return currency


def create_currencies(providers_dict, stdout):
    return {name: create_or_link_currency(name, ratio, stdout) for name, ratio in providers_dict.items()}

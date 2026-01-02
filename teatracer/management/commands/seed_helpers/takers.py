from teatracer.models import Taker

def create_or_link_taker(name, stdout):
    taker, created = Taker.objects.get_or_create(name=name)
    if created:
        stdout.write(f'Taker "{name}" created')
    return taker


def create_takers(takers_list, stdout):
    return {name: create_or_link_taker(name, stdout) for name in takers_list}

from teatracer.models import Provider

def create_or_link_provider(name, stdout):
    provider, created = Provider.objects.get_or_create(name=name)
    if created:
        stdout.write(f'Provider "{name}" created')
    return provider


def create_providers(providers_list, stdout):
    return {name: create_or_link_provider(name, stdout) for name in providers_list}

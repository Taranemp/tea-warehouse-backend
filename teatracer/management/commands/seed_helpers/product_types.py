from teatracer.models import ProductType

def create_or_link_product_type(name, stdout):
    product_type, created = ProductType.objects.get_or_create(name=name)
    if created:
        stdout.write(f'ProductType "{name}" created')
    return product_type


def create_product_types(product_types_list, stdout):
    return {name: create_or_link_product_type(name, stdout) for name in product_types_list}

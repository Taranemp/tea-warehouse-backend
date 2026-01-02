from teatracer.models import Product

def create_or_link_product(name, sku, product_type, stdout):
    product, created = Product.objects.get_or_create(
        name=name,
        sku=sku,
        product_type=product_type,
        defaults={"is_final": False}
    )
    if created:
        stdout.write(f'Product "{name}" created')
    return product


def create_products(product_types, stdout):
    return {
        "Leaf G1": create_or_link_product(
            name= "Premium", sku= "G1", product_type=product_types["black tea"], stdout=stdout
        ),
        "Leaf G2": create_or_link_product(
            name= "First Flush", sku= "G2", product_type=product_types["black tea"], stdout=stdout
        ),
        "Leaf G3": create_or_link_product(
            name= "Broken Tea", sku= "G3", product_type=product_types["black tea"], stdout=stdout
        ),
        "Processed leaf": create_or_link_product(
            name= "Long Leaf", sku= "Proc", product_type=product_types["black tea"], stdout=stdout
        ),
        "Sort A": create_or_link_product(
            name= "Green Tea A", sku= "SA", product_type=product_types["black tea"], stdout=stdout
        ),
        "Sort B": create_or_link_product(
            name= "Green Tea A", sku= "SBG", product_type=product_types["green tea"], stdout=stdout
        ),
        "Sort C": create_or_link_product(
            name= "Green Tea A", sku= "SC", product_type=product_types["black tea"], stdout=stdout
        ),
        "Mix Tea AB": create_or_link_product(
            name= "Green Tea A", sku= "MAB", product_type=product_types["black tea"], stdout=stdout
        ),
        "Mix Tea CD": create_or_link_product(
            name= "Green Tea A", sku= "MCD", product_type=product_types["black tea"], stdout=stdout
        ),
        "Mix Tea FE": create_or_link_product(
            name= "Green Tea A", sku= "MFEG", product_type=product_types["green tea"], stdout=stdout
        ),
    }

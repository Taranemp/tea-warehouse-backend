from teatracer.models import MovementType

def create_or_link_movement_type(name, stdout):
    movement, created = MovementType.objects.get_or_create(name=name)
    if created:
        stdout.write(f'MovementType "{name}" created')
    return movement


def create_movement_types(movement_types_list, stdout):
    names = movement_types_list
    return {name: create_or_link_movement_type(name, stdout) for name in names}

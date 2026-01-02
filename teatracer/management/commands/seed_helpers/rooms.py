from teatracer.models import Room

def create_or_link_room(name, stdout):
    room, created = Room.objects.get_or_create(name=name)
    if created:
        stdout.write(f'Room "{name}" created')
    return room


def create_rooms(rooms_list, stdout):
    return {name: create_or_link_room(name, stdout) for name in rooms_list}

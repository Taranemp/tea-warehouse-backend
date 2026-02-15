from django.contrib.auth import get_user_model

User = get_user_model()

def create_super_user(stdout):
    username = "admin"
    password = "admin"
    email = "admin@admin.com"

    if User.objects.filter(username=username).exists():
        stdout.write("Superuser exists")
        return

    User.objects.create_superuser(
        username=username,
        password=password,
        first_name='John',
        last_name='Due',
        phone='09993334444',
        email=email,
    )
    stdout.write("Superuser created")




# TODO: Delete later
# ------------------------------------------------
# - [ ] username: accountant01, supervisor01, inventory_man_room_01, inventory_man_room_02
# - [ ] password set for all 'Admin@123'
# - [ ] create three group: RoomManagersGroup, AccountantsGroup, SupervisorGroup

def run_all_users_groups_permissions():
    create_accountants()
    create_supervisor()
    create_inventory_man()
    create_user_groups()
    


def create_accountants():
    pass

def create_supervisor():
    pass

def create_inventory_man():
    pass

def create_user_groups():
    pass
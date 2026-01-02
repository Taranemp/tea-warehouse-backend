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

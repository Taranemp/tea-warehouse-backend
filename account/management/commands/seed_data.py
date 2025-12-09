from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Seed initial data such as default superuser"

    def handle(self, *args, **options):
        User = get_user_model()

        username = "admin"
        password = "admin"
        email = "admin@admin.com"

        # If superuser already exists, do nothing
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING("Superuser already exists."))
            return

        # Create the superuser
        User.objects.create_superuser(
            username=username,
            password=password,
            email=email,
        )

        self.stdout.write(self.style.SUCCESS("Superuser created successfully."))

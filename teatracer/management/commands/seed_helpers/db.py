import os
from django.conf import settings
from django.core.management import call_command

def remove_and_migrate_db(stdout):
    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')

    if os.path.exists(db_path):
        os.remove(db_path)
        stdout.write('DB removed successfully.')
    else:
        stdout.write('DB does not exist.')

    try:
        call_command('makemigrations', interactive=True)
        call_command('migrate', interactive=True)
        stdout.write('Migrations applied')
    except Exception as e:
        stdout.write(f'Migration Failed: {e}')

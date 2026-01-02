# import os
# from django.conf import settings
# from django.core.management import call_command
#
# def remove_and_migrate_db(stdout):
#     db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
#
#     if os.path.exists(db_path):
#         os.remove(db_path)
#         stdout.write('DB removed successfully.')
#     else:
#         stdout.write('DB does not exist.')
#
#     try:
#         call_command('makemigrations', interactive=True)
#         call_command('migrate', interactive=True)
#         stdout.write('Migrations applied')
#     except Exception as e:
#         stdout.write(f'Migration Failed: {e}')



import os
from django.conf import settings
from django.core.management import call_command
import importlib.util

def remove_and_migrate_db(stdout):
    # ---------- Remove DB.sqlite3 File ----------
    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    if os.path.exists(db_path):
        os.remove(db_path)
        stdout.write('DB removed successfully.')
    else:
        stdout.write('DB does not exist.')

    # ---------- remove migrations file ----------
    for app in settings.INSTALLED_APPS:
        try:
            if app.startswith('django.'):
                continue

            spec = importlib.util.find_spec(app)
            if spec is None or spec.origin is None:
                continue

            app_path = os.path.dirname(spec.origin)
            migrations_path = os.path.join(app_path, 'migrations')
            if os.path.exists(migrations_path):
                for filename in os.listdir(migrations_path):
                    if filename != '__init__.py' and filename.endswith('.py'):
                        file_path = os.path.join(migrations_path, filename)
                        os.remove(file_path)
                        stdout.write(f'Removed migration file: {app}.{filename}')
        except Exception as e:
            stdout.write(f'Error checking migrations for {app}: {e}')

    # ---------- run migrations ----------
    try:
        call_command('makemigrations', interactive=True)
        call_command('migrate', interactive=True)
        stdout.write('Migrations applied successfully.')
    except Exception as e:
        stdout.write(f'Migration Failed: {e}')

# tea-tracer-backend
This is a django rest backend repo for tea tracer

### Run and Deploy
 
1- Create a `.venv` dir for environment and install dependencies

```bash
python -m venv .venv
pip install -r requirements.txt
```
<br>

2- To run the code, create a `.env` file based on `.env.sample`  in root directory

<br>

3- Migrate the Database for `db.sqlite3`

```bash
python manage.py makemigrations
python manage.py migrate
```
<br>

4- Run Seed Data to have admin account with following information

```bash
# This will create a superuser with:
# Username: admin
# Password: admin
# Email: admin@admin.com

python manage.py seed_data
```
<br>


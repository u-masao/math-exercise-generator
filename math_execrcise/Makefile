help:

shell:
	poetry run python manage.py shell

runserver:
	poetry run python manage.py runserver 127.0.0.1:8000

check:
	poetry run python manage.py check

migrate:
	poetry run python manage.py migrate

makemigrations-polls:
	poetry run python manage.py makemigrations polls

sqlmigrate-polls-0001:
	poetry run python manage.py sqlmigrate polls 0001

add_polls:
	poetry run python manage.py startapp polls

lint:
	poetry run black -l 79 .
	poetry run flake8 .
	poetry run mypy .

sql:
	sqlite3 db.sqlite3

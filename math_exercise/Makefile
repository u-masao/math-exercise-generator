help:

createsuperuser:
	poetry run python manage.py createsuperuser

shell:
	poetry run python manage.py shell

runserver:
	poetry run python manage.py runserver 0.0.0.0:8000

check:
	poetry run python manage.py check

migrate:
	poetry run python manage.py migrate

makemigrations-polls:
	poetry run python manage.py makemigrations polls

sqlmigrate-polls-0001:
	poetry run python manage.py sqlmigrate polls 0001

test: lint test_polls test_sheets

test_polls:
	poetry run python manage.py test polls

add_polls:
	poetry run python manage.py startapp polls

add_sheets:
	poetry run python manage.py startapp sheets

test_sheets:
	poetry run python manage.py test sheets

makemigrations-sheets:
	poetry run python manage.py makemigrations sheets

lint:
	poetry run isort .
	poetry run black -l 88 .
	poetry run flake8 . --max-line-length 88

sql:
	sqlite3 db.sqlite3

dumpdata-to-fixture-sheets:
	poetry run python manage.py dumpdata | jq 'map(select(.["model"] == "sheets.question"))' > sheets/fixture/questions.json
	poetry run python manage.py dumpdata | jq 'map(select(.["model"] == "sheets.algorythm"))' > sheets/fixture/algorythms.json

makemigrations-sheets-empty:
	poetry run python manage.py makemigrations sheets --empty

heroku-migrate:
	heroku run sh -c 'cd math_exercise ; python manage.py migrate'

heroku_login:
	heroku login

heroku_apps:
	heroku apps

heroku_git_remote:
	echo heroku git:remote -a app_name

heroku_start:
	heroku ps:scale web=1

heroku_stop:
	heroku ps:scale web=0

heroku_open:
	heroku open

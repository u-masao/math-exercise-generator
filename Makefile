
start-project:
	poetry run django-admin startproject math_exercise

version:
	poetry run python -m django --version

requirements:
	poetry export -f requirements.txt --output requirements.txt

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

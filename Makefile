
start-project:
	poetry run django-admin startproject math_exercise

version:
	poetry run python -m django --version

requirements:
	poetry export -f requirements.txt --output requirements.txt

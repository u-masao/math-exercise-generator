

all: lint
	poetry run python -m src.example


lint:
	poetry run black src
	poetry run flake8 src
	poetry run mypy src

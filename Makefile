all: reports

reports: lint
	poetry run python -m src.questions reports

lint:
	poetry run black src -l 79
	poetry run flake8 src
	poetry run mypy src

clean:
	rm -f reports/*.pdf

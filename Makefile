all: reports

reports: lint clean
	poetry run python -m src.questions reports --pages 30

lint:
	poetry run black src -l 79
	poetry run flake8 src
	poetry run mypy src

clean:
	rm -f reports/*.pdf

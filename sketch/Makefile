all: reports

reports: lint clean
	poetry run python -m src.questions

lint:
	poetry run isort src
	poetry run black src -l 79
	poetry run flake8 src

clean:
	rm -f reports/*.pdf

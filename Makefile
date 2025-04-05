install:
	pip install -upgrade pip && pip install -r requirements.txt

lint:
	flake8 --max-line-length=120 --ignore=E501,E203,E266,E402,E731 .
	black --check --line-length 120 .
	isort --check-only --profile black .

run:
	python src/app.py

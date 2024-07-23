lint:
	flake8 .

format:
	black .

test:
	pytest

test-coverage:
	pytest
	coverage report
	coverage xml
	coveralls

check:
	black --check .
	flake8 .

migrate:
	python manage.py migrate

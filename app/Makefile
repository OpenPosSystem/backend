lint:
	flake8 .

format:
	black .

test:
	pytest

test-coverage:
	coverage run -m pytest && coverage report && coverage xml

check:
	black --check .
	flake8 .

migrate:
	python manage.py migrate

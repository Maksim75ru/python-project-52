PORT ?= 8000

install:
	poetry install

package-install:
	python3 -m pip install --user --force-reinstall dist/*.whl

lint:
	poetry run flake8 task_manager

dev:
	poetry run python manage.py runserver

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

test:
	poetry run python manage.py test

test-coverage:
	poetry run coverage run --source='task_manager' manage.py test task_manager
	poetry run coverage xml


PORT ?= 8080

install:
	poetry install

package-install:
	python3 -m pip install --user --force-reinstall dist/*.whl

lint:
	poetry run flake8 task_manager

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi:application

dev:
	poetry run python3 manage.py runserver

migrate:
	poetry run python3 manage.py makemigrations
	poetry run python3 manage.py migrate

test:
	poetry run python3 manage.py test

test-coverage:
	poetry run coverage run --source='task_manager' manage.py test task_manager
	poetry run coverage xml


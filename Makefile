PORT ?= 8000
MANAGE := poetry run python manage.py

start:
	@$(MANAGE) migrate
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi:application

install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user --force-reinstall dist/*.whl

dev:
	@$(MANAGE) migrate
	@$(MANAGE) runserver

shell:
	@$(MANAGE) shell

make-migration:
	@$(MANAGE) makemigrations

migrate: make-migration
	@$(MANAGE) migrate

lint:
	poetry run flake8 task_manager

test:
	poetry run python3 manage.py test

test-coverage:
	poetry run coverage run --source="task_manager" manage.py test task_manager
	poetry run coverage xml

makemessages:
	django-admin makemessages --ignore="static" --ignore=".env" -l ru
	django-admin compilemessages --ignore="static" --ignore=".env" -l ru
	django-admin makemessages -a --ignore="static" --ignore=".env"

build: install migrate

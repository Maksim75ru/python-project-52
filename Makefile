PORT ?= 8000
MANAGE := poetry run python manage.py

start:
	@$(MANAGE) migrate
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi:application

install:
	@poetry install

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
	@$(MANAGE) test

test-coverage:
	coverage run --source='.'  manage.py test task_manager
	coverage html

build: install migrate

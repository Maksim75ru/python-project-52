install:
	poetry install

build: check
	poetry build

package-install:
	python3 -m pip install --user --force-reinstall dist/*.whl

lint:
	poetry run flake8 task_manager

start:
	poetry run python manage.py runserver 127.0.0.1:8000

check:
	poetry check


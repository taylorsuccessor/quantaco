.DEFAULT_GOAL := help


install:
	poetry install

poetry-shell:
	poetry shell
	
lint:
	poetry run flake8 .
	poetry run pylint .

format:
		poetry run isort . # --check-only
		poetry run black .

# make startapp appname=users
startapp:
	poetry run python manage.py startapp $(appname)

migrate:
	poetry run python manage.py migrate
	poetry run python manage.py migrate django_celery_results # if needed

makemigrations:
	poetry run python manage.py makemigrations

run:
	poetry run python manage.py runserver

test:
	poetry run pytest

create-user:
	poetry run python manage.py createsuperuser

enter-docker:
	docker-compose exec web /bin/bash

celery-start:
	poetry run celery -A large_file_processing worker --loglevel=info

celery-clear:
	poetry run  celery -A large_file_processing purge

spark-submit-chunk:
	spark-submit  process_large_file_pyspark_window.py

spark-submit:
	spark-submit  process_large_file_pyspark.py

help:
	echo "Makefile commands:"
	echo "  install        - Install all dependencies"
	echo "  migrate        - Apply database migrations"
	echo "  makemigrations - Create new database migrations"
	echo "  run            - Run the Django development server"
	echo "  test           - Run tests"

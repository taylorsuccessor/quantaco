FROM python:3.12.4

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-dev

COPY .env.docker /app/.env
COPY . /app/

RUN poetry run python manage.py collectstatic --noinput

CMD ["gunicorn", "apidjango.wsgi:application", "--bind", "0.0.0.0:8000"]

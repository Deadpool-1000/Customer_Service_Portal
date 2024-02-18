FROM python:3.11-slim-bookworm

COPY Pipfile Pipfile.lock ./
WORKDIR /app
COPY . .
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

EXPOSE 5000
CMD gunicorn -w 4 -b 0.0.0.0:5000 'wsgi:app'
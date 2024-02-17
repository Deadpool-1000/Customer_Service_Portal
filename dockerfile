FROM python:3.11-slim-bookworm

COPY Pipfile Pipfile.lock ./
WORKDIR /app
COPY . .
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

EXPOSE 5000
CMD cd src && python3 -m flask run --host=0.0.0.0
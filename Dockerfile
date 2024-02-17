FROM python:3.11

WORKDIR /app
ADD . /app

COPY . .
ENV POETRY_VERSION=1.7.0
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_VIRTUALENVS_CREATE=false

RUN curl -sSL https://install.python-poetry.org | python -

ENV PATH="/root/.local/bin:${PATH}"
RUN poetry install --no-interaction --no-ansi

COPY pyproject.toml /app
COPY poetry.lock /app

EXPOSE 8000
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

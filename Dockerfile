FROM python:3.10.0

ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.13

# System deps:
RUN pip install --upgrade pip
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi --no-dev

# Creating folders, and files for a project:
COPY . /code

EXPOSE 8000
# RUN poetry run django test
RUN poetry run ./manage.py test --settings=leave_management.settings.dev
CMD ["gunicorn", "leave_management.asgi:application", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker"]

# Usage
## Build Dockerfile for production
# docker build -t shop_api --build-arg YOUR_ENV=production .
# docker run --rm --publish 8000:8000 -e SECRET_KEY={{ DJANGO_SECRET_KEY }} shop_api

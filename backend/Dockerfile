FROM python:3.11.5-slim-bookworm
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE nemesis.settings

RUN apt-get update && apt-get install -y postgresql-client

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN useradd -ms /bin/bash nemesis
RUN chown -R nemesis:nemesis /app
USER nemesis

EXPOSE 8000

RUN chmod +x entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
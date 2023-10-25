FROM python:3.11.5-slim-bookworm
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE nemesis.settings

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN useradd -ms /bin/bash nemesis
RUN chown -R nemesis:nemesis /app
USER nemesis

EXPOSE 8000

RUN chmod +x entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
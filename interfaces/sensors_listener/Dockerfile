FROM python:3.11.5-slim-bookworm
ENV PYTHONUNBUFFERED 1

COPY interfaces/sensors_listener/requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir -p /app/interfaces/sensors_listener
COPY ./ /app/
WORKDIR /app/interfaces/sensors_listener

RUN useradd -ms /bin/bash nemesis_sl
RUN chown -R nemesis_sl:nemesis_sl /app
USER nemesis_sl

CMD ["python", "SensorsListener.py"]

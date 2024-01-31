FROM python:3.11.5-slim-bookworm
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir -p /app/interfaces/replay
COPY . /app/interfaces/replay
WORKDIR /app/interfaces/replay

RUN useradd -ms /bin/bash nemesis_replay
RUN chown -R nemesis_replay:nemesis_replay /app
USER nemesis_replay

CMD ["python", "SensorsListener.py"]

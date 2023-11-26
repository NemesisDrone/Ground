FROM python:3.11.5-slim-bookworm
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir -p /app/interfaces/communication
COPY . /app/interfaces/coamunication
WORKDIR /app/interfaces/communication

RUN useradd -ms /bin/bash nemesis_com
RUN chown -R nemesis_com:nemesis_com /app
USER nemesis_com

EXPOSE 27015

CMD ["python", "CommunicationServer.py", "0.0.0.0"]
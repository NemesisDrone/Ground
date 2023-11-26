FROM python:3.11.6-slim-bookworm
ENV PYTHONUNBUFFERED 1

# Copy data.
USER nemesis_nvs
RUN mkdir -p /app/interfaces/nvs
COPY . /app/interfaces/nvs
WORKDIR /app/interfaces/nvs

# Install required stuff.
USER root
RUN apt update
RUN apt install libgstreamer1.0-0 libgirepository-1.0-1 libgirepository1.0-dev gstreamer1.0-plugins-base gobject-introspection python3-gst-1.0 python3-gi -y
RUN python3 -m pip install -r requirements.txt

# Setup for run
USER nemesis_nvs

CMD ["python3", "VideoStreaming.py"]

FROM python:3.11.6-slim-bookworm
ENV PYTHONUNBUFFERED 1

RUN useradd -m nemesis_nvs

# Install required stuff.
RUN apt update
RUN apt install libgstreamer1.0-0 libgirepository-1.0-1 libgirepository1.0-dev gstreamer1.0-plugins-base gobject-introspection python3-gst-1.0 python3-gi cmake libcairo2-dev python3-cairo python3-gi-cairo gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-libav -y

# Setup paths
RUN mkdir -p /app/interfaces/nvs
COPY ./requirements.txt /app/interfaces/nvs/requirements.txt
WORKDIR /app/interfaces/nvs

# Install the other stuff.
RUN python3 -m pip install -r /app/interfaces/nvs/requirements.txt

# Copy data.
COPY . /app/interfaces/nvs

# Setup for run
USER nemesis_nvs

# Expose ports
EXPOSE 7000
EXPOSE 7001

# In the YAML
CMD []
ENTRYPOINT []

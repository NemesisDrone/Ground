import json
import socket
import threading
import sys
import os
import redis
import logging
import time

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

r = redis.Redis(host=os.environ.get("REDIS_HOST"), port=os.environ.get("REDIS_PORT"), decode_responses=True, db=0)
r.set("IS_DRONE_CONNECTED", 0)
r.set("LAST_HEARTBEAT_RECEIVED", 0)
r.set("LAST_HEARTBEAT_SENT", 0)

# socket_server = None


def publish_drone_connection_status(status: bool) -> None:
    """
    Publish the drone connection status on REDIS.
    """
    r.set("IS_DRONE_CONNECTED", int(status))
    r.publish("communication_forwarding", json.dumps({
        "type": "drone:connection-status",
        "data": {
            "connected": status
        }
    }))

    if not status:
        logging.critical("Drone disconnected")


def handle_emission(client_socket):
    """
    Method used to handle the emission of messages to the server.
    :param client_socket: The socket to use to send messages
    """
    logging.info("Thread Handle Emission started")
    pubsub = r.pubsub()
    pubsub.subscribe("actions")

    while True:
        message = pubsub.get_message(ignore_subscribe_messages=True)
        try:
            if message:
                message = message["data"]
                logging.debug("from redis: %s", message)
                data = str(json.dumps(message))
                client_socket.send(len(data).to_bytes(4, byteorder='big'))
                client_socket.send(data.encode())

            # Wait 3 seconds before sending another heartbeat
            if time.time() - float(r.get("LAST_HEARTBEAT_SENT")) > 1.5:
                time.sleep(0.1)
                client_socket.send(len("heartbeat").to_bytes(4, byteorder='big'))
                client_socket.send("heartbeat".encode())
                r.set("LAST_HEARTBEAT_SENT", time.time())
                logging.debug("Heartbeat sent")

        except BrokenPipeError as e:
            logging.error("Broken pipe error: %s", e)
            publish_drone_connection_status(False)
            break


def handle_reception(client_socket):
    """
    Method used to handle the reception of messages from the server.
    And forward them on REDIS to be used by the backend/other services
    :param client_socket: The socket to use to receive messages
    """
    logging.info("Thread Handle Reception started")
    while True:
        try:
            message_length_bytes = client_socket.recv(4)
            message_length = int.from_bytes(message_length_bytes, byteorder='big')
            message = client_socket.recv(message_length).decode()

            if message:
                """
                If received message is a heartbeat, set the drone as connected
                """
                if message == "heartbeat":
                    logging.debug("Heartbeat received")
                    r.set("LAST_HEARTBEAT_RECEIVED", time.time())
                    publish_drone_connection_status(True)
                    continue

                # logging.debug("from socket: %s", message)
                r.publish("communication_forwarding", message)

        except Exception as e:
            logging.error("Reception error: %s", e)
            publish_drone_connection_status(False)
            break


class CommunicationServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.settimeout(5)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        self.connections = []

    def handle_client_connection(self, client_socket):
        thread_reception = threading.Thread(
            target=handle_reception,
            args=(client_socket,),
            daemon=True,
        )
        thread_reception.start()

        thread_emission = threading.Thread(
            target=handle_emission,
            args=(client_socket,),
            daemon=True,
        )
        thread_emission.start()

    def accept_connections(self):
        logging.info("CommunicationServer - Waiting for connection on %s:%s", self.host, self.port)
        while True:
            try:
                client_socket, _ = self.server_socket.accept()
                # remove all existing connections
                # so yes it's not really a server but it's fine, i guess i could use a socket pool. Ah ? That's copilot who said "socket pool", not me. Should I use it ? Nah, I'm fine.
                for connection in self.connections:
                    connection.close()
                self.connections.append(client_socket)

                logging.info("CommunicationServer - New connection : %s", client_socket)

                thread = threading.Thread(
                    target=self.handle_client_connection,
                    args=(client_socket,),
                    daemon=True,
                )
                thread.start()
            except TimeoutError as e:
                continue


if __name__ == "__main__":
    socket_server = CommunicationServer(sys.argv[1], 27015)
    socket_server.accept_connections()

import socket
import threading
import sys
import os
import redis
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

r = redis.Redis(host=os.environ.get("REDIS_HOST"), port=os.environ.get("REDIS_PORT"), decode_responses=True, db=0)

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
        if message:
            message = message["data"]
            logging.debug("from redis: %s", message)
            client_socket.send(
                ('~' + message).encode()
            )


def handle_reception(client_socket):
    """
    Method used to handle the reception of messages from the server.
    And forward them on REDIS to be used by the backend/other services
    :param client_socket: The socket to use to receive messages
    """
    print("Handle Reception Thread started")
    while True:
        try:
            message_length_bytes = client_socket.recv(4)
            message_length = int.from_bytes(message_length_bytes, byteorder='big')
            message = client_socket.recv(message_length).decode()

            if message:
                logging.debug("from socket: %s", message)
                r.publish("communication_forwarding", message)

        except Exception as e:
            logging.error("Reception error: %s", e)
            break


class CommunicationServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            client_socket, _ = self.server_socket.accept()
            self.connections.append(client_socket)

            logging.info("CommunicationServer - New connection : %s", client_socket)

            thread = threading.Thread(
                target=self.handle_client_connection,
                args=(client_socket,),
                daemon=True,
            )
            thread.start()


if __name__ == "__main__":
    socket_server = CommunicationServer(sys.argv[1], 27015)
    socket_server.accept_connections()

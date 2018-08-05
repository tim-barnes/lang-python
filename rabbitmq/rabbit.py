import pika
import socket
import time


TIMEOUT_S = 3
TIMEOUT_LIMIT = 10

SERVER = 'rabbitmq'

def wait_for(server):
    """
    Waits for TIMEOUT_LIMIT * TIMEOUT_S seconds for RabbitMQ to be up
    """
    s = socket.socket()

    counter = 0
    while counter < TIMEOUT_LIMIT:
        try:
            s.connect((server, 5672))
            s.close()
            return True
        except socket.error as e:
            print("Waiting for: {}:5672".format(server))
            time.sleep(TIMEOUT_S)

    return False


def connection(server, username, password):
    """
    Returns a rabbit MQ connection
    """

    credentials = pika.PlainCredentials(username, password)
    return pika.BlockingConnection(pika.ConnectionParameters(server, credentials=credentials))

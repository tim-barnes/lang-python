import pika
import time
import os
from rabbit import connection, wait_for, SERVER

ME = os.environ['HOSTNAME']
MODULO = int("0x{}".format(ME[0:3]), 16) % 2
print(" MODULO: {}".format(MODULO))


def callback(ch, method, properties, body):
    print("<= Receiver {}".format(body))
    # time.sleep(int(body))
    # print("== done")
    # ch.basic_ack(delivery_tag=method.delivery_tag)


if not wait_for('rabbitmq'):
    print("Rabbit MQ server '{}' not up!".format(SERVER))
    exit(1)


connection = connection(SERVER, 'guest', 'guest')
channel = connection.channel()
channel.exchange_declare(exchange='numbers',
                         exchange_type='direct')

queue = channel.queue_declare(exclusive=True)
queue_name = queue.method.queue

channel.queue_bind(exchange='numbers', 
                   queue=queue_name,
                   routing_key=str(MODULO))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

print("=== Waiting for messages")

channel.start_consuming()

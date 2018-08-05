import time
import pika
from rabbit import wait_for, connection, SERVER


if not wait_for('rabbitmq'):
    print("Rabbit MQ server '{}' not up!".format(SERVER))
    exit(1)

connection = connection(SERVER, 'guest', 'guest')
channel = connection.channel()

channel.exchange_declare(exchange='numbers',
                         exchange_type='direct')

for i in range(1, 10):
    channel.basic_publish(exchange='numbers',
                          routing_key='{}'.format(i % 2),
                          body='{}'.format(i))

    print(" => {} {}".format(i % 2, i))
    time.sleep(1)

connection.close()

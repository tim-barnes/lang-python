"""
Simple worker - accepts a number, calculates a term and sends it on

Use as term.py -[a, b, c] num
"""
import argparse
import pika
import time
import uuid
from rabbit import connection, wait_for, SERVER


class Requester(object):
    """
    The actual calculation
    """

    def __init__(self, *, request_queue, response_queue):
        self.request_queue = request_queue
        self.response_queue = response_queue

        # For the call itself
        self.response = None
        self.correlation_id = None

        # Setup the connections
        self.connection = connection(SERVER, 'guest', 'guest')
        self.channel = self.connection.channel()

        # Using a topic exchange
        self.channel.exchange_declare(exchange='numbers',
                                      exchange_type='topic')

        # Bind the response queue to us
        queue = self.channel.queue_declare(exclusive=True)
        queue_name = queue.method.queue

        self.channel.queue_bind(exchange='numbers',
                                queue=queue_name,
                                routing_key=self.response_queue)

        self.channel.basic_consume(self.on_response_callback,
                                   queue=queue_name,
                                   no_ack=True)

        print("=== Setup for response")

    def on_response_callback(self, ch, method, props, body):
        if self.correlation_id == props.correlation_id:
            self.response = int(body)

    def call(self, n):
        self.response = None
        self.correlation_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='numbers',
                                   routing_key=self.request_queue,
                                   properties=pika.BasicProperties(
                                         correlation_id=self.correlation_id,
                                         ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Simple term calculator")

    parser.add_argument("-n",
                        default=100,
                        help="The number of terms expected")

    parser.add_argument("--req",
                        default="x.req",
                        help="The request queue for calculation")
    parser.add_argument("--res",
                        default="x.res",
                        help="The response queue for the calculated term")

    args = parser.parse_args()

    # Connect to RabbitMQ
    if not wait_for('rabbitmq'):
        print("Rabbit MQ server '{}' not up!".format(SERVER))
        exit(1)

    # Short delay to make sure the calculation queue is up and listening
    # TODO switch to durable queues so Rabbit recovers this for us
    time.sleep(2)

    # Make the calls
    calculator_rpc = Requester(request_queue=args.req, response_queue=args.res)
    for i in range(0, int(args.n)):
        calculator_rpc.call(i)

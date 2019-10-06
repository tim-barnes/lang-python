"""
Simple worker - accepts a number, calculates a term and sends it on

Use as term.py -[a, b, c] num
"""
import argparse
import pika
from rabbit import connection, wait_for, SERVER


class Term(object):
    """
    The actual calculation
    """

    def __init__(self, *, a=0, b=0, c=0, output_queue=""):
        self.a = a
        self.b = b
        self.c = c
        self.output_queue = output_queue

    def calculate(self, x):
        return self.a * x ** 2 + self.b * x + self.c

    def on_request_callback(self, ch, method, props, body):
        value = int(body)
        me = str(self)

        print("<= {} {}".format(me, value))
        term = self.calculate(value)
        print(" => {} {}".format(me, term))

        ch.basic_publish(exchange='numbers',
                         routing_key=self.output_queue,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=str(term))

    def __str__(self):
        s = []
        if self.a != 0:
            s.append("{}x^2".format(self.a))
        if self.b != 0:
            s.append("{}x".format(self.b))
        if self.c != 0:
            s.append("{}".format(self.c))
        return "+".join(s)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Simple term calculator")

    parser.add_argument("-a",
                        default=0,
                        help="The A coefficient")
    parser.add_argument("-b",
                        default=0,
                        help="The B coefficient")
    parser.add_argument("-c",
                        default=0,
                        help="The C coefficient")

    parser.add_argument("--iq",
                        default="x.req",
                        help="The input queue for calculation")
    parser.add_argument("--oq",
                        default="x.term",
                        help="The output queue for the calculated term")

    args = parser.parse_args()

    calculator = Term(a=int(args.a), b=int(args.b), c=int(args.c), output_queue=args.oq)

    # Connect to RabbitMQ
    if not wait_for('rabbitmq'):
        print("Rabbit MQ server '{}' not up!".format(SERVER))
        exit(1)

    connection = connection(SERVER, 'guest', 'guest')
    channel = connection.channel()

    # Using a topic exchange
    channel.exchange_declare(exchange='numbers',
                             exchange_type='topic')

    queue = channel.queue_declare(exclusive=True)
    queue_name = queue.method.queue

    channel.queue_bind(exchange='numbers',
                       queue=queue_name,
                       routing_key=args.iq)

    channel.basic_consume(calculator.on_request_callback,
                          queue=queue_name,
                          no_ack=True)

    print("=== Waiting for messages")
    channel.start_consuming()

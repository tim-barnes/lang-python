"""
Simple worker - accepts a number, calculates a term and sends it on

Use as term.py -[a, b, c] num
"""
import argparse
import pika
from rabbit import connection, wait_for, SERVER


class Sum(object):
    """
    The actual calculation
    """

    def __init__(self, *, num_terms=3, output_queue=""):
        self.num_terms = num_terms
        self.output_queue = output_queue

        self.correlation = {}

    def on_request_callback(self, ch, method, props, body):
        value = int(body)
        me = str(self)

        cid = props.correlation_id

        terms = self.correlation.setdefault(cid, [])
        terms.append(value)

        print("<= {} {} {} {}".format(me, cid, value, terms))

        # Dispatch the sum if we have recieved all the terms
        if len(terms) == self.num_terms:
            total = sum(terms)
            print(" => {} {} {}".format(me, cid, total))
            ch.basic_publish(exchange='numbers',
                             routing_key=self.output_queue,
                             properties=pika.BasicProperties(correlation_id=cid),
                             body=str(total))
            self.correlation.pop(cid)

    def __str__(self):
        return "Sum"


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Simple term calculator")

    parser.add_argument("-t",
                        default=3,
                        help="The number of terms expected")

    parser.add_argument("--iq",
                        default="x.req",
                        help="The input queue for calculation")
    parser.add_argument("--oq",
                        default="x.term",
                        help="The output queue for the calculated term")

    args = parser.parse_args()

    calculator = Sum(num_terms=int(args.t), output_queue=args.oq)

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

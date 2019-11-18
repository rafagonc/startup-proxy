import os
from pika import BlockingConnection, URLParameters


def get_connection():
    while True:
        try:
            connc = BlockingConnection(
                URLParameters(
                    os.getenv("AMQP_URL",
                              "amqp://guest:guest@localhost:5672/")))
            if connc.is_open:
                break
        except Exception:
            pass
    return connc


def get_channel():
    return get_connection().channel()


def declare_queue_if_needed(ch, queue_name, props={}, durable=False):
    try:
        ch.queue_declare(queue=queue_name, durable=durable, arguments=props)
    except Exception:
        pass

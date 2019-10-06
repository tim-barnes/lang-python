import time
from worker_a import pulse as pulse_a
from worker_b import pulse as pulse_b
from celery import Celery, chain


app = Celery(__name__, broker="redis://redis//")
# app.conf.task_routes = {
#     'worker_a.pulse': {'queue': 'worker_a'},
#     'worker_b.pulse': {'queue': 'worker_b'}
# }


def heartbeat():
    i = 0

    while True:
        print(f"Beat: {i}")

        c = chain(pulse_a.s(i) | pulse_b.s())
        c()
        i += 1

        time.sleep(1)


if __name__ == "__main__":
    time.sleep(1)
    heartbeat()

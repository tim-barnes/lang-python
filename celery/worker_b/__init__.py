from celery import Celery


app = Celery(__name__, broker="redis://redis//")
# app.conf.task_routes = {
#     'worker_b.pulse': {'queue': 'worker_b'}
# }

@app.task
def pulse(i):
    print(f"Pulse: {i} ({__name__})")

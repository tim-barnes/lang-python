from celery import Celery

app = Celery(__name__, broker="redis://redis//")
# app.conf.task_routes = {
#     'worker_a.pulse': {'queue': 'worker_a'}
# }

@app.task
def pulse(i):
    print(f"Pulse: {i} ({__name__})")
    return i + 1000

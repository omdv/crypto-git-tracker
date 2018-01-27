from project import create_app
from celery_once import QueueOnce

app, cel = create_app()


@cel.task(name='task_summary', base=QueueOnce, once={'graceful': True})
def task_summary():
    return 'Success summary'
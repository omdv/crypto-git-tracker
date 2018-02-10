import datetime as dt
from project import create_app, db
from project.api.models import GitRateLimitModel
from project.analytics.git_watcher import GitWatcher
from celery_once import QueueOnce


app, cel = create_app()


@cel.task(name='task_rate_limit', base=QueueOnce, once={'graceful': True})
def task_rate_limit():
    with app.app_context():
        watcher = GitWatcher(None, None, None, None)
        watcher.set_app_config(app.config)
        rate = watcher.get_rate_limit()

        # write record
        db.session.add(GitRateLimitModel(time=dt.datetime.now(), rate=rate))
        db.session.commit()
        print('Current rate limit {}'.format(rate))

    return 'Success summary'

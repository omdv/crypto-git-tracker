from project import create_app, db
from project.api.models import RepoControlRecord
from project.analytics.git_watcher import GitWatcher
from celery_once import QueueOnce

app, cel = create_app()


@cel.task(name='task_watcher', base=QueueOnce, once={'graceful': True})
def task_watcher(verbose=True):
    with app.app_context():
        # read control table
        repos = RepoControlRecord.query.all()
        updated = 0

        # query watcher
        for _r in repos:
            if verbose:
                print("Coin: {}\t Url: {}\t Date: {}".
                      format(_r.ticker, _r.url, _r.last_update))

            watcher = GitWatcher(
                _r.ticker, _r.apihandle, _r.url, _r.last_update)
            watcher.set_app_config(app.config)
            new_date = watcher.download()
            if new_date:
                _r.last_update = new_date
                updated += 1
            db.session.add(_r)

        # save new data
        try:
            db.session.commit()
            result_string = "Updated {} of {}".format(updated, len(repos))
            if verbose:
                print(result_string)
            result = result_string
        except:
            db.session.rollback()
            raise BaseException("Failed to save updated date")
            result = "Failed to save"

    return result

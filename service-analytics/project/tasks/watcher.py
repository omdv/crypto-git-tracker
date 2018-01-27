from project import create_app, db
from project.api.models import RepoControlRecord
from project.analytics.git_watcher import GitWatcher
from celery_once import QueueOnce

app, cel = create_app()


@cel.task(name='task_watcher', base=QueueOnce, once={'graceful': True})
def task_watcher():
    with app.app_context():
        # read control table
        repos = RepoControlRecord.query.all()

        # query watcher
        for repo in repos:
            print("Coin: {}\t Url: {}\t Date: {}".
                  format(repo.coin, repo.url, repo.last_update))

            watcher = GitWatcher(repo.coin, repo.url, repo.last_update)
            watcher.set_app_config(app.config)
            new_date = watcher.download()
            if new_date:
                repo.last_update = new_date
            db.session.add(repo)

        # save new data
        try:
            db.session.commit()
            print("Successfully saved\n")
            result = "Updated {}".format(len(repos))
        except:
            db.session.rollback()
            raise BaseException("Failed to save updated date")
            result = "Failed to save"

    return result

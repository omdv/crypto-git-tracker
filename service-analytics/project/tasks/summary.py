from project import create_app
from project.analytics.git_analytics import GitAnalytics
from celery_once import QueueOnce


app, cel = create_app()


@cel.task(name='task_summary', base=QueueOnce, once={'graceful': True})
def task_summary():
    with app.app_context():
        analyzer = GitAnalytics(app.config)
        df, _, _ = analyzer.summary_table()
        try:
            print("Processed {} coins".format(df.shape[0]))
        except:
            print("Processed 0 coins")

    return 'Success summary'

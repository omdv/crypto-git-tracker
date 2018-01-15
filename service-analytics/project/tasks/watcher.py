from project import create_app

app, cel = create_app()


@cel.task(name='test_watcher')
def test_watcher():
    print('Git watcher')
    return 'Git watcher'
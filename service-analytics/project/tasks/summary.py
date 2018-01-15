from project import create_app

app, cel = create_app()


@cel.task(name='test_summary')
def test_watcher():
    print('Git summary')
    return 'Git summary'
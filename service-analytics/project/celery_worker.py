# the purpose of this file is to provide context for celery in supervisord
from project import create_app

app, cel = create_app()
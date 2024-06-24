web: gunicorn tasktopia.wsgi --log-file
worker: celery -A Tasktopia worker --loglevel=info
beat: celery -A Tasktopia beat --loglevel=info
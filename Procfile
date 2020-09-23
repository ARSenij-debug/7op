web: gunicorn django_project.wsgi:application --log-file - --log-level debug
web: gunicorn --bind 0.0.0.0:$PORT hello:app
python manage.py collectstatic --noinput
manage.py migrate
web: python manage.py runserver 0.0.0.0:5000

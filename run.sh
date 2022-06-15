pkill gunicorn
pipenv install
pipenv run gunicorn app.main:app
# lrtest

### dev run command:

```
pipenv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8082
```
### prod run command:
```
pipenv run gunicorn app.main:app
```
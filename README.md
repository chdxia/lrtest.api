# lrtest

### dev run command:

```
uvicorn app.main:app --reload --host 0.0.0.0 --port 8082
```
### prod run command:
```
gunicorn app.main:app
```
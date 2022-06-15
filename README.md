# lrtest

### dev run command:

```shell
pipenv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8082
```
### prod run command:
```shell
pipenv run gunicorn app.main:app
```
### jenkins 配置 :

- GitHub项目：https://github.com/chdxia/lrtest-api/
- Git Repositories：git@github.com:chdxia/lrtest-api.git
- 构建触发器：GitHub hook trigger for GITScm polling
- 构建环境：Send files or execute commands over SSH before the build starts

```shell
# Exec command
rm -rf /root/lrtest-api/.*
```

- 构建：Send files or execute commands over SSH

```shell
# Source files
**/**
# Remote directory
/root/lrtest-api
# Exec command
cd /root/lrtest-api
pipenv install
pipenv run gunicorn app.main:app
```
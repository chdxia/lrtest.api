# lrtest-api

prod访问：http://lrtest.chdxia.com
接口文档地址：http://lrtest.chdxia.com/api/v1/docs

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
- 构建触发器：GitHub hook trigger for GITScm polling（在github设置钩子，将请求发送达到jenkins所在地址，GitHub-Repositories-Settings-Webhooks-PlayloadURL：http://jenkins.chdxia.com/github-webhook/）
- 构建环境：Send files or execute commands over SSH after the build runs

```shell
# Exec command
rm -rf /root/lrtest-api/*
```

- 构建：pass
- 构建后操作：Send build artifacts over SSH

```shell
# Source files
**/**
# Remote directory
/root/lrtest-api
# Exec command
cd /root/lrtest-api
chmod u+x run.sh
./run.sh
```
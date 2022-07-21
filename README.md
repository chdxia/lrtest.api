# lrtest-api

prod访问：https://lrtest.chdxia.com

Jenkins地址：https://jenkins.chdxia.com

接口文档地址：https://lrtest.chdxia.com/api/v1/docs

*提示：请修改./app/lib/config.py中的配置信息

### dev run command:

```shell
pipenv install
pipenv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8082
```
### prod run command:
```shell
pipenv install
pipenv run gunicorn app.main:app
```

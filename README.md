# lrtest-api

<p>
  <a href="https://github.com/tiangolo/fastapi">
    <img src="https://img.shields.io/badge/fastapi-0.79.0-brightgreen.svg" alt="fastapi">
  </a>
  <a href="https://github.com/tortoise/tortoise-orm">
    <img src="https://img.shields.io/badge/tortoise--orm-0.19.2-brightgreen.svg" alt="tortoise-orm">
  </a>
</p>

基于FastAPI开发的一个工具平台（后端）

API文档传送门：https://lrtest.chdxia.com/api/v1/docs

项目演示传送门：https://lrtest.chdxia.com

Jenkins传送门：https://jenkins.chdxia.com

前端传送门：https://github.com/chdxia/lrtest-web

### 项目依赖

[fastapi](https://fastapi.tiangolo.com/zh/)：Web框架

[tortoise-orm](https://tortoise.github.io/)：受 Django ORM启发的一个异步ORM（数据库对象关系映射器）

[aiomysql](https://aiomysql.readthedocs.io/en/latest/)：基于pymysql的一个异步MySQL驱动程序

[uvicorn](https://www.uvicorn.org/)：ASGI 服务器

[gunicorn](https://docs.gunicorn.org/en/latest/index.html)：WSGI HTTP 服务器

[loguru](https://pypi.org/project/loguru/)：让日志记录变得简单

[pyyaml](https://pyyaml.org/)：与yaml文件的交互

[passlib](https://passlib.readthedocs.io/en/stable/)：加密用户密码

[qiniu](https://developer.qiniu.com/kodo/1242/python)：七牛SDK，用于图片资源存储

> *提示：请修改./app/lib/config.py中的配置信息

### 开发:

```shell
# 安装依赖
pipenv install

# 启动服务
pipenv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8082
```
### 发布:
```shell
# 安装依赖
pipenv install

# 启动服务
pipenv run gunicorn app.main:app
```

import os
import yaml
from urllib.parse import quote
from .log_settings import logger


# cur_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
# env_path = os.path.join(cur_path, "env.yaml")
home_path = os.environ['HOME']
env_path = os.path.join(home_path, '.env', 'lrtest_env.yaml')


try:
    with open (env_path, 'r', encoding='utf-8') as f:
        config_data = yaml.load(f, Loader=yaml.FullLoader)
except:
    logger.error("load env.yaml fail!!!")


# 获取配置文件
class GetConfig():
    # 获取database_url
    def get_database_url():
        try:
            host = config_data["mysql"]["host"]
            port = config_data["mysql"]["port"]
            user = quote(config_data["mysql"]["user"])
            password = quote(config_data["mysql"]["password"])
            database = config_data["mysql"]["database"]
        except:
            logger.error("mysql config error!!!")
        return f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8'


    # 获取api_route_depends
    def get_api_route_depends():
        try:
            api_route_depends = config_data["api_route_depends"]
        except:
            logger.error('api_route_depends config error!!!')
        return api_route_depends
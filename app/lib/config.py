import os
from urllib.parse import quote
import yaml
from .log_settings import logger


# 这样做是为了在public仓库隐藏自己的配置信息，如需使用，请修改为正确的配置文件路径
# cur_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
# env_path = os.path.join(cur_path, "config.yaml")
home_path = os.environ['HOME']
env_path = os.path.join(home_path, '.env', 'lrtest_config.yaml')


try:
    with open (env_path, 'r', encoding='utf-8') as f:
        config_data = yaml.load(f, Loader=yaml.FullLoader)
except IOError:
    logger.error("load env.yaml fail!!!")


def get_api_route_depends():
    '''获取api_route_depends'''
    try:
        api_route_depends = config_data['api_route_depends']
        return api_route_depends
    except KeyError:
        logger.error('api_route_depends config error!!!')


def get_mysql_credentials():
    '''获取mysql_database_credentials'''
    try:
        host = config_data['mysql']['host']
        port = config_data['mysql']['port']
        user = quote(config_data['mysql']['user'])
        password = quote(config_data['mysql']['password'])
        database = config_data['mysql']['database']
        return {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database
        }
    except KeyError:
        logger.error('mysql config error!!!')


def get_qiniu_config():
    '''获取七牛配置'''
    try:
        bucket = config_data['qiniu']['bucket']
        access_key = config_data['qiniu']['access_key']
        secret_key = config_data['qiniu']['secret_key']
        callback_url = config_data['qiniu']['callback_url']
        external_link_base = config_data['qiniu']['external_link_base']
        return {
            'bucket': bucket,
            'access_key': access_key,
            'secret_key': secret_key,
            'callback_url': callback_url,
            'external_link_base': external_link_base
        }
    except KeyError:
        logger.error('qiniu config error!!!')

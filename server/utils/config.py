from distutils.command.config import config
import os
import yaml
from urllib.parse import quote
from .log_settings import logger


cur_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


yaml_path = os.path.join(cur_path, "config.yaml")


try:
    with open (yaml_path, 'r', encoding='utf-8') as f:
        config_data = yaml.load(f, Loader=yaml.FullLoader)
except:
    logger.error("load config.yaml fail!!!")


class GetConfig():
    def get_database_url():
        try:
            host = config_data["mysql"]["host"]
            port = config_data["mysql"]["port"]
            user = quote(config_data["mysql"]["user"])
            password = quote(config_data["mysql"]["password"])
            database = config_data["mysql"]["database"]
        except:
            logger.error("mysql config error!!!")
        return "mysql+pymysql://{u}:{p}@{host}:{port}/{db}".format(u=user, p=password, host=host, port=port, db=database)
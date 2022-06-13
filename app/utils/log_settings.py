import os
import time
from loguru import logger


basedir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


log_path = os.path.join(basedir, 'logs')


if not os.path.exists(log_path):
    os.mkdir(log_path)


log_path_all = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_log.log')


# rotation日志分割,retention保留时间,enqueue异步写入
logger.add(log_path_all, rotation="00:00", retention="5 days", enqueue=True)


""" logger = logging.getLogger()
logger.setLevel(logging.INFO)


fh = logging.FileHandler(filename=f'./logs/{time.strftime("%Y-%m-%d")}_log.log')


formatter = logging.Formatter("%(asctime)s | %(levelname)s     | %(module)s:%(funcName)s:%(lineno)d - %(message)s")


fh.setFormatter(formatter)


#将日志输出至文件
logger.addHandler(fh)


logger = logging.getLogger(__name__) """
import json
import qiniu
from .config import get_qiniu_config


config = get_qiniu_config()


def qiniu_upload_token():
    '''生成七牛upload_token'''
    bucket = get_qiniu_config()['bucket']
    access_key = get_qiniu_config()['access_key']
    secret_key = get_qiniu_config()['secret_key']
    policy = {
        "callbackUrl": get_qiniu_config()['callback_url'],
        "callbackBodyType": "application/json",
        "callbackBody": json.dumps({"key":"$(key)","hash":"$(etag)"})
    }
    return qiniu.Auth(access_key, secret_key).upload_token(bucket=bucket, key=None, policy=policy)


def get_qiniu_list():
    '''获取文件列表'''
    bucket = get_qiniu_config()['bucket']
    access_key = get_qiniu_config()['access_key']
    secret_key = get_qiniu_config()['secret_key']
    return qiniu.BucketManager(qiniu.Auth(access_key, secret_key)).list(bucket=bucket)
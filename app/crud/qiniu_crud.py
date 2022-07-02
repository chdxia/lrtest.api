import json
import qiniu
from ..utils.config import get_qiniu_config


bucket = get_qiniu_config()['bucket']
access_key = get_qiniu_config()['access_key']
secret_key = get_qiniu_config()['secret_key']


def get_qiniu_upload_token():
    '''生成七牛upload_token'''
    policy = {
        "callbackUrl": get_qiniu_config()['callback_url'],
        "callbackBodyType": "application/json",
        "callbackBody": json.dumps({"key":"$(key)","hash":"$(etag)"})
    }
    return qiniu.Auth(access_key, secret_key).upload_token(bucket=bucket, key=None, policy=policy)


def get_qiniu_list():
    '''获取七牛文件列表'''
    return qiniu.BucketManager(qiniu.Auth(access_key, secret_key)).list(bucket=bucket)


def delete_qiniu_files(keys=list):
    '''批量删除文件'''
    return qiniu.BucketManager(qiniu.Auth(access_key, secret_key)).batch(qiniu.build_batch_delete(bucket=bucket, keys=keys))
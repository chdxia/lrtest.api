import qiniu
import json
from .config import get_qiniu_config


config = get_qiniu_config()


def qiniu_upload_token(key):
    bucket = get_qiniu_config()['bucket']
    access_key = get_qiniu_config()['access_key']
    secret_key = get_qiniu_config()['secret_key']
    policy = {
        "callbackUrl": get_qiniu_config()['callback_url'],
        "callbackBodyType": "application/json",
        "callbackBody": json.dumps({"key":"$(key)","hash":"$(etag)"})
    }
    return qiniu.Auth(access_key, secret_key).upload_token(bucket, key, 3600, policy)
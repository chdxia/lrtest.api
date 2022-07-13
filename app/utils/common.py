from passlib.hash import sha256_crypt


def get_request_info(request):
    '''获取并返回请求数据'''
    return {
        "host": request.client.host,
        "port": request.client.port,
        "method": request.method,
        "url": request.url,
        "headers": request.headers,
        "cookies": request.cookies
    }


def str_to_sha256(password):
    '''加密'''
    return sha256_crypt.encrypt(password, rounds=5000)


def str_to_selt_sha256(password, salt):
    '''加盐加密'''
    return sha256_crypt.encrypt(password, salt=salt, rounds=5000)

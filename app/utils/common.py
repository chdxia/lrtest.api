from passlib.hash import sha256_crypt


class Common():
    # 获取并返回请求数据
    def get_request_info(request):
        return {
            "host": request.client.host,
            "port": request.client.port,
            "method": request.method,
            "url": request.url,
            "headers": request.headers,
            "cookies": request.cookies
        }


    # 加密
    def str_to_sha256(password):
        return sha256_crypt.encrypt(password, rounds=5000)


    # 加盐加密
    def str_to_selt_sha256(password, salt):
        return sha256_crypt.encrypt(password, salt=salt, rounds=5000)
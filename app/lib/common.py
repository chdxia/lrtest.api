from passlib.hash import sha256_crypt


# 加密
def str_to_sha256(password):
    return sha256_crypt.encrypt(password, rounds=5000)


# 加盐加密
def str_to_selt_sha256(password, salt):
    return sha256_crypt.encrypt(password, salt=salt, rounds=5000)

# 忽略值为None的参数
def ignore_none(**args):
    return {key: value for key, value in args.items() if value is not None}

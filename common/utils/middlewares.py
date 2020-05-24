from flask import request, g

from utils.jwt_util import verify_jwt


def jwt_authentication():
    """
    校验token的请求钩子函数
    :return:
    """
    # 初始化
    g.user_id = None
    g.use_refresh_token = False

    token = request.headers.get('Authorization')

    if token is not None and token.startswith('Bearer '):  # 'Bearer '后面一个空格
        token = token.split(' ')[1]
        # token = token[7:]

        # def verify_jwt(token, secret=None): 调用jwt_token的校验方法
        payload = verify_jwt(token)
        if payload is not None:
            g.user_id = payload.get('user_id')

            # 判断是否为refresh_token
            g.use_refresh_token = payload.get('is_refresh', False)


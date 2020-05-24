from server import sio
from werkzeug.wrappers import Request
import jwt

JWT_SECRET = 'TPmi4aLWRbyVq8zu9v82dWYW17/z+UvRnYTt4P6fAXA'


def verify_jwt(token, secret=None):
    """
    检验jwt
    :param token: jwt
    :param secret: 密钥
    :return: dict: payload
    """
    try:
        payload = jwt.decode(token, secret, algorithm=['HS256'])
    except jwt.PyJWTError:
        payload = None

    return payload


@sio.on('connect', namespace='/notify')
def on_connect(sid, environ):
    """
    与客户端建立链接
    :param sid: 是socketio为当前连接客户端生成的识别id
    :param environ: 在连接握手时客户端发送的握手数据（HTTP报文解析之后的字典）
    :return:
    """
    # 借助werkzeug 工具集 来帮助我们解读 客户端请求的HTTP数据
    request = Request(environ)

    # 解读request对象， 可以像在flask中使用一样来读取数据
    token = request.args.get('token')

    if token is not None:
        payload = verify_jwt(token, secret=JWT_SECRET)
        if payload is not None:
            user_id = payload.get('user_id')

            # 将用户加入用户id名称的房间
            sio.enter_room(sid, str(user_id))


@sio.on('disconnect', namespace='/notify')
def on_disconnect(sid):
    """客户端断开链接"""
    # 查询sid存在的房间rooms列表
    rooms = sio.rooms(sid)

    for room in rooms:
        # 将用户踢出房间
        sio.leave_room(sid, room)

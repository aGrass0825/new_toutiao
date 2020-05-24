from server import sio
import time

# 建立链接
@sio.on('connect')
def on_connect(sid, environ):
    """
       与客户端建立好连接后被执行
       :param sid: string sid是socketio为当前连接客户端生成的识别id
       :param environ: dict 在连接握手时客户端发送的握手数据(HTTP报文解析之后的字典)
    """
    # 发送事件 sio.emit('事件消息类型', '内容', '接收人')
    # 事件消息类型是与前端约定好的(事件名字可以随意定，但要与前端一致)
    data = {
        'msg': 'hello',
        'timestamp': round(time.time() * 1000)
    }
    sio.emit('message_my', data, room=sid)


# 以字符串的形式表示一个自定义事件，事件的定义由前后端约定
@sio.on('message_my')
def on_message(sid, data):
    """
    自定义事件消息的处理方法
    :param sid: string sid是发送此事件消息的客户端id
    :param data: data是客户端发送的消息数据
    前端发送的数据data格式也是
    {
        'msg':xxx,
        'timestamp':xxxx
    }
    """
    # TODO 此处使用RPC调用聊天机器人子系统，获取聊天回复的内容
    qq_data = {
        'msg': '{}'.format(data.get('msg')),
        'timestamp': round(time.time() * 1000)
    }
    # sio.send(req_data, room=sid)
    # 当事件消息类型是message类型时，可以简写sio.send('内容', '接受人')
    print(sid)
    print(data)
    sio.emit('message_my', qq_data, room=sid)
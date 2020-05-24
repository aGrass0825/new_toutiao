import socketio

# 链接rabbitmq数据库地址
RABBITMQ = 'amqp://python:rabbitmqpwd@localhost:5672/toutiao'

# 链接rabbitmq数据库
mgr = socketio.KombuManager(RABBITMQ)

sio = socketio.Server(async_handlers='eventlet', client_manager=mgr)  # 告诉socketio服务器使用的是eventlet协程库
app = socketio.Middleware(sio)

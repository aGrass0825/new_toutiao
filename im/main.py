import sys
import eventlet
eventlet.monkey_patch()

import eventlet.wsgi
from server import app
import chat
import notify
"""
IM服务器的启动程序
"""

# 端口优化
if len(sys.argv) < 2:  # sys.argv--> ['main.py', '端口号']
    print('Usage: python main.py [port]!')
    exit(1)
port = int(sys.argv[1])

# 创建eventlet服务器对象
SERVER_ADDRESS = ('0.0.0.0', port)
listen_socket = eventlet.listen(SERVER_ADDRESS)
eventlet.wsgi.server(listen_socket, app)

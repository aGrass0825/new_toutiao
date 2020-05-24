from flask import current_app

import qiniu.config
from qiniu import Auth, put_file, etag, put_data


def upload(file_data):  # file_data为上传二进制流(二进制文件)
    # 需要填写你的 Access Key 和 Secret Key
    access_key = current_app.config['QINIU_ACCESS_KEY']
    secret_key = current_app.config['QINIU_SECRET_KEY']

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = current_app.config['QINIU_BUCKET_NAME']
    # bucket_name = 'wh20toutiao'

    # 上传后保存的文件名
    key = None  # key为None时由七牛自动生成

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600000)

    # 要上传文件的本地路径
    # localfile = './sync/bbb.jpg'
    # ret, info = put_file(token, key, localfile)

    ret, info = put_data(token, key, file_data)

    # print('ret={}'.format(ret))
    # print('info={}'.format(info))
    # assert ret['key'] == key
    # assert ret['hash'] == etag(localfile)
    return ret['key']
import grpc
import time

import reco_pb2_grpc
import reco_pb2


def run():
    """
    客户端调用的运行
    :return:
    """
    with grpc.insecure_channel('127.0.0.1:8888') as channel:
        # 创建用户进行rpc调用的工具
        stub = reco_pb2_grpc.UserRecommendStub(channel)

        rr = reco_pb2.UserRequest()
        rr.user_id = 1
        rr.channel_id = 11
        rr.article_num = 22
        rr.time_stamp = round(time.time() * 1000)

        ret = stub.user_recommend(rr)
        print('ret={}'.format(ret))


if __name__ == '__main__':
    run()

import time

import grpc
from concurrent.futures import ThreadPoolExecutor
import reco_pb2_grpc
import reco_pb2


class UserRecommendServicer(reco_pb2_grpc.UserRecommendServicer):
    """
    声明RPC调用的服务
    """

    def user_recommend(self, request, context):
        """
        用户文章推荐，实际是由推荐系统编写
        :param request: rpc调用的请求数据对象，UserRequest对象
        :param context: 错误信息和状态
        :return:
        """
        # 伪推荐   --> 获取rpc调用的请求参数
        user_id = request.user_id
        channel_id = request.channel_id
        article_num = request.article_num
        time_stamp = request.time_stamp

        # 构建调用返回值对象
        response = reco_pb2.ArticleResponse()
        response.exposure = 'exposure.....'
        response.time_stamp = round(time.time() * 1000)

        articles_list = []
        for i in range(article_num):
            article = reco_pb2.Article()
            article.article_id = i + 1
            article.track.click = 'click==='
            article.track.collect = 'collect+++'
            article.track.liking = 'liking****'
            article.track.read = 'read'
            articles_list.append(article)

        response.recommends.extend(articles_list)
        return response


def serve():
    """RPC服务运行程序， 启动后可以等待接受rpc的调用请求"""
    # 创建RPC服务器对象
    server = grpc.server(ThreadPoolExecutor(max_workers=10))

    # 将RPC的具体函数代码交给RPC服务器对接
    reco_pb2_grpc.add_UserRecommendServicer_to_server(UserRecommendServicer(), server)

    # 为服务器绑定端口和ip地址
    server.add_insecure_port('127.0.0.1:8888')

    # 启动服务器运行
    server.start()  # 由于是非阻塞的

    while True:
        time.sleep(10)


if __name__ == '__main__':
    serve()

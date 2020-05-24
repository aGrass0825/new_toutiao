
import time

from flask import current_app, g
from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser

from cache import article as cache_article  # 起别名

from rpc import reco_pb2, reco_pb2_grpc
from toutiao.resources.news import constants
from utils import parser


class ArticleListResource(Resource):
    """
    获取推荐文章列表数据
    """
    def _feed_articles(self, channel_id, timestamp, feed_count):
        """
        RPC调用获取推荐文章
        :param channel_id: 频道id
        :param feed_count: 推荐数量
        :param timestamp: 时间戳
        :return: [{article_id, trace_params}, ...], timestamp
        """
        # 创建用户进行rpc调用的工具
        stub = reco_pb2_grpc.UserRecommendStub(current_app.rpc_reco)

        rr = reco_pb2.UserRequest()
        rr.user_id = str(g.user_id) if g.user_id else 'Anonymous'
        rr.channel_id = channel_id
        rr.article_num = feed_count
        rr.time_stamp = timestamp

        ret = stub.user_recommend(rr)
        pre_timmestamp = ret.time_stamp
        feed_articles = ret.recommends
        return feed_articles, pre_timmestamp

    def get(self):
        """
        获取文章列表
        """
        qs_parser = RequestParser()
        qs_parser.add_argument('channel_id', type=parser.channel_id, required=True, location='args')
        qs_parser.add_argument('timestamp', type=inputs.positive, required=True, location='args')
        args = qs_parser.parse_args()
        channel_id = args.channel_id
        timestamp = args.timestamp
        per_page = constants.DEFAULT_ARTICLE_PER_PAGE_MIN
        try:
            feed_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
        except Exception:
            return {'message': 'timestamp param error'}, 400

        results = []

        # 获取推荐文章列表
        feeds, pre_timestamp = self._feed_articles(channel_id, timestamp, per_page)

        # 查询文章
        for feed in feeds:
            article = cache_article.ArticleInfoCache(feed.article_id).get()
            if article:
                article['pubdate'] = feed_time
                article['trace'] = {
                    'click': feed.track.click,
                    'collect': feed.track.collect,
                    # 'share': feed.track.share,
                    'read': feed.track.read
                }
                results.append(article)

        return {'pre_timestamp': pre_timestamp, 'results': results}
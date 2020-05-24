from flask import current_app

from rediscluster.exceptions import RedisError
from sqlalchemy import func
from models import db
from models.news import Article, Attitude, Collection, CommentLiking, Comment
from models.user import Relation


# 由于不仅仅只统计一个字段的数量(文章数量、点赞数量、粉丝数量...)都会用到下面的方法-->封装


class CountStorageBase(object):
    """数量存储工具类"""
    key = ''

    @classmethod
    def get(cls, member_id):
        """
        查询指定数量
        :param member_id:
        :return:
        """
        try:
            count = current_app.redis_master.zscore(cls.key, member_id)  # zscore(k, v)查出有序集合中的权重
        except RedisError as e:
            current_app.logger.error(e)
            count = current_app.redis_slave.zscore(cls.key, member_id)

        return 0 if count is None else int(count)  # 三目运算

    @classmethod
    def incr(cls, member_id, increment=1):
        """
        累计数量
        :param increment: 累计值（类似步长） 可以正数或负数
        :param member_id: 用户ID
        :return:
        """
        try:
            current_app.redis_master.zincrby(cls.key, increment, member_id)  # zincrby(k, s, v)增加或者减少
        except RedisError as e:
            current_app.logger.error(e)
            raise e

    @classmethod
    def reset(cls, db_query_result):
        """重置redis数据"""

        # 删除redis的记录
        r = current_app.redis_master
        r.delete(cls.key)

        # 将数据库的数据保存到redis中
        # 方法一 ---->管道
        # pl = r.pipeline()
        # for user_id, count in ret:
        #     pl.zadd(key, count, user_id)
        # pl.execute()
        # 方法二
        redis_list = []
        for user_id, count in db_query_result:  # db_query_result-->[(1, 46141), (2, 46357), (3, 46187), (5, 25)]
            redis_list.append(count)  # count 一定要在上面，由zadd()里面的顺序决定的
            redis_list.append(user_id)

        # zadd(key, count, user_id)
        r.zadd(cls.key, *redis_list)  # *可以拆列表和元组 **可以拆字典

    @staticmethod
    def db_query():
        """用来修正redis数据库先查询sql"""
        pass


class UserArticlesCountStorage(CountStorageBase):
    """用户文章数量存储工具类"""
    key = 'count:user:arts'

    @staticmethod
    def db_query():
        """查询用户文章数量sql方法"""
        result = db.session.query(Article.user_id, func.count(Article.id)).filter(
            Article.status == Article.STATUS.APPROVED) \
            .group_by(Article.user_id).all()
        return result


class UserFollowingsCountStorage(CountStorageBase):
    """用户关注数量工具类"""
    key = 'count:user:follows'

    @staticmethod
    def db_query():
        """查询用户文章数量sql方法"""
        result = db.session.query(Relation.user_id, func.count(Relation.target_user_id)).filter(
            Relation.relation == Relation.RELATION.FOLLOW) \
            .group_by(Relation.user_id).all()
        return result


class UserFansCountStorage(CountStorageBase):
    """用户粉丝数量工具类"""
    key = 'count:user:fans'


class UserLikingCountStorage(CountStorageBase):
    """用户点赞数量工具类"""
    key = 'count:user:liking'


class ArticleLikingCountStorage(CountStorageBase):
    """
    文章点赞数据
    """
    key = 'count:art:liking'

    @classmethod
    def db_query(cls):
        ret = db.session.query(Attitude.article_id, func.count(Collection.article_id)) \
            .filter(Attitude.attitude == Attitude.ATTITUDE.LIKING).group_by(Collection.article_id).all()
        return ret


class CommentLikingCountStorage(CountStorageBase):
    """
    评论点赞数据
    """
    key = 'count:comm:liking'

    @classmethod
    def db_query(cls):
        ret = db.session.query(CommentLiking.comment_id, func.count(CommentLiking.comment_id)) \
            .filter(CommentLiking.is_deleted == 0).group_by(CommentLiking.comment_id).all()
        return ret


class ArticleCollectingCountStorage(CountStorageBase):
    """
    文章收藏数量
    """
    key = 'count:art:collecting'

    @classmethod
    def db_query(cls):
        ret = db.session.query(Collection.article_id, func.count(Collection.article_id)) \
            .filter(Collection.is_deleted == 0).group_by(Collection.article_id).all()
        return ret


class ArticleCommentCountStorage(CountStorageBase):
    """
    文章评论数量
    """
    key = 'count:art:comm'

    @classmethod
    def db_query(cls):
        ret = db.session.query(Comment.article_id, func.count(Comment.id)) \
            .filter(Comment.status == Comment.STATUS.APPROVED).group_by(Comment.article_id).all()
        return ret

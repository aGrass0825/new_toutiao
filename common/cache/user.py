import json
from flask import current_app
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import load_only
from rediscluster.exceptions import RedisError

from cache.constants import UserProfileCacheTTL, UserProfileNotExistsCacheTTL
from models.user import User

"""
需求：
1.查询用户资料数据
2.清理用户资料数据缓存
3.判断用户是否存在
"""


class UserProfileCache(object):
    """用户资料缓存数据工具类"""

    def __init__(self, user_id):
        self.key = 'user:{}:profile'.format(user_id)  # key表示这个工具需要操作redis键名
        self.user_id = user_id

    def save(self):
        """如果redis中没有查到数据-->数据库查，保存到redis中，返回"""
        r = current_app.redis_cluster  # 链接redis分布式集群
        try:
            user = User.query.options(load_only(
                User.mobile,
                User.name,
                User.profile_photo,
                User.introduction,
                User.certificate
            )).filter_by(id=self.user_id).first()
        except DatabaseError as e:
            current_app.logger.error(e)
            raise e

        if user is not None:
            # 数据库中查到了数据-->保存到redis中，返回
            user_dict = {
                'mobile': user.mobile,
                'name': user.name,
                'photo': user.profile_photo,
                'intr': user.introduction,
                'certi': user.certificate
            }
            user_json = json.dumps(user_dict)
            try:
                # 保存到redis中是以string保存的
                r.setex(self.key, UserProfileCacheTTL.get_val(), user_json)
            except RedisError as e:
                current_app.logger.error(e)

            # 返回
            return user_dict
        else:
            try:
                # 如果数据库没有查到数据，为了防护缓存穿透，保存redis记录(-1),返回
                r.setex(self.key, UserProfileNotExistsCacheTTL.get_val(), '-1')
            except RedisError as e:
                current_app.logger.error(e)
            # 返回
            return None

    def get(self):
        """查询用户资料数据方法"""
        # 查询redis的缓存数据
        r = current_app.redis_cluster  # 链接redis分布式集群
        try:
            ret = r.get(self.key)
        except RedisError as e:
            # 记录错误信息
            current_app.logger.error(e)
            # 为了从数据库查询数据，所以设置ret=None,让代码进入数据库中查询
            ret = None

        if ret is not None:
            # 如果redis中查询到数据->返回
            if ret == b'-1':  # 以'b'定义字符串为bytes类型
                # 表示用户不存在
                return None
            else:
                # 表示用户存在
                user_dict = json.loads(ret)
                return user_dict
        else:
            # 如果redis中没有查到数据-->数据库查，保存到redis中，返回
            return self.save()

    def clear(self):
        """清理用户资料数据缓存方法"""
        r = current_app.redis_cluster  # 链接redis分布式集群
        try:
            r.delete(self.key)
        except RedisError as e:
            current_app.logger.error(e)

    def determine_user_exists(self):
        """判断用户是否存在"""
        # 查询redis记录
        r = current_app.redis_cluster
        try:
            ret = r.get(self.key)
        except RedisError as e:
            current_app.logger.error(e)
            ret = None

        if ret is not None:
            # 如果redis存在数据-->返回
            if ret == b'-1':
                # 表示用户不存在
                return False
            else:
                return True
        else:
            # 如果redis不存在数据-->查询数据库
            result = self.save()
            if result is not None:
                return True
            else:
                return False

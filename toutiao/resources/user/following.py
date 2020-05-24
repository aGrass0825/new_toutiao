from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import IntegrityError
from flask import g, current_app
# from flask_restful import inputs
import time

from utils.decorators import login_required
from models.user import Relation, User
from utils import parser
from models import db
from cache import user as cache_user
# from cache import statistic as cache_statistic
# from . import constants


class FollowingListResource(Resource):
    """
    关注用户
    """
    method_decorators = {
        'post': [login_required],
        'get': [login_required],
    }

    def post(self):
        """
        关注用户
        """
        # 关注用户的数据库保存
        json_parser = RequestParser()
        json_parser.add_argument('target', type=parser.user_id, required=True, location='json')
        args = json_parser.parse_args()
        target = args.target
        if target == g.user_id:
            return {'message': 'User cannot follow self'}, 400
        ret = 1
        try:
            follow = Relation(user_id=g.user_id, target_user_id=target, relation=Relation.RELATION.FOLLOW)
            db.session.add(follow)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            ret = Relation.query.filter(Relation.user_id == g.user_id,
                                        Relation.target_user_id == target,
                                        Relation.relation != Relation.RELATION.FOLLOW)\
                .update({'relation': Relation.RELATION.FOLLOW})
            db.session.commit()

        # if ret > 0:
        #     tiemstamp = time.time()
        #     cache_user.UserFollowingCache(g.user_id).update(target, tiemstamp)
        #     cache_user.UserFollowingCache(target).update(g.user_id, tiemstamp)
        #     cache_statistic.UserFollowingsCountStorage.incr(g.user_id)
        #     cache_statistic.UserFollowersCountStorage.incr(target)
        #     cache_user.UserRelationshipCache(g.user_id).clear()

        # 发送关注通知
        _user = cache_user.UserProfileCache(g.user_id).get()
        _data = {
            'user_id': g.user_id,
            'user_name': _user['name'],
            'user_photo': _user['photo'],
            'timestamp': int(time.time())
        }
        current_app.sio_mgr.emit('following notify', data=_data, room=str(target))  # target指的是被关注用户的id

        return {'target': target}, 201
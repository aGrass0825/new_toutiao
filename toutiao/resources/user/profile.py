from flask import g, current_app
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from models import db
from models.user import User
from utils.decorators import login_required
from utils import parser
from utils.qiniu_storage import upload
from cache import user as cache_user
from cache import statistic as cache_statistic

class PhotoResource(Resource):
    # 强制为登录的用户才能访问
    method_decorators = [login_required]

    def patch(self):
        # 校验参数
        re = RequestParser()
        re.add_argument('photo', type=parser.check_image, required=True, location='files')
        req = re.parse_args()
        image_file = req.photo

        # 业务处理：上传图片
        image_data = image_file.read()  # image_data必须是二进制才行
        file_name = upload(image_data)

        # 保存图片地址
        User.query.filter(User.id == g.user_id).update({'profile_photo': file_name})
        db.session.commit()

        # 返回结果
        photo_url = current_app.config['QINIU_DOMAIN'] + file_name
        return {'photo_url': photo_url}, 201


class UserResource(Resource):
    """用户资料接口"""
    def get(self, user_id):
        # 校验参数
        cache_tool = cache_user.UserProfileCache(user_id)
        if not cache_tool.determine_user_exists():
            # 用户不存在
            return {'message': 'User does not exits'}, 400
        else:
            # 用户存在 查询用户信息
            user_dict = cache_tool.get()
            del user_dict['mobile']
            user_dict['user_id'] = user_id
            user_dict['photo'] = current_app.config['QINIU_DOMAIN'] + user_dict['photo']
            # TODO 统计稍好处理
            user_dict['article_count'] = cache_statistic.UserArticlesCountStorage.get(user_id)
            user_dict['follows_count'] = cache_statistic.UserFollowingsCountStorage.get(user_id)
            user_dict['fans_count'] = cache_statistic.UserFansCountStorage.get(user_id)
            user_dict['liking_count'] = cache_statistic.UserLikingCountStorage.get(user_id)

        # 返回
        return user_dict



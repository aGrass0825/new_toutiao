from cache import statistic as cache_statistic


def __fix_process(storage_tool_class):
    ret = storage_tool_class.db_query()
    storage_tool_class.reset(ret)


def fix_statistics(flask_app):
    """修正统计数据的定时任务(方法)"""

    # 构造上下文环境
    with flask_app.app_context():
        # (用户文章数量)查询数据库，获取统计数据
        # select user_id, count(article_id)  form news_article_basic where status=2 group by user_id;
        # +---------+-------------------+
        # | user_id | count(article_id) |
        # +---------+-------------------+
        # |       1 |             46141 |
        # |       2 |             46357 |
        # |       3 |             46187 |
        # |       5 |                25 |
        # +---------+-------------------+
        # 用户文章数量
        __fix_process(cache_statistic.UserArticlesCountStorage)

        # 用户关注数量
        __fix_process(cache_statistic.UserFollowingsCountStorage)

        # # 用户粉丝数量
        # __fix_process(cache_statistic.UserFansCountStorage)
        #
        # # 用户点赞数量
        __fix_process(cache_statistic.ArticleLikingCountStorage)
        #
        # # 文章收藏数量
        __fix_process(cache_statistic.ArticleCollectingCountStorage)


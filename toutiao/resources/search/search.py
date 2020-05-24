from flask import current_app
from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser

from models.news import Article
from . import constants
from cache import article as cache_article


class SearchResource(Resource):
    """搜索结果"""

    def get(self):
        """获取搜索结果"""
        qs_parser = RequestParser()
        qs_parser.add_argument('q', type=inputs.regex(r'^.{1,50}$'), required=True, location='args')
        qs_parser.add_argument('page', type=inputs.positive, required=False, location='args')
        qs_parser.add_argument('per_page', type=inputs.int_range(constants.DEFAULT_SEARCH_PER_PAGE_MIN,
                                                                 constants.DEFAULT_SEARCH_PER_PAGE_MAX, 'per_page'),
                               required=False, location='args')
        args = qs_parser.parse_args()
        q = args.q
        page = 1 if args.page is None else args.page
        per_page = args.per_page if args.per_page else constants.DEFAULT_SEARCH_PER_PAGE_MIN

        # 查询es (组合查询)
        query_dict = {
            "from": per_page * (page - 1),
            "size": per_page,
            "_source": ["article_id", "title"],
            "query": {
                "bool": {
                    "must": {
                        "match": {
                            "_all": q
                        }
                    },
                    "filter": {
                        "term": {
                            "status": Article.STATUS.APPROVED
                        }
                    }
                }
            }
        }

        # es.search(index=库名, doc_type=表名, body=查询条件)
        ret = current_app.es.search(index='articles', doc_type='article', body=query_dict)

        total_count = ret['hits']['total']
        results = []

        for item in ret['hits']['hits']:
            article_id = item['_id']
            article_dict = cache_article.ArticleInfoCache(article_id).get()

            if article_dict:
                results.append(article_dict)

        return {"page": page, "per_page": per_page, "total_count": total_count, "results": results}

    # 返回给前端接口的样式
    # {
    #     "message": "OK",
    #     "data": {
    #         "page": xx,
    #         "per_page": xx,
    #         "total_count": xx,
    #         "results": [
    #             {
    #                 "article_id": xx,
    #                 "title": xx,
    #                 "cover": xx
    #             },
    #             ...
    #         ]
    #     }
    # }


class SuggestionResource(Resource):
    """实现提示和自动补全功能"""
    def get(self):
        """
        获取联想建议
        """
        qs_parser = RequestParser()
        qs_parser.add_argument('q', type=inputs.regex(r'^.{1,50}$'), required=True, location='args')
        args = qs_parser.parse_args()
        q = args.q

        # 先尝试自动补全建议查询
        query = {
            'from': 0,
            'size': 10,
            '_source': False,
            'suggest': {
                'word-completion': {
                    'prefix': q,
                    'completion': {
                        'field': 'suggest'
                    }
                }
            }
        }
        ret = current_app.es.search(index='completions', body=query)
        options = ret['suggest']['word-completion'][0]['options']

        # 如果没得到查询结果，进行纠错建议查询
        if not options:
            query = {
                'from': 0,
                'size': 10,
                '_source': False,
                'suggest': {
                    'text': q,
                    'word-phrase': {
                        'phrase': {
                            'field': '_all',
                            'size': 1
                        }
                    }
                }
            }
            ret = current_app.es.search(index='articles', doc_type='article', body=query)
            options = ret['suggest']['word-phrase'][0]['options']

        results = []
        for option in options:
            if option['text'] not in results:
                results.append(option['text'])

        return {'options': results}
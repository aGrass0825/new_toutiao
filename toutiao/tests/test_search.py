import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(BASE_DIR, 'common'))  # 保证from setting import testing导包路径正确
sys.path.insert(0, BASE_DIR)  # 保证from toutiao import create_app 导包路径正确

import unittest
from toutiao import create_app
from settings import testing
import json

class TestSearchResource(unittest.TestCase):
    """测试搜索视图模块"""

    def setUp(self):
        """测试前初始化"""
        # from toutiao.main import app -->app = create_app(DefaultConfig, enable_config_file=True)
        # self.client = app.test_client()   由于app是在DefaultConfig配置中，测试配置是在TestingConfig中，所以不能直接使用
        app = create_app(testing.TestingConfig)
        self.client = app.test_client()

    def test_normal_request(self):
        """正常情况测试"""
        resp = self.client.get('/v1_0/search?q=python')
        # assert resp.status_code == 200
        self.assertEqual(resp.status_code, 200)

        resp_dict = json.loads(resp.data)  # resp.data是json字符串，故转换成字典才能操作。
        # assert "message" in resp_dict
        # assert "data" in resp_dict
        self.assertIn("message", resp_dict)
        self.assertIn("data", resp_dict)

        data = resp_dict['data']
        self.assertIn("page", data)
        self.assertIn("results", data)

    def test_missing_q_param_error(self):
        """测试没有q参数情况"""
        resp = self.client.get('/v1_0/search')
        self.assertEqual(resp.status_code, 400)

    def test_q_length_error(self):
        """测试q参数长度错误的情况"""
        q = 'a' * 49
        resp = self.client.get(f'/v1_0/search?q={q}')
        self.assertEqual(resp.status_code, 400)

    def tearDown(self):
        """该方法会在测试代码执行完后执行，相当于做测试后的扫尾工作"""
        pass


if __name__ == '__main__':
    unittest.main()

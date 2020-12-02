# coding=utf-8
"""
作者：vissy@zhu
"""

import unittest
from commonlib.confighttp import ConfigHttp
from testdata.api_data import api_homepage
from testdata.common_data import common_data
from commonlib.connectdb import connectdb

confighttp = ConfigHttp()


class Test_GetAppSearchPage(unittest.TestCase):
    '''
    首页搜索'胃肠道'
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetAppSearchPage, self).__init__(*args)
        self.url = api_homepage['getAppSearchPage']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_getAppSearchPage(self):
        data = {
            "centerSize": 3,
            "docSize": 2,
            "hospitalSize": 2,
            "param": "胃肠道"
        }
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        # 结果验证
        self.assertEqual(self.response['status'], 0, '接口连接正常')
        self.assertIn('胃肠道', self.response['result']['centers'][0]['name'], '搜索返回的数据错误')
        self.assertLessEqual(1, self.response['result']['centers'][0]['id'], '搜索未返回中心id')
        self.assertIn('liangyihui.net', self.response['result']['centers'][0]['iconUrl'], '中心icon未返回')

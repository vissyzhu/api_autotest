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


class Test_GetBannerList(unittest.TestCase):
    '''
    首页banner列表
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetBannerList, self).__init__(*args)
        self.url = api_homepage["getBannerList"]  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_getbannerlist(self):
        data = {
            "type": 1
        }
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        # 结果验证
        self.assertEqual(self.response['status'], 0, "接口连接错误")
        self.assertLessEqual(1, self.response['result'][0]['id'], '首页banner返回的id不对')
        self.assertIn('http', self.response['result'][0]['picUrl'], '首页banner地址返回不对')
        self.assertLessEqual(1, len(self.response['result']), '首页banner未返回')

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


class Test_GetAreaTree(unittest.TestCase):
    '''
    找专家页的地区列表
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetAreaTree, self).__init__(*args)
        self.url = api_homepage['getAreaTree']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_getAreaTree(self):
        self.auth = common_data['Authorization']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        # 结果验证
        self.assertEqual(self.response['status'], 0, '接口连接错误')
        self.assertEqual('110000', self.response['result'][0]['areaCode'], '北京的地区码错误')
        self.assertIn('北京', self.response['result'][0]['areaName'], '城市名返回错误')
        self.assertIn('区', self.response['result'][0]['childrens'][0]['areaName'], '二级数据未返回')
        self.assertLessEqual(31, len(self.response['result']), '城市数据返回不全')


if __name__ == '__main__':
    t = Test_GetAreaTree()
    t.test_getAreaTree()

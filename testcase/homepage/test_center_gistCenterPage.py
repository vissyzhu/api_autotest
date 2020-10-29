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


class Test_GistCenterPage(unittest.TestCase):
    '''
    首页搜索按钮，推荐中心
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GistCenterPage, self).__init__(*args)
        self.url = api_homepage['gistCenterPage']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_gistCenterPage(self):
        data = {
            "index": 1,
            "param": "",
            "size": 4
        }
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        # 结果验证
        self.assertEqual(self.response['status'], 0, "数据连接错误")
        self.assertLessEqual(1, self.response['result']['records'][0]['id'], '单病种中心id未返回')
        self.assertNotEqual(None, self.response['result']['records'][0]['name'], '单病种中心名称未返回')
        self.assertIn('liangyihui.net', self.response['result']['records'][0]['iconUrl'], '单病种中心icon未返回')
        self.assertLessEqual(1,len(self.response['result']['records']),  '未返回推荐中心数据')


if __name__ == '__main__':
    t = Test_GistCenterPage()
    t.test_gistCenterPage()

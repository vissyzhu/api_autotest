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


class Test_GistCenterDocuments(unittest.TestCase):
    '''
    首页患者指南
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GistCenterDocuments, self).__init__(*args)
        self.url = api_homepage['gistCenterDocuments']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_gistCenterDocuments(self):
        data = {
            "index": 1,
            "size": 8,
            "all": True,
            "app": True
        }
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        # 结果验证
        self.assertEqual(self.response['status'], 0, "接口连接错误")
        self.assertLessEqual(1, self.response['result']['records'][0]['id'], '单病种中心文章未返回')
        self.assertNotEqual(None, self.response['result']['records'][0]['title'], '单病种中心文章标题未返回')
        self.assertIn('http://bosdev.liangyihui.net', self.response['result']['records'][0]['picurl'], '单病种中心文章图片未返回')
        self.assertLessEqual(1, self.response['result']['records'][0]['readCount'], '单病种中心文章的浏览数不对')
        self.assertLessEqual(5, len(self.response['result']['records']), '单病种中心文章的数量返回不对')


if __name__ == '__main__':
    t = Test_GistCenterDocuments()
    t.test_gistCenterDocuments()

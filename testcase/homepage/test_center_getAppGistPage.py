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


class Test_getAppGistPage(unittest.TestCase):
    '''
    单病种中心页
    '''

    def __init__(self, *args, **kwargs):
        super(Test_getAppGistPage, self).__init__(*args)
        self.url = api_homepage['getAppGistPage']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中
        self.centerId = common_data['centerId']

    def test_getAppGistPage(self):
        self.auth = common_data['Authorization']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "centerId": "%s" % self.centerId,
            "teamSize": 4,
            "docSize": 4,
            "overseaDocSize": 2,
            "hospitalSize": 2
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        # 结果验证
        self.assertEqual(self.response['status'], 0, "接口连接错误")
        self.assertEqual(5, self.response['result']['center']['id'], '单病种id返回错误')
        self.assertEqual('胃肠道间质瘤', self.response['result']['center']['name'], '单病种中心名称返回错误')
        self.assertLessEqual(1, len(self.response['result']['doctors']), '该单病种中心下专家数据未返回')
        self.assertLessEqual(1, self.response['result']['doctors'][0]['doctorId'], '该单病种中心专家id未返回')
        self.assertNotEqual(None, self.response['result']['doctors'][0]['name'], '该单病种中心医生名称未返回')
        self.assertIn('间质瘤', self.response['result']['doctors'][0]['disease'], '该单病种中心下专家擅长的瘤种不对')

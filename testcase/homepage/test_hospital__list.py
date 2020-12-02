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


class Test_HospitalList(unittest.TestCase):
    '''
    肿瘤名院列表
    '''

    def __init__(self, *args, **kwargs):
        super(Test_HospitalList, self).__init__(*args)
        self.url = api_homepage['hospitallist']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_hospitallist(self):
        self.auth = common_data['Authorization']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "index": 1,
            "size": 8,
            "isFamous": "1"
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        common_data['hospitalId'] = self.response['result']['records'][0]['id']
        self.check_result()

    def check_result(self):
        # 结果验证
        self.assertEqual(self.response['status'], 0, "接口连接错误")
        self.assertLessEqual(1, self.response['result']['records'][0]['id'], '医院的id号不对')
        self.assertNotEqual(None, self.response['result']['records'][0]['name'], '医院姓名未返回')
        self.assertIn('liangyihui.net', self.response['result']['records'][0]['picUrl'], '医院头像未返回')
        self.assertNotEqual(None, self.response['result']['records'][0]['address'], '医院地址未返回')
        self.assertLessEqual(1, len(self.response['result']['records']), '医院列表无数据')

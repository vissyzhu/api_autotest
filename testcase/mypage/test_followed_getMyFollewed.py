# coding=utf-8
"""
作者：vissy@zhu
"""

import unittest
from commonlib.confighttp import ConfigHttp
from testdata.api_data import api_mypage
from testdata.common_data import common_data
from commonlib.connectdb import connectdb

confighttp = ConfigHttp()


class Test_GetMyFollowed(unittest.TestCase):
    '''
    我的关注页，医院和科室列表
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetMyFollowed, self).__init__(*args)
        self.url = api_mypage['getMyFollowed']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    # 医院列表
    def test_getMyFollowed_hospital(self):
        self.auth = common_data['Authorization']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "category": 1
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()
        self.assertNotEqual(None, self.response['result'][0]['disease'], '我关注的医院擅长瘤种未显示')

    # 科室列表
    def test_getMyFollowed_dept(self):
        self.auth = common_data['Authorization']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "category": 2
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()
        self.assertNotEqual(None, self.response['result'][0]['dept'], '我关注的科室名称未返回')

    def check_result(self):
        # 结果验证
        self.assertEqual(self.response['status'], 0, '接口连接错误')
        self.assertNotEqual(None, self.response['result'][0]['hospital'], '我关注的医院名未显示')
        # self.assertIn('liangyihui', self.response['result'][0]['picUrl'], '我关注医院/科室的头图未显示')

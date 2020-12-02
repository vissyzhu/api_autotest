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


class Test_GetPatientPayList(unittest.TestCase):
    '''
    我的订单列表
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetPatientPayList, self).__init__(*args)
        self.url = api_mypage['getPatientPayList']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    # 问诊列表
    def test_getPatientPayList(self):
        self.auth = common_data['Authorization']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "index": 1,
            "size": 8,
            "type": 1
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()
        self.assertIn(self.response['result']['records'][0]['inType'], (0, 1, 2, 3), '问诊类型未返回')
        self.assertLessEqual(0, self.response['result']['records'][0]['inStatus'], '订单状态未返回')

    # 答疑列表
    def test_getPatientPayList_ask(self):
        self.auth = common_data['Authorization']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "index": 1,
            "size": 8,
            "type": 2
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()
        self.assertLessEqual(0, self.response['result']['records'][0]['status'], '订单状态未返回')

    def check_result(self):
        # 结果验证
        self.assertEqual(self.response['status'], 0, '接口连接错误')
        self.assertNotEqual(None, self.response['result']['records'][0]['doctorName'], '问诊的医生名未显示')
        self.assertNotEqual(None, self.response['result']['records'][0]['patientName'], '就诊人姓名未显示')
        self.assertIn(self.response['result']['records'][0]['gender'], (1, 2), '就诊人性别未显示')
        self.assertNotEqual(None, self.response['result']['records'][0]['disease'], '就诊人的疾病未显示')
        self.assertLessEqual(0, self.response['result']['records'][0]['amount'], '订单金额不对')
        self.assertLessEqual(1, len(self.response['result']['records']), '订单列表数据返回不全')

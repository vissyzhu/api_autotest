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


class Test_GetPrePage(unittest.TestCase):
    '''
    我的处方列表
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetPrePage, self).__init__(*args)
        self.url = api_mypage['getPrePage']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_getPrePage(self):
        self.auth = common_data['Authorization']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "index": 1,
            "size": 8
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        common_data['prescriptionSn']=self.response['result']['records'][0]['id']
        self.check_result()

    def check_result(self):
        # 结果验证
        self.assertEqual(self.response['status'], 0, '接口连接错误')
        self.assertNotEqual(None, self.response['result']['records'][0]['prescriptionSn'], '处方号不对')
        self.assertNotEqual(None, self.response['result']['records'][0]['doctorName'], '医生姓名未显示')
        self.assertNotEqual(None, self.response['result']['records'][0]['result'], '诊断结果未显示')
        self.assertNotEqual(None, self.response['result']['records'][0]['prescriptionDrugs'][0]['drugName'], '药品名称未显示')
        self.assertLessEqual(1, len(self.response['result']['records']), '处方数据显示不全')


if __name__ == '__main__':
    t = Test_GetPrePage()
    t.test_getPrePage()

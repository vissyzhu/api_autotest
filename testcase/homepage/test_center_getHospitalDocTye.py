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


class Test_GetHospitalDocType(unittest.TestCase):
    '''
    单病种中心文章类型
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetHospitalDocType, self).__init__(*args)
        self.url = api_homepage['getHospitalDocType']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_getHospitalDocType(self):
        self.auth = common_data['Authorization']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        confighttp.set_data(header)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        # 结果验证
        self.assertEqual(self.response['status'], 0, "接口连接错误")
        self.assertEqual('前沿动态', self.response['result'][0]['name'], '单病种中心标签未显示')
        self.assertLessEqual(3, len(self.response['result']), '单病种中心标签数据返回不全')

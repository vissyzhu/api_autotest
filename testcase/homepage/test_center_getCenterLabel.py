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


class Test_GetCenterLabel(unittest.TestCase):
    '''
    单病种中心标签类型-胃肠间质瘤为例
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetCenterLabel, self).__init__(*args)
        self.url = api_homepage['getCenterLabel']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中
        self.centerId = common_data['centerId']

    def test_getCenterLabel(self):
        self.auth = common_data['Authorization']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }

        data = {
            "id": "%s" % self.centerId
        }
        confighttp.set_data(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        # 结果验证
        self.assertEqual(self.response['status'], 0, "接口连接错误")
        self.assertEqual('前沿动态', self.response['result'][0]['name'], '单病种中心标签未显示')
        self.assertLessEqual(3, len(self.response['result']), '单病种中心标签数据返回不全')

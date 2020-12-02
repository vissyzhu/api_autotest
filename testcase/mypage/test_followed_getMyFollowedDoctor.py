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


class Test_GetMyFollowedDoctor(unittest.TestCase):
    '''
    我的关注-医生列表
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetMyFollowedDoctor, self).__init__(*args)
        self.url = api_mypage['getMyFollowedDoctor']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_getMyFollowedDoctor(self):
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
        self.assertNotEqual(None, self.response['result']['myFollowDoctorList'][0]['name'], '我关注的医生姓名未显示')
        self.assertNotEqual(None, self.response['result']['myFollowDoctorList'][0]['deptName'], '我关注的医生科室未显示')
        self.assertNotEqual(None, self.response['result']['myFollowDoctorList'][0]['hospital'], '我关注医生的医院未显示')
        self.assertIn('liangyihui', self.response['result']['myFollowDoctorList'][0]['headPortraitUrl'], '我关注医生的头像未显示')
        self.assertLessEqual(1, len(self.response['result']['myFollowDoctorList']), '我关注医生的数据显示不全')

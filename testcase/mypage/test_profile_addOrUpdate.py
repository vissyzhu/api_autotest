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


class Test_AddOrUpdate(unittest.TestCase):
    '''
    新增或修改健康档案
    '''

    def __init__(self, *args, **kwargs):
        super(Test_AddOrUpdate, self).__init__(*args)
        self.url = api_mypage['addOrUpdate']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    # 修改健康档案
    def test_addOrUpdate(self):
        self.auth = common_data['Authorization']
        self.patientId = common_data['patientId']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "id": 96,
            "name": "朱珣",
            "gender": 2,
            "mobile": "15250485783",
            "idNo": "320324199006055006",
            "relation": 0,
            "birthdate": 644544000,
            "areaId": 1,
            "cityId": 3,
            "mainDiseaseId": 45,
            "idNoType": 1
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        # 结果验证
        self.assertEqual(self.response['status'], 0, '接口连接错误')
        self.assertEqual(self.response['result']['patientId'], self.patientId, '健康档案和患者关联错误')
        self.assertEqual(self.response['result']['name'], '朱珣', '姓名不一致')
        self.assertEqual(2, self.response['result']['gender'], '性别不一致')
        self.assertEqual(644544000, self.response['result']['birthdate'], '出生日期不一致')
        self.assertEqual(1, self.response['result']['areaId'], '所在地区不一致')
        self.assertEqual(3, self.response['result']['cityId'], '所在城市不一致')
        self.assertEqual(45, self.response['result']['mainDiseaseId'], '疾病不一致')

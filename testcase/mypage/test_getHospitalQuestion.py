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


class Test_GetHospitalQuestion(unittest.TestCase):
    '''
    我的提问列表
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetHospitalQuestion, self).__init__(*args)
        self.url = api_mypage['getHospitalQuestion']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_getHospitalQuestion(self):
        self.auth = common_data['Authorization']
        self.patientId = common_data['patientId']
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
        self.check_result()

    def check_result(self):
        connect = connectdb()
        conn = connect[0]
        cc = connect[1]
        cc.execute(
            "SELECT  `patient_condition` , `detail`  FROM `ask_question` WHERE `ask_by` =%s and `source` =2 AND `is_delete` =0 ORDER BY `id`  DESC %s" % self.patientId)  # 查询
        result = cc.fetchall()  # 获得数据库查询结果
        conn.close()
        # 结果验证
        if len(result) != 0 or len(self.response['result']['records']) != 0:
            self.assertEqual(self.response['status'], 0, '接口连接错误')
            self.assertEqual(self.response['result']['records'][0]['patientCondition'], result[0][0], '病情描述不一致')
            self.assertEqual(self.response['result']['records'][0]['detail'], result[0][1], '问题描述不一致')
            self.assertEqual(len(result), len(self.response['result']['records']), '提问数据显示不全')
        else:
            print('我的提问页数据不对！')

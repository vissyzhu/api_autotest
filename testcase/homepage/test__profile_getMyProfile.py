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


class Test_GetMyProfile(unittest.TestCase):
    '''
    获取我的健康档案,先获取档案id，便于提交服务订单
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetMyProfile, self).__init__(*args)
        self.url = api_mypage['getMyProfile']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_getMyProfile(self):
        self.auth = common_data['Authorization']
        self.patientId = common_data['patientId']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        common_data['profileId'] = self.response['result'][0]['id']
        self.check_result()

    def check_result(self):
        connect = connectdb()
        conn = connect[0]
        cc = connect[1]
        cc.execute("SELECT  *  FROM `dh_patient_profile` WHERE patient_id=%s" % self.patientId)  # 查询
        result = cc.fetchall()  # 获得数据库查询结果
        conn.close()
        # 结果验证
        self.assertEqual(self.response['status'], 0, '接口连接错误')
        self.assertEqual(self.response['result'][0]['name'], result[0][2], '姓名不一致')
        self.assertEqual(self.response['result'][0]['gender'], result[0][3], '性别不一致')
        self.assertEqual(self.response['result'][0]['mobile'], result[0][13], '手机号不一致')
        self.assertEqual(self.response['result'][0]['idNo'], result[0][14], '身份证不一致')
        self.assertEqual(self.response['result'][0]['birthdate'], result[0][5], '出生日期不一致')
        self.assertEqual(self.response['result'][0]['mainDiseaseId'], result[0][6], '疾病id不一致')
        self.assertEqual(self.response['result'][0]['areaId'], result[0][7], '所在省份不一致')
        self.assertEqual(self.response['result'][0]['cityId'], result[0][12], '所在城市不一致')
        self.assertEqual(self.response['result'][0]['relation'], result[0][8], '亲友关系不一致')

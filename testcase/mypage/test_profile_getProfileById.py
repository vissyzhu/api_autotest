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


class Test_GetProfileById(unittest.TestCase):
    '''
    根据健康档案id查看档案信息
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetProfileById, self).__init__(*args)
        self.url = api_mypage['getProfileById']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_getProfileById(self):
        self.auth = common_data['Authorization']
        self.profileId = common_data['profileId']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "id": self.profileId
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
            "SELECT * FROM (SELECT  dpp.id as idd,dpp.`city_id` ,dpp.`name`  ,dpp.`gender` ,dpp.`mobile` ,dpp.`id_no` ,dpp.`birthdate` ,dd.name as disease FROM `dh_patient_profile` dpp JOIN dh_disease dd on dpp.`main_disease_id` =dd.id )a join `base_area`  ba ON a.city_id=ba.`base_area_id`  WHERE a.idd=%s" % self.profileId)  # 查询
        result = cc.fetchall()  # 获得数据库查询结果
        conn.close()
        # 结果验证
        self.assertEqual(self.response['status'], 0, '接口连接错误')
        self.assertEqual(self.response['result']['name'], result[0][2], '姓名不一致')
        self.assertEqual(self.response['result']['gender'], result[0][3], '性别不一致')
        self.assertLessEqual(30, self.response['result']['age'], '年龄未返回')
        self.assertEqual(self.response['result']['mobile'], result[0][4], '手机号不一致')
        self.assertEqual(self.response['result']['idNo'], result[0][5], '身份证不一致')
        self.assertEqual(self.response['result']['birthdate'], result[0][6], '出生日期不一致')
        self.assertEqual(self.response['result']['disease'], result[0][7], '疾病不一致')
        self.assertEqual(self.response['result']['areaName'], result[0][11], '所在地区不一致')

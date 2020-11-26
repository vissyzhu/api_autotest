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


class Test_GetPrescriptionById(unittest.TestCase):
    '''
    处方详情接口
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetPrescriptionById, self).__init__(*args)
        self.url = api_mypage['getPrescriptionById']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_getPrescriptionById(self):
        self.auth = common_data['Authorization']
        self.prescriptionId = common_data['prescriptionId']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "id": "%s" % self.prescriptionId
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
            "SELECT dp.`result` ,dpd.`drug_name`,dpd.`drug_specs`   from `dh_prescription` dp RIGHT  JOIN `dh_prescription_drug` dpd ON dp.`id` =dpd.`prescription_id` WHERE dp.`id` =%s" % self.prescriptionId)  # 查询
        result = cc.fetchall()  # 获得数据库查询结果
        conn.close()
        # 结果验证
        self.assertEqual(self.response['status'], 0, '接口连接错误')
        self.assertNotEqual(None, self.response['result']['name'], '就诊人姓名未显示')
        self.assertNotEqual(None, self.response['result']['deptName'], '就诊科室未显示')
        self.assertIn(self.response['result']['gender'], (1, 2), '就诊人性别未显示')
        self.assertLessEqual(1, self.response['result']['age'], '就诊人年龄未显示')
        self.assertEqual(self.response['result']['result'], result[0][0], '诊断结果不对')
        self.assertEqual(self.response['result']['prescriptionDrugs'][0]['drugName'], result[0][1], '处方的药品名不对')
        self.assertEqual(self.response['result']['prescriptionDrugs'][0]['drugSpecs'], result[0][2], '处方药品的规格不对')
        self.assertNotEqual(None, self.response['result']['prescriptionDrugs'][0]['useMethod'], '药品用法未显示')
        self.assertNotEqual(None, self.response['result']['prescriptionDrugs'][0]['useRate'], '用药频率未显示')
        self.assertLessEqual(1, self.response['result']['prescriptionDrugs'][0]['drugAmount'], '药品数量未显示')
        self.assertNotEqual(None, self.response['result']['prescriptionDrugs'][0]['drugUnit'], '药品单位未显示')
        self.assertLessEqual(1, len(self.response['result']['prescriptionDrugs']), '药品数据不全')


if __name__ == '__main__':
    t = Test_GetPrescriptionById()
    t.test_getPrescriptionById()

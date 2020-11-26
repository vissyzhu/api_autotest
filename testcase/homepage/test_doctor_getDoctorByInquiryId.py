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


class Test_GetDoctorByInquiryId(unittest.TestCase):
    '''
    图文问诊的医生和图文问诊的订单详情
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetDoctorByInquiryId, self).__init__(*args)
        self.url = api_homepage['getDoctorByInquiryId']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_getDoctorByInquiryId(self):
        self.auth = common_data['Authorization']
        self.inquiryId = common_data['inquiryId']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "id": self.inquiryId
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        connect = connectdb()
        conn = connect[0]
        cc = connect[1]
        cc.execute("SELECT * FROM `dh_inquiry` WHERE id=%s" % self.inquiryId)  # 查询
        result = cc.fetchall()  # 获得数据库查询结果
        conn.close()
        # 结果验证
        self.assertEqual(self.response['status'], 0, '接口连接错误')
        self.assertEqual(self.response['result']['dhInquiry']['patientProfileId'],result[0][1],'返回的健康档案id不对')
        self.assertEqual(self.response['result']['dhInquiry']['toDoctorId'],result[0][2],'图文问诊的医生id不一致')
        self.assertEqual(self.response['result']['dhInquiry']['description'],result[0][3],'图文问诊内容不一致')



if __name__ == '__main__':
    t = Test_GetDoctorByInquiryId()
    t.test_getDoctorByInquiryId()

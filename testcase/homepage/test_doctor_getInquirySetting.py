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


class Test_getInquirySetting(unittest.TestCase):
    '''
    医生的服务设置
    '''

    def __init__(self, *args, **kwargs):
        super(Test_getInquirySetting, self).__init__(*args)
        self.url = api_homepage['getInquirySetting']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_getInquirySetting(self):
        self.auth = common_data['Authorization']
        self.doctorId = common_data['doctorId']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "id": "%s" % self.doctorId,
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        connect = connectdb()
        conn = connect[0]
        cc = connect[1]
        cc.execute("SELECT * FROM `dh_inquiry_setting`  WHERE doctor_id=%s" % self.doctorId)  # 查询
        result = cc.fetchall()  # 获得数据库查询结果
        conn.close()
        # 结果验证
        self.assertEqual(self.response['status'], 0, '接口连接错误')
        self.assertEqual(self.response['result']['askSwitch'], result[0][2], '图文咨询开关设置不一致')
        self.assertEqual(self.response['result']['askAmount'], result[0][3], '图文咨询设置的价格不一致')
        self.assertEqual(self.response['result']['inquirySwitch'], result[0][4], '图文问诊开关设置不一致')
        self.assertEqual(self.response['result']['inquiryAmount'], result[0][5], '图文问诊设置的价格不一致')
        self.assertEqual(self.response['result']['videoSwitch'], result[0][6], '视频咨询的开关设置不一致')
        self.assertEqual(self.response['result']['videoAmount'], result[0][7], '视频咨询设置的价格不一致')
        self.assertEqual(self.response['result']['opinionSwitch'], result[0][9], '第二诊疗意见开关设置不一致')
        self.assertEqual(self.response['result']['opinionAmount'], result[0][10], '第二诊疗意见设置的价格不一致')
        self.assertEqual(self.response['result']['questionSwitch'], result[0][11], '一问一答开关设置不一致')
        self.assertEqual(self.response['result']['questionAmount'], result[0][12], '一问一答设置的价格不一致')

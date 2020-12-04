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


class Test_CancelInquiry(unittest.TestCase):
    '''
    取消订单
    '''

    def __init__(self, *args, **kwargs):
        super(Test_CancelInquiry, self).__init__(*args)
        self.url = api_mypage['cancelInquiry']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_cancelInquiry(self):
        self.auth = common_data['Authorization']
        self.inquiryId = common_data['inquiryId']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "inquiryId": self.inquiryId,
            "type": 1
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        connect = connectdb()
        conn = connect[0]
        cc = connect[1]
        cc.execute("SELECT `status`  FROM  `dh_inquiry` WHERE id=%s" % self.inquiryId)  # 查询
        result = cc.fetchall()  # 获得数据库查询结果
        cc.execute("SELECT  id  FROM `dh_payment` WHERE service_id=%s" % self.inquiryId)
        result0 = cc.fetchall()
        common_data['paymentId'] = result0[0][0]
        conn.close()
        # 结果验证
        self.assertEqual(self.response['status'], 0, '接口连接错误')
        self.assertEqual(6, result[0][0], '取消订单成功')

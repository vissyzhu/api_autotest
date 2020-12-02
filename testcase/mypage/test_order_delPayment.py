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


class Test_DelPayment(unittest.TestCase):
    '''
    删除订单
    '''

    def __init__(self, *args, **kwargs):
        super(Test_DelPayment, self).__init__(*args)
        self.url = api_mypage['delPayment']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_delPayment(self):
        self.auth = common_data['Authorization']
        self.paymentId = common_data['paymentId']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "paymentId": self.paymentId
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
            "SELECT di.`is_delete` ,dp.`is_delete`  FROM `dh_inquiry` di JOIN `dh_payment` dp on di.`id` =dp.`service_id` WHERE dp.`id` =%s" % self.paymentId)  # 查询
        result = cc.fetchall()  # 获得数据库查询结果
        conn.close()
        # 结果验证
        self.assertEqual(self.response['status'], 0, '接口连接错误')
        self.assertEqual(1, result[0][0], '订单表订单删除失败')
        self.assertEqual(1, result[0][1], '支付表订单删除失败')

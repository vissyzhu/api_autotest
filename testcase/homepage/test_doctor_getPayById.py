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


class Test_GetPayById(unittest.TestCase):
    '''
    获取图文问诊的支付状态
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetPayById, self).__init__(*args)
        self.url = api_homepage['getPayById']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_getPayById(self):
        self.auth = common_data['Authorization']
        self.inquiryId = common_data['inquiryId']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "id": "%s" % self.inquiryId
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        connect = connectdb()
        conn = connect[0]
        cc = connect[1]
        cc.execute("SELECT * FROM `dh_payment` WHERE service_id=%s" % self.inquiryId)  # 查询
        result = cc.fetchall()  # 获得数据库查询结果
        conn.close()
        # 结果验证
        self.assertEqual(self.response['status'], 0, '接口连接错误')
        self.assertEqual(self.response['result']['serialNumber'], result[0][1], '订单id不一致')
        self.assertEqual(self.response['result']['serviceType'], result[0][2], '服务类型不一致')
        self.assertEqual(self.response['result']['amount'], result[0][4], '服务的价格不一致')


if __name__ == '__main__':
    t = Test_GetPayById()
    t.test_getPayById()

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


class Test_CollectDocument(unittest.TestCase):
    '''
    收藏公开课
    '''

    def __init__(self, *args, **kwargs):
        super(Test_CollectDocument, self).__init__(*args)
        self.url = api_homepage['collectDocument']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中
        self.auth = common_data['Authorization']
        self.docId = common_data['docId']
        self.patientId = common_data['patientId']

    # 收藏公开课
    def test_collectDocument(self):
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "docId": "%s" % self.docId,
            "collectId": 0,
            "actionType": 1
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
            "SELECT  *  FROM `document_collect` WHERE `userId` =%s  ORDER BY `collectId`  DESC  " % self.patientId)  # 查询
        result = cc.fetchall()  # 获得数据库查询结果
        conn.close()
        # 结果验证
        self.assertEqual(self.response['status'], 0, "接口连接错误")
        self.assertEqual(self.response['result']['collectId'], result[0][6], '返回的收藏id错误')
        self.assertEqual(0, result[0][7], '收藏失败')

    # 取消收藏公开课，同收藏，只是参数不同，不做结果验证
    def test_cancelCollectDocument(self):
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "docId": "%s" % self.docId,
            "collectId": 0,
            "actionType": 2
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()

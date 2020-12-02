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


class Test_GetMyCollectedDocument(unittest.TestCase):
    '''
    我的收藏
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetMyCollectedDocument, self).__init__(*args)
        self.url = api_mypage['getMyCollectedDocument']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_getMyCollectedDocument(self):
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
            "SELECT  *  FROM `document_collect` WHERE `userId` =%s AND `userType` =2" % self.patientId)  # 查询
        result = cc.fetchall()  # 获得数据库查询结果
        conn.close()
        # 结果验证
        if len(result) != 0:
            self.assertEqual(self.response['status'], 0, '接口连接错误')
            self.assertNotEqual(None, self.response['result']['records'][0]['title'], '公开课名称未返回')
            self.assertLessEqual(1, self.response['result']['records'][0]['id'], '公开课id未返回')
            self.assertIn('liangyihui', self.response['result']['records'][0]['picurl'], '公开课背景图未返回')
            self.assertLessEqual(1, len(self.response['result']['records']), '收藏的公开课未返回')
        else:
            self.assertEqual(self.response['status'], 0, '接口连接错误')

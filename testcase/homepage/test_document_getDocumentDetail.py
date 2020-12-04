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


class Test_GetDocumentDetail(unittest.TestCase):
    '''
    义诊详情页
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetDocumentDetail, self).__init__(*args)
        self.url = api_homepage['getDocumentDetail']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_getDocumentDetail(self):
        self.auth = common_data['Authorization']
        self.docId = common_data['docId']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "head": {},
            "docId": "%s" % self.docId
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        connect = connectdb()
        conn = connect[0]
        cc = connect[1]
        cc.execute("SELECT  `title` ,content  FROM  `document_detail` WHERE id=%s" % self.docId)  # 查询
        result = cc.fetchall()  # 获得数据库查询结果
        conn.close()
        # 结果验证
        self.assertEqual(self.response['status'], 0, "接口连接错误")
        self.assertEqual(self.response['result']['basic']['title'], result[0][0], '义诊标题不一致')
        self.assertIn(result[0][1],self.response['result']['basic']['contents'][0],  '义诊详情不一致')

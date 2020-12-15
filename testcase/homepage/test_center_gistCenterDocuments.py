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


class Test_GistCenterDocuments(unittest.TestCase):
    '''
    单病种下的文章
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GistCenterDocuments, self).__init__(*args)
        self.url = api_homepage['gistCenterDocuments']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中
        self.centerId = common_data['centerId']

    def test_gistCenterDocuments(self):
        self.auth = common_data['Authorization']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "index": 1,
            "size": 3,
            "centerId": "%s" % self.centerId,
            "type": 1534,
            "all": False,
            "app": True
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        connect = connectdb()
        conn = connect[0]
        cc = connect[1]
        cc.execute("SELECT * FROM dh_center_relate_document WHERE center_id=5 ")  # 查询
        result = cc.fetchall()  # 获得数据库查询结果
        conn.close()
        # 结果验证
        self.assertEqual(self.response['status'], 0, "接口连接错误")
        if len(result) != 0:
            self.assertLessEqual(1, self.response['result']['records'][0]['id'], '文章id未返回')
            self.assertNotEqual(None, self.response['result']['records'][0]['title'], '文章标题未返回')
            # self.assertLessEqual(1, self.response['result']['records'][0]['readCount'], '文章查看次数未返回')
            self.assertIn(self.response['result']['records'][0]['docType'], (16, 22), '文章类型不对')
        else:
            print('暂无数据')

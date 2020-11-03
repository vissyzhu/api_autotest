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


class Test_GetDocumentList(unittest.TestCase):
    '''
    单病种中心-名医义诊
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetDocumentList, self).__init__(*args)
        self.url = api_homepage['getDocumentList']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_getDocumentList(self):
        data = {
            "head": {},
            "centerId": "5",
            "filters": [{
                "filterGroupId": 23
            }],
            "sort": {
                "pageIdx": 0,
                "pageSize": 100,
                "startTime": 0
            }
        }
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        # 结果验证
        self.assertEqual(self.response['status'], 0, "接口连接错误")
        self.assertLessEqual(1, self.response['result']['docGroups'][0]['count'], '往期回顾的义诊列表返回数据不对')
        self.assertNotEqual(None, self.response['result']['docGroups'][0]['documents'][0]['title'], '义诊名未返回')
        self.assertLessEqual(1, len(self.response['result']['docGroups'][0]['documents']), '义诊列表数据返回不对')


if __name__ == '__main__':
    t = Test_XXXXX()
    t.test_xxxx()

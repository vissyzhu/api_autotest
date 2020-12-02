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


class Test_GetAppDocDocumentPage(unittest.TestCase):
    '''
    医生主页下的科普文章,写死韩艺菲医生的科普
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetAppDocDocumentPage, self).__init__(*args)
        self.url = api_homepage['getAppDocDocumentPage']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_getAppDocDocumentPage(self):
        self.auth = common_data['Authorization']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "doctorId": "238480",
            "index": 1,
            "size": 20
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        # 结果验证
        self.assertEqual(self.response['status'], 0, '接口连接错误')
        self.assertIn('韩艺菲', self.response['result'][0]['documents'][0]['title'], '科普文章标题错误')
        self.assertIn('liangyihui', self.response['result'][0]['documents'][0]['picUrl'], '科普文章的背景图未显示')
        self.assertLessEqual(1, self.response['result'][0]['documents'][0]['docId'], '科普文章id错误')
        self.assertLessEqual(1, len(self.response['result'][0]['documents']), '科普文章未显示')

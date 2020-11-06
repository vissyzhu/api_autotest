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


class Test_getAppHospitalDocumentPage(unittest.TestCase):
    '''
    医院下的科普文章
    '''

    def __init__(self, *args, **kwargs):
        super(Test_getAppHospitalDocumentPage, self).__init__(*args)
        self.url = api_homepage['getAppHospitalDocumentPage']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_getAppHospitalDocumentPage(self):
        self.auth = common_data['Authorization']
        self.hospitalId = common_data['hospitalId']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "hospitalId": "%s" % self.hospitalId,
            "index": 1,
            "size": 20
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        # 结果验证
        self.assertEqual(self.response['status'], 0, "接口连接错误")
        if self.response['result'][0]['count'] != 0:
            self.assertNotEqual(None, self.response['result'][0]['documents'][0]['title'], '科普文章标题未显示')
            self.assertLessEqual(1, self.response['result'][0]['documents'][0]['docId'], '科普文章的id未返回')
            self.assertLessEqual(0, self.response['result'][0]['documents'][0]['readAmount'], '科普文章的阅读次数未返回')
        else:
            print('该医院暂无科普文章')


if __name__ == '__main__':
    t = Test_getAppHospitalDocumentPage()
    t.test_getAppHospitalDocumentPage()

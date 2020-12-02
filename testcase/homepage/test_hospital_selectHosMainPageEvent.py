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


class Test_selectHosMainPageEvent(unittest.TestCase):
    '''
    医院主页下的专家科普专题
    '''

    def __init__(self, *args, **kwargs):
        super(Test_selectHosMainPageEvent, self).__init__(*args)
        self.url = api_homepage['selectHosMainPageEvent']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_selectHosMainPageEvent(self):
        self.auth = common_data['Authorization']
        self.hospitalId = common_data['hospitalId']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "eventId": 0,
            "id": "%s" % self.hospitalId,
            "index": 1,
            "size": 4,
            "type": 1
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        # 结果验证
        self.assertEqual(self.response['status'], 0, "接口连接错误")
        if len(self.response['result']['pageEventVO']) != 0:
            self.assertLessEqual(1, self.response['result']['pageEventVO'][0]['eventId'], '专题id未返回')
            self.assertNotEqual(None, self.response['result']['pageEventVO'][0]['name'], '专题名未返回')
            self.assertIn('liangyihui', self.response['result']['pageEventVO'][0]['picUrl'], '专题icon未返回')
        else:
            print('该医院暂无专家科普专题')

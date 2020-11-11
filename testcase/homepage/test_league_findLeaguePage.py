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


class Test_FindLeaguePage(unittest.TestCase):
    '''
    医联体列表
    '''

    def __init__(self, *args, **kwargs):
        super(Test_FindLeaguePage, self).__init__(*args)
        self.url = api_homepage['findLeaguePage']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_findLeaguePage(self):
        self.auth = common_data['Authorization']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "index": 1,
            "size": 20
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        common_data['leagueId'] = self.response['result']['records'][0]['id']
        self.check_result()

    def check_result(self):
        # 结果验证
        self.assertEqual(self.response['status'], 0, '接口连接错误')
        self.assertNotEqual(None, self.response['result']['records'][0]['name'], '医联体名未返回')
        self.assertIn('liangyihui', self.response['result']['records'][0]['picUrl'], '医联体的图片未返回')


if __name__ == '__main__':
    t = Test_FindLeaguePage()
    t.test_findLeaguePage()

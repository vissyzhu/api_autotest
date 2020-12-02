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


class Test_ThumbUp(unittest.TestCase):
    '''
    团队主页点赞
    '''

    def __init__(self, *args, **kwargs):
        super(Test_ThumbUp, self).__init__(*args)
        self.url = api_homepage['thumbUp']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_thumbUp(self):
        self.auth = common_data['Authorization']
        self.teamId = common_data['teamId']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "mainPageId": "%s" % self.teamId,
            "mainPageType": 4
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        # 结果验证
        self.assertEqual(self.response['status'], 0, "接口连接错误")
        self.assertLessEqual(1, self.response['result']['thumbUpCount'], '团队主页点赞数显示不对')
        self.assertEqual('点赞成功', self.response['result']['msg'], '点赞失败')

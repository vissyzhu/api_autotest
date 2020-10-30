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


class Test_GistCenterTree(unittest.TestCase):
    '''
    全球肿瘤防治中心
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GistCenterTree, self).__init__(*args)
        self.url = api_homepage['gistCenterTree']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_gistCenterTree(self):
        data = {
        }
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        # 结果验证
        self.assertEqual(self.response['status'], 0, '接口连接错误')
        # 预防中心
        self.assertEqual(self.response['result'][1]['name'], '预防中心', '预防中心列表未返回')
        self.assertEqual('防癌中心', self.response['result'][1]['centerTreeVOS'][0]['name'], '预防中心的防癌中心数据未返回')
        self.assertLessEqual(1, len(self.response['result'][1]['centerTreeVOS'][0]['centerTreeVOS']), '防癌中心数据未返回')
        # 诊疗中心
        self.assertEqual(self.response['result'][2]['name'], '诊疗中心', '诊疗中心列表未返回')
        self.assertEqual('实体瘤中心', self.response['result'][2]['centerTreeVOS'][0]['name'], '诊疗中心的实体瘤中心数据未返回')
        self.assertLessEqual(1, len(self.response['result'][2]['centerTreeVOS'][0]['centerTreeVOS']), '实体瘤中心数据未返回')
        # 研究中心
        self.assertEqual(self.response['result'][4]['name'], '研究中心', '研究中心列表未返回')
        self.assertEqual('临床试验', self.response['result'][4]['centerTreeVOS'][0]['centerTreeVOS'][0]['name'],
                         '临床试验数据未返回')


if __name__ == '__main__':
    t = Test_GistCenterTree()
    t.test_gistCenterTree()

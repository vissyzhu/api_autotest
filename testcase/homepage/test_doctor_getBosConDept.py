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


class Test_GetBosConDept(unittest.TestCase):
    '''
    找专家页科室列表
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetBosConDept, self).__init__(*args)
        self.url = api_homepage['getBosConDept']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_getBosConDept(self):
        self.auth = common_data['Authorization']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {

        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        # 结果验证
        self.assertEqual(self.response['status'], 0, '接口连接错误')
        self.assertEqual('肿瘤科', self.response['result'][0]['name'], '一级科室名称不对')
        self.assertEqual('肿瘤内科', self.response['result'][0]['childrens'][0]['name'], '二级科室不对')
        self.assertEqual('病理科', self.response['result'][1]['name'], '科室名称不对')
        self.assertLessEqual(20, len(self.response['result']), '科室数据返回不全')


if __name__ == '__main__':
    t = Test_GetBosConDept()
    t.test_getBosConDept()

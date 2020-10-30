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


class Test_GetTeamPage(unittest.TestCase):
    '''
    团队列表
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetTeamPage, self).__init__(*args)
        self.url = api_homepage['getTeamPage']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_getTeamPage(self):
        self.teamId = common_data['teamId']
        data = {
            "centerId": 0,
            "index": 1,
            "size": 20
        }
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        common_data['teamId'] = self.response['result']['records'][0]['id']
        self.check_result()

    def check_result(self):
        connect = connectdb()
        conn = connect[0]
        cc = connect[1]
        cc.execute("SELECT * FROM dh_medical_team WHERE id=%s" % self.teamId)  # 查询
        result = cc.fetchall()  # 获得数据库查询结果
        conn.close()
        # 结果验证
        self.assertEqual(self.response['status'], 0, "接口连接错误")
        self.assertLessEqual(1, len(self.response['result']['records']), '团队数据返回不全')
        self.assertEqual(result[0][1], self.response['result']['records'][0]['teamName'], '团队名称未返回')
        self.assertEqual(result[0][3], self.response['result']['records'][0]['picUrl'], '团队图片未显示')


if __name__ == '__main__':
    t = Test_GetTeamPage()
    t.test_getTeamPage()

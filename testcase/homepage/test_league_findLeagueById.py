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


class Test_FindLeagueById(unittest.TestCase):
    '''
    医联体详情页
    '''

    def __init__(self, *args, **kwargs):
        super(Test_FindLeagueById, self).__init__(*args)
        self.url = api_homepage['findLeagueById']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_findLeagueById(self):
        self.auth = common_data['Authorization']
        self.leagueId = common_data['leagueId']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "leagueId": "%s" % self.leagueId
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        connect = connectdb()
        conn = connect[0]
        cc = connect[1]
        cc.execute("SELECT  name,pic_url,description  FROM `dh_medical_league`  WHERE id=%s" % self.leagueId)  # 查询
        result = cc.fetchall()  # 获得数据库查询结果
        conn.close()
        # 结果验证
        self.assertEqual(self.response['status'], 0, '接口连接错误')
        self.assertEqual(self.response['result']['name'], result[0][0], '医联体名不一致')
        self.assertEqual(self.response['result']['picUrl'], result[0][1], '医联体图片不一致')
        self.assertEqual(self.response['result']['description'], result[0][2], '医联体简介不一致')

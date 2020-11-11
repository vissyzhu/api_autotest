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


class Test_GetLeagueHos(unittest.TestCase):
    '''
    医联体关联的医院数据
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetLeagueHos, self).__init__(*args)
        self.url = api_homepage['getLeagueHos']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_getLeagueHos(self):
        self.auth = common_data['Authorization']
        self.leagueId = common_data['leagueId']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "leagueId": "%s" % self.leagueId,
            "index": 1,
            "size": 2
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        connect = connectdb()
        conn = connect[0]
        cc = connect[1]
        cc.execute(
            "SELECT  bh.`hospital_name`   FROM `dh_hospital_relate_league` rl JOIN `basicdata_hospital` bh on rl.`hospital_id` =bh.`rec_id` WHERE rl.`league_id` =%s" % self.leagueId)  # 查询
        result = cc.fetchall()  # 获得数据库查询结果
        conn.close()
        # 结果验证
        self.assertEqual(self.response['status'], 0, '接口连接错误')
        if len(result) != 0 or len(self.response['result']['records']) != 0:
            self.assertEqual(self.response['result']['records'][0]['name'], result[0][0], '医联体下的医院名不一致')
            self.assertIn('liangyihui', self.response['result']['records'][0]['picUrl'], '医联体的医院背景图没显示')
        else:
            print('该医联体下无医院数据')


if __name__ == '__main__':
    t = Test_GetLeagueHos()
    t.test_getLeagueHos()

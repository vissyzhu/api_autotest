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


class Test_GetLeagueDoc(unittest.TestCase):
    '''
    医联体关联的医生数据
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetLeagueDoc, self).__init__(*args)
        self.url = api_homepage['getLeagueDoc']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_getLeagueDoc(self):
        self.auth = common_data['Authorization']
        self.leagueId = common_data['leagueId']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "leagueId": "%s" % self.leagueId,
            "index": 1,
            "size": 20
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        connect = connectdb()
        conn = connect[0]
        cc = connect[1]
        cc.execute("SELECT  *  FROM `dh_doctor_relate_league` WHERE `league_id` =%s" % self.leagueId)
        result = cc.fetchall()
        if len(result) != 0 or len(self.response['result']['records']) != 0:
            cc.execute(
                "SELECT  ui.`real_name` ,uc.`dept_title` ,uc.`dept_name`, uc.`cmp_name`  ,ui.`introduction`   FROM `user_identity` ui JOIN  `user_company` uc on ui.`user_id` =uc.`user_id` WHERE ui.`user_id` =%s" %
                result[0][0])  # 查询
            result = cc.fetchall()  # 获得数据库查询结果
            self.assertEqual(self.response['status'], 0, '接口连接错误')
            self.assertEqual(self.response['result']['records'][0]['name'], result[0][0], '医生姓名错误')
            self.assertEqual(self.response['result']['records'][0]['deptTitle'], result[0][1], '医生职称错误')
            self.assertEqual(self.response['result']['records'][0]['dept'], result[0][2], '医生科室错误')
            self.assertEqual(self.response['result']['records'][0]['hospital'], result[0][3], '医生所在医院显示错误')
            self.assertEqual(self.response['result']['records'][0]['description'], result[0][4], '医生的个人简介错误')
            self.assertLessEqual(1, len(self.response['result']['records']), '医生数据返回不全')
        else:
            print('该医联体下无医生数据')
        conn.close()


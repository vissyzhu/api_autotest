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


class Test_GetTeamMainPage(unittest.TestCase):
    '''
    团队主页
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetTeamMainPage, self).__init__(*args)
        self.url = api_homepage['getTeamMainPage']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_getTeamMainPage(self):
        self.teamId = common_data['teamId']
        self.auth = common_data['Authorization']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "teamId": "%s" % self.teamId,
            "index": 1,
            "size": 9
        }

        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        connect = connectdb()
        conn = connect[0]
        cc = connect[1]
        cc.execute("SELECT * FROM dh_medical_team WHERE id=%s" % self.teamId)
        result0 = cc.fetchall()
        # 团队简介结果验证
        self.assertEqual(self.response['status'], 0, "接口连接错误")
        self.assertEqual(self.response['result']['teamId'], self.teamId, '团队信息返回错误')
        self.assertEqual(result0[0][1], self.response['result']['teamName'], '团队名称未返回')
        self.assertEqual(result0[0][2], self.response['result']['description'], '团队介绍未显示')
        self.assertEqual(result0[0][3], self.response['result']['picUrl'], '团队图片未显示')
        self.assertLessEqual(1, self.response['result']['thumbUpCount'], '团队点赞数未显示')
        # 团队成员
        cc.execute(
            "SELECT * FROM `dh_doctor_relate_team` dd JOIN(SELECT * FROM `dh_doctor_ext` de JOIN `user_plat` up on de.`doctor_id`= up.`user_id` WHERE de.`is_forbid`= 0 AND up.`user_plat`= 3 AND up.`user_type`= 1) AS a ON dd.`doctor_id`= a.doctor_id WHERE dd.`team_id`= %s" % self.teamId)  # 查询
        result1 = cc.fetchall()  # 获得数据库查询结果
        if len(result1) != 0:
            cc.execute(
                "SELECT  ui.`real_name` ,uc.`dept_title`  , uc.`cmp_name`,uc.`dept_name`,ui.`introduction`     FROM  `user_identity` ui JOIN  `user_company` uc on ui.`user_id` =uc.`user_id` WHERE ui.`user_id` = %s" %
                result1[0][0])  # 查询
            result2 = cc.fetchall()  # 获得数据库查询结果
            conn.close()
            self.assertEqual(result2[0][0], self.response['result']['doctorVOS']['records'][0]['name'], '团队成员未显示')
            self.assertEqual(result2[0][1], self.response['result']['doctorVOS']['records'][0]['deptTitle'], '专家职称未显示')
            self.assertEqual(result2[0][2], self.response['result']['doctorVOS']['records'][0]['hospital'],
                             '专家所在医院显示错误')
            self.assertEqual(result2[0][3], self.response['result']['doctorVOS']['records'][0]['dept'], '专家所在科室显示错误')

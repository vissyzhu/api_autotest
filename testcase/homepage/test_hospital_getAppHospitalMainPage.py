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


class Test_getAppHospitalMainPage(unittest.TestCase):
    '''
    医院主页
    '''

    def __init__(self, *args, **kwargs):
        super(Test_getAppHospitalMainPage, self).__init__(*args)
        self.url = api_homepage['getAppHospitalMainPage']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_getAppHospitalMainPage(self):
        self.auth = common_data['Authorization']
        self.hospitalId = common_data['hospitalId']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "hospitalId": "%s" % self.hospitalId,
            "docSize": 1,
            "askSize": 2,
            "doctorSize": 3
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
            "SELECT bh.`hospital_name` ,bh.`address` ,bh.`telephone` ,dh.`description` ,dh.`pic_url`,bh.`level` ,bh.`category`    FROM `dh_hospital_ext` dh JOIN `basicdata_hospital` bh ON  dh.`hospital_id` =bh.`rec_id` WHERE dh.`hospital_id` =%s" % self.hospitalId)  # 查询
        result0 = cc.fetchall()  # 获得数据库查询结果
        # 医院的基本信息验证
        self.assertEqual(self.response['status'], 0, "接口连接错误")
        self.assertEqual(self.response['result']['hospitalMsg']['id'], self.hospitalId, '医院id返回错误')
        self.assertEqual(self.response['result']['hospitalMsg']['name'], result0[0][0], '医院名称错误')
        self.assertEqual(self.response['result']['hospitalMsg']['address'], result0[0][1], '医院地址错误')
        self.assertEqual(self.response['result']['hospitalMsg']['mobile'], result0[0][2], '医院的联系方式错误')
        self.assertEqual(self.response['result']['hospitalMsg']['description'], result0[0][3], '医院的简介错误')
        self.assertEqual(self.response['result']['hospitalMsg']['picUrl'], result0[0][4], '医院的背景图错误')
        self.assertEqual(self.response['result']['hospitalMsg']['level'], result0[0][5], '医院等级错误')
        self.assertEqual(self.response['result']['hospitalMsg']['category'], result0[0][6], '医院分类错误')
        self.assertLessEqual(0, self.response['result']['hospitalMsg']['thumbUpNum'], '医院主页的点赞数未返回')
        # 医院下的医生数据验证
        cc.execute(
            "SELECT * FROM `dh_doctor_relate_team` dd JOIN(SELECT *FROM `dh_doctor_ext` de JOIN `user_plat` up on de.`doctor_id`= up.`user_id` WHERE de.`is_forbid`= 0AND up.`user_plat`= 3AND up.`user_type`= 1) AS a ON dd.`doctor_id`= a.doctor_id WHERE dd.`team_id`= %s" % self.teamId)  # 查询
        result1 = cc.fetchall()  # 获得数据库查询结果
        if len(result1) != 0:
            cc.execute(
                "SELECT  ui.`real_name` ,uc.`dept_title`  , uc.`cmp_name`,uc.`dept_name`,ui.`introduction`     FROM  `user_identity` ui JOIN  `user_company` uc on ui.`user_id` =uc.`user_id` WHERE ui.`user_id` = %s" %
                result1[0][0])  # 查询
            result2 = cc.fetchall()  # 获得数据库查询结果
            self.assertEqual(self.response['result']['doctorUserPage']['records'][0]['name'], result2[0][0], '医生名称错误')
            self.assertEqual(self.response['result']['doctorUserPage']['records'][0]['deptTitle'], result2[0][1],
                             '医生职称错误')
            self.assertEqual(self.response['result']['doctorUserPage']['records'][0]['hospital'], result2[0][2],
                             '医生所在医院错误')
            self.assertEqual(self.response['result']['doctorUserPage']['records'][0]['dept'], result2[0][3], '医生所在科室错误')
            self.assertEqual(self.response['result']['doctorUserPage']['records'][0]['description'], result2[0][4],
                             '医生个人简介错误')
        else:
            print('该医院下无医生数据')
        # 医院下的科室数据验证
        cc.execute("SELECT   name FROM dh_hospital_dept WHERE  hospital_id=%s" % self.hospitalId)
        result3 = cc.fetchall()
        conn.close()
        if len(result3) != 0:
            self.assertEqual(self.response['result']['depts'][0]['name'], result3[0][0], '医院的科室名称错误')
        else:
            print('该医院无科室数据')


if __name__ == '__main__':
    t = Test_getAppHospitalMainPage()
    t.test_getAppHospitalMainPage()

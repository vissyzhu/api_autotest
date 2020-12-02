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


class Test_GetDoctorMainPage(unittest.TestCase):
    '''
    医生主页
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetDoctorMainPage, self).__init__(*args)
        self.url = api_homepage['getDoctorMainPage']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_getDoctorMainPage(self):
        self.auth = common_data['Authorization']
        self.doctorId = common_data['doctorId']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "doctorId": "%s" % self.doctorId,
            "docSize": 1,
            "askSize": 2,
            "evaluateSize": 2
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
            "SELECT  ui.`real_name` ,uc.`dept_title` ,uc.`dept_name`, uc.`cmp_name`   ,ui.`specialty`,ui.`introduction`   FROM `user_identity` ui JOIN  `user_company` uc on ui.`user_id` =uc.`user_id` WHERE ui.`user_id` =%s" %
            self.response['result']['records'][0]['doctorId'])  # 查询
        result = cc.fetchall()
        conn.close()
        # 结果验证
        self.assertEqual(self.response['status'], 0, '接口连接错误')
        self.assertEqual(self.response['result']['mainPageVO'][0]['name'], result[0][0], '医生姓名错误')
        self.assertEqual(self.response['result']['mainPageVO'][0]['deptTitle'], result[0][1], '医生职称错误')
        self.assertEqual(self.response['result']['mainPageVO'][0]['dept'], result[0][2], '医生科室错误')
        self.assertEqual(self.response['result']['mainPageVO'][0]['hospital'], result[0][3], '医生所在医院显示错误')
        self.assertEqual(self.response['result']['mainPageVO'][0]['specialty'], result[0][4], '医生的专业擅长错误')
        self.assertEqual(self.response['result']['mainPageVO'][0]['introduction'], result[0][5], '医生的职业经历错误')
        self.assertLessEqual(1, self.response['result']['mainPageVO'][0]['fansCount'], '关注数不对')
        self.assertLessEqual(1, self.response['result']['mainPageVO'][0]['serviceTime'], '服务次数不对')
        self.assertIn('感谢', self.response['result']['rateVoPage'][0]['rateText'], '评价内容未显示')
        self.assertLessEqual(1, len(self.response['result']['rateVoPage']), '患者评价数据显示不全')
        self.assertNotEqual(None, self.response['result']['questionDetailPage']['records'][0]['detail'], '问题没显示')

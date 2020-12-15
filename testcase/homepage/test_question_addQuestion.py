# coding=utf-8
"""
作者：vissy@zhu
"""

import unittest
from commonlib.confighttp import ConfigHttp
from testdata.api_data import api_homepage
from testdata.common_data import common_data
from commonlib.connectdb import connectdb
import time

confighttp = ConfigHttp()


# @unittest.skip('业务逻辑变更，无免费答疑')
class Test_AddQuestion(unittest.TestCase):
    '''
    立即提问
    '''

    def __init__(self, *args, **kwargs):
        super(Test_AddQuestion, self).__init__(*args)
        self.url = api_homepage['addQuestion']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

        self.date = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

    # # 公开课的定向提问
    # def test_addQuestion(self):
    #     header = {
    #         'Authorization': '%s' % self.auth,
    #         'From-Platform': 'miniapp'
    #     }
    #     data = {
    #         "subscribeType": 1,
    #         "fromDocId": "%s" % self.docId,
    #         "detail": "公开课定向留言提问+问题描述+lyhccapiautotest" + self.date,
    #         "patientCondition": "公开课定向留言提问+病情描述+lyhccapiautotest" + self.date,
    #         "preferDoctor": "公开课定向留言提问+想咨询的医生+lyhccapiautotest" + self.date,
    #         "disease": "鼻咽癌",
    #         "askTo": None,
    #         "askToType": None,
    #         "attachments": [],
    #         "patientProfileId": self.profileId
    #     }
    #     confighttp.set_headers(header)
    #     confighttp.set_data(data)
    #     self.response = confighttp.post().json()
    #     self.check_result()
    #     self.assertEqual(self.response['result']['docId'], self.result[0][4], '定向提问的公开课id存储错误')

    # 医生的定向提问
    def test_addQuestion(self):
        self.auth = common_data['Authorization']
        self.doctorId = common_data['doctorId']
        self.profileId = common_data['profileId']
        self.patientId = common_data['patientId']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "subscribeType": 1,
            "fromDocId": None,
            "detail": "医生定向提问+问题描述+lyhccapiautotest" + self.date,
            "patientCondition": "医生定向提问+病情描述+lyhccapiautotest" + self.date,
            "preferDoctor": "赵徐",
            "disease": "鼻咽癌",
            "askTo": "%s" % self.doctorId,
            "askToType": 0,
            "attachments": [],
            "patientProfileId": self.profileId
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        common_data['askPayId'] = self.response['result']
        self.check_result()

    # # 答疑大厅的立即提问
    # def test_addQuestion(self):
    #     header = {
    #         'Authorization': '%s' % self.auth,
    #         'From-Platform': 'miniapp'
    #     }
    #     data = {
    #         "subscribeType": 1,
    #         "fromDocId": None,
    #         "detail": "问题描述+lyhccapiautotest" + self.date,
    #         "patientCondition": "病情描述+lyhccapiautotest" + self.date,
    #         "preferDoctor": "",
    #         "disease": "鼻咽癌",
    #         "askTo": None,
    #         "askToType": None,
    #         "attachments": [],
    #         "patientProfileId": self.profileId
    #     }
    #     confighttp.set_headers(header)
    #     confighttp.set_data(data)
    #     self.response = confighttp.post().json()
    #     self.check_result()

    def check_result(self):
        connect = connectdb()
        conn = connect[0]
        self.cc = connect[1]
        self.cc.execute(
            "SELECT  `detail` ,`patient_condition`  ,`prefer_doctor` ,`disease` ,`ask_to` , `patient_profile_id`  FROM `ask_question` WHERE `source` =2 and `ask_by` =%s ORDER BY  `id`  DESC " % self.patientId)  # 查询
        self.result = self.cc.fetchall()  # 获得数据库查询结果
        conn.close()
        # 结果验证
        self.assertEqual(self.response['status'], 0, "接口连接错误")
        self.assertIn('医生定向提问+问题描述', self.result[0][0], '问题描述不一致')
        self.assertIn('医生定向提问+病情描述', self.result[0][1], '病情描述不一致')
        self.assertEqual('赵徐', self.result[0][2], '想咨询的医生不一致')
        self.assertEqual('鼻咽癌', self.result[0][3], '患者提交的瘤种不一致')
        self.assertEqual(self.doctorId, self.result[0][4], '患者定向提问的医生不一致')
        self.assertEqual(self.profileId, self.result[0][5], '就诊人id不一致')

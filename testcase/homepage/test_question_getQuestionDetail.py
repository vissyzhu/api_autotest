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


class Test_GetQuestionDetail(unittest.TestCase):
    '''
    在线答疑-问题详情
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetQuestionDetail, self).__init__(*args)
        self.url = api_homepage['getQuestionDetail']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_getQuestionDetail(self):
        self.auth = common_data['Authorization']
        self.questionId = common_data['questionId']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "id": "%s" % self.questionId,
            "needCount": True,
            "needAnswers": True,
            "answerStatus": 1
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
            "SELECT detail,patient_condition,disease,ask_by FROM ask_question WHERE id=%s" % self.questionId)  # 查询答疑问题表
        result = cc.fetchall()  # 获得数据库查询结果
        conn.commit()
        conn.close()
        # 结果验证
        self.assertEqual(self.response["status"], 0, "接口连接错误")
        self.assertEqual(self.response['result']['question']['id'], self.questionId, '问题id错误')
        self.assertEqual(self.response['result']['question']['detail'], result[0][0], '问题内容错误')
        self.assertEqual(self.response['result']['question']['patientCondition'], result[0][1], '病情描述错误')
        self.assertEqual(self.response['result']['question']['disease'], result[0][2], '问题瘤种错误')

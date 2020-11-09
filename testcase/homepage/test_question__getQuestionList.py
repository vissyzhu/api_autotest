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


class Test_Question_GetQuestionList(unittest.TestCase):
    '''
    在线答疑全部列表
    '''

    def __init__(self, *args, **kwargs):
        super(Test_Question_GetQuestionList, self).__init__(*args)
        self.url = api_homepage['getQuestionList']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_question_getQuestionList(self):
        self.auth = common_data['Authorization']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "diseaseList": [],
            "orderBy": "UPDATETIME",
            "pageStart": 1,
            "pageSize": 8,
            "status": 1,
            "isPublish": 1,
            "answerStatus": 1,
            "askTo": 0
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        common_data['questionId'] = self.response['result']['records'][0]['id']
        self.check_result()

    def check_result(self):
        # 结果验证
        # 结果验证
        self.assertEqual(self.response['status'], 0, "接口连接错误")
        self.assertNotEqual(None, self.response['result']['records'][0]['detail'], '问题内容没显示')
        self.assertEqual('胃肠间质瘤GIST', self.response['result']['records'][0]['disease'], '问题的瘤种不对')
        self.assertIn(self.response['result']['records'][0]['patientIdentity']['gender'], (1, 2), '患者性别不对')
        self.assertLessEqual(1, self.response['result']['records'][0]['patientIdentity']['age'], '患者年龄不对')
        self.assertNotEqual(None, self.response['result']['records'][0]['patientIdentity']['area'], '患者所在地区未显示')
        self.assertLessEqual(1, len(self.response['result']['records']), '在线答疑的问题返回不全')


if __name__ == '__main__':
    t = Test_XXXXX()
    t.test_xxxx()

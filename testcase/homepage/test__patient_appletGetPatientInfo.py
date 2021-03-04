# coding=utf-8
"""
作者：vissy@zhu
"""

import unittest
from commonlib.confighttp import ConfigHttp
from testdata.api_data import api_mypage
from testdata.common_data import common_data
from commonlib.connectdb import connectdb

confighttp = ConfigHttp()


class Test_AppletGetPatientInfo(unittest.TestCase):
    '''
    获取小程序的患者信息
    '''

    def __init__(self, *args, **kwargs):
        super(Test_AppletGetPatientInfo, self).__init__(*args)
        self.url = api_mypage['appletGetPatientInfo']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_appletGetPatientInfo(self):
        self.auth = common_data['Authorization']
        self.mobile = common_data['mobile']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.patientId = self.response['result']['basicInfo']['patientId']
        self.check_result()

    def check_result(self):
        connect = connectdb()
        conn = connect[0]
        cc = connect[1]
        cc.execute("SELECT id,nick_name,tel,attentions FROM patient_identity WHERE mobile=%s" % self.mobile)  # 查询
        result = cc.fetchall()  # 获得数据库查询结果
        conn.close()
        # 结果验证
        self.assertEqual(self.response['status'], 0, '接口连接出错')
        self.assertEqual(self.response['result']['basicInfo']['patientId'], result[0][0], '患者id返回错误')
        self.assertIn('http', self.response['result']['basicInfo']['headPortraitUrl'], '患者头像未返回')
        self.assertIn('vissy', self.response['result']['basicInfo']['nickName'], '患者昵称返回错误')
        self.assertEqual(self.response['result']['basicInfo']['tel'], result[0][2], '患者联系方式返回错误')
        self.assertEqual(self.response['result']['basicInfo']['attentions'], result[0][3], '患者关注的瘤种数据返回错误')

# coding=utf-8
"""
作者：vissy@zhu
"""

import unittest
from commonlib.confighttp import ConfigHttp
from testdata.api_data import api_mypage
from testdata.common_data import common_data
from commonlib.connectdb import connectdb
import time

confighttp = ConfigHttp()


class Test_UpdatePatient(unittest.TestCase):
    '''
    修改个人信息
    '''

    def __init__(self, *args, **kwargs):
        super(Test_UpdatePatient, self).__init__(*args)
        self.url = api_mypage['updatePatient']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中
        self.date = time.strftime('%Y%m%d', time.localtime(time.time()))

    def test_updatePatient(self):
        self.auth = common_data['Authorization']
        self.patientId = common_data['patientId']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "picUrl": "http://7xr5oh.com2.z0.glb.qiniucdn.com/data/1603188499136?e=2147483647&token=j4SBYhetYrc0sjLhIviVMGTHqzUrH6Zuh7dD0Jxh:Pj1azF6nc5k5bTPdM2KUiQt6_Hs=",
            "nickName": "昵称测试+lyhautotest" + self.date,
            "attentions": "甲状腺癌,胃肠间质瘤GIST,肝癌"
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        connect = connectdb()
        conn = connect[0]
        cc = connect[1]
        cc.execute("SELECT  nick_name,attentions  FROM `patient_identity` WHERE id=%s" % self.patientId)  # 查询
        result = cc.fetchall()  # 获得数据库查询结果
        conn.close()
        # 结果验证
        self.assertEqual(self.response['status'], 0, '接口连接错误')
        self.assertIn(self.date, result[0][0], '昵称未修改成功')
        self.assertEqual('甲状腺癌,胃肠间质瘤GIST,肝癌', result[0][1], '患者关注的瘤种不一致')

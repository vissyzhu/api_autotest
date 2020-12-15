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


class Test_GetDisByCenter(unittest.TestCase):
    '''
    单病种中心在线答疑关联的疾病，
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetDisByCenter, self).__init__(*args)
        self.url = api_homepage['getDisByCenter']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中
        self.centerId = common_data['centerId']

    def test_getDisByCenter(self):
        data = {
            "centerId": "%s" % self.centerId
        }
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        connect = connectdb()
        conn = connect[0]
        cc = connect[1]
        cc.execute(
            "SELECT dc.`disease_id` ,dd.name FROM `dh_center_relate_disease` dc join dh_disease dd ON  dc.`disease_id`  =dd.id WHERE dc.`center_id` =5")  # 查询
        result = cc.fetchall()  # 获得数据库查询结果
        conn.close()
        # 结果验证
        self.assertEqual(self.response['status'], 0, "接口连接错误")
        if len(self.response['result']) != 0 and len(result) != 0:
            self.assertEqual(self.response['result'][0]['id'], result[0][0], '单病种中心关联瘤种的id错误')
            self.assertEqual(self.response['result'][0]['name'], result[0][1], '单病种中心关联瘤种的名称错误')
        else:
            print("接口或查询返回数据错误。")

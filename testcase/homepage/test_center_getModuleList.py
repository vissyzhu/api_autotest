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


class Test_getModuleList(unittest.TestCase):
    '''
    单病种中心-模块配置接口，以胃肠道间质瘤为例
    '''

    def __init__(self, *args, **kwargs):
        super(Test_getModuleList, self).__init__(*args)
        self.url = api_homepage['getModuleList']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中
        self.centerId = common_data['centerId']

    def test_getModuleList(self):
        self.auth = common_data['Authorization']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "recordId": "%s" % self.centerId,
            "type": 0
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
            "SELECT  dm.`name`  FROM `dh_module`  dm JOIN  `dh_module_relate`  dmr on dm.`id` =dmr.`module_id` WHERE dmr.`record_id` =5 ORDER BY  dm.`sort`  DESC ")  # 查询
        result = cc.fetchall()  # 获得数据库查询结果
        conn.close()
        # 结果验证
        if len(self.response['result']) != 0 or len(result) != 0:
            self.assertEqual(self.response['status'], 0, "接口连接错误")
            for i in range(len(result)):
                self.assertEqual(self.response['result'][i]['name'], result[i][0], '模块未返回')
        else:
            print("该单病种中心未配置模块数据！")

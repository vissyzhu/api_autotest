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


class Test_FindListByPage(unittest.TestCase):
    '''
    在线答疑--瘤种筛选数据
    '''

    def __init__(self, *args, **kwargs):
        super(Test_FindListByPage, self).__init__(*args)
        self.url = api_homepage['findListByPage']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_findListByPage(self):
        self.auth = common_data['Authorization']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "startIndex": 0,
            "index": 1,
            "size": 100
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        connect = connectdb()
        conn = connect[0]
        cc = connect[1]
        cc.execute("SELECT  *  FROM  dh_disease")  # 查询
        result = cc.fetchall()  # 获得数据库查询结果
        conn.close()
        # 结果验证
        self.assertEqual(self.response['status'], 0, "接口连接错误")
        self.assertEqual(self.response['result']['records'][0]['id'], result[0][0], '瘤种id返回错误')
        self.assertEqual(self.response['result']['records'][0]['name'], result[0][2], '瘤种名称返回错误')
        self.assertEqual(len(self.response['result']['records']), len(result), '瘤种数量返回不全')


if __name__ == '__main__':
    t = Test_FindListByPage()
    t.test_findListByPage()

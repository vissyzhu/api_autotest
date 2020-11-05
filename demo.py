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


class Test_XXXXX(unittest.TestCase):
    '''
    xxxxxx
    '''

    def __init__(self, *args, **kwargs):
        super(Test_XXXXX, self).__init__(*args)
        self.url = api_homepage["xxx"]  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_xxxx(self):
        self.auth = common_data['Authorization']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "xxxxx"
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        connect = connectdb()
        conn = connect[0]
        cc = connect[1]
        cc.execute("SELECT * FROM user_identity WHERE user_id=%s" % self.user_id)  # 查询
        result = cc.fetchall()  # 获得数据库查询结果
        conn.close()
        # 结果验证
        self.assertEqual(self.response['status'], 0, "接口连接错误")
        self.assertEqual(self.response["basic"]['userId'], common_data['userid'], "用户id错误")
        self.assertEqual(self.response['basic']['name'], result[0][7], '用户昵称错误')


if __name__ == '__main__':
    t = Test_XXXXX()
    t.test_xxxx()

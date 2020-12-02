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


class Test_GetAppHomePage(unittest.TestCase):
    '''
    首页各板块返回的数据接口
    '''

    def __init__(self, *args, **kwargs):
        super(Test_GetAppHomePage, self).__init__(*args)
        self.url = api_homepage['getAppHomePage']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中

    def test_getAppHomePage(self):
        data = {
            "centerSize": 4,
            "docSize": 4,
            "hospitalSize": 2,
            "leagueSize": 2,
            "overseaDocSize": 2,
            "teamSize": 4
        }
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        self.check_result()

    def check_result(self):
        # 结果验证
        self.assertEqual(self.response['status'], 0, "接口连接错误")
        self.assertLessEqual(1, self.response['result']['centers'][0]['id'], '单病种中心未返回')
        self.assertNotEqual(None, self.response['result']['centers'][0]['name'], '单病种中心名称未返回')
        # self.assertIn('liangyihui' , self.response['result']['centers'][0]['iconUrl'],
        #               '单病种中心icon图标未显示')
        self.assertLessEqual(1, len(self.response['result']['centers']), '单病种中心数量返回不对')
        self.assertLessEqual(1, self.response['result']['teams'][0]['teamId'], '团队数据未返回')
        self.assertNotEqual(None, self.response['result']['teams'][0]['teamName'], '团队名称未返回')
        # self.assertIn('liangyihui' , self.response['result']['teams'][0]['picUrl'], '团队头像未返回')
        self.assertNotEqual(None, self.response['result']['teams'][0]['leaders'], '团队的领衔专家未返回')
        self.assertLessEqual(1, len(self.response['result']['teams']), '团队数量返回不对')
        self.assertLessEqual(1, self.response['result']['doctors'][0]['doctorId'], '推荐专家数据未返回')
        self.assertNotEqual(None, self.response['result']['doctors'][0]['name'], '推荐专家姓名未返回')
        # self.assertIn('liangyihui' , self.response['result']['doctors'][0]['portraitUrl'],
        #               '医生头像未返回')
        self.assertNotEqual(None, self.response['result']['doctors'][0]['deptTitle'], '推荐专家的职称未返回')
        self.assertNotEqual(None, self.response['result']['doctors'][0]['hospital'], '推荐专家所在医院未返回')
        self.assertLessEqual(1, len(self.response['result']['doctors']), '推荐专家返回的数量不对')
        self.assertLessEqual(1, self.response['result']['famousHospitals'][0]['id'], '肿瘤名院据未返回')
        self.assertIn('医院', self.response['result']['famousHospitals'][0]['name'], '肿瘤名院的医院名称未返回')
        self.assertNotEqual(None, self.response['result']['famousHospitals'][0]['disease'], '肿瘤名医的擅长瘤种未返回')
        # self.assertIn('liangyihui', self.response['result']['famousHospitals'][0]['picUrl'],
        #               '肿瘤名院的医院头像未返回')
        self.assertLessEqual(1, len(self.response['result']['famousHospitals']), '肿瘤名院返回的数量不对')
        self.assertLessEqual(1, self.response['result']['leagues'][0]['id'], '医联体数据未返回')
        self.assertNotEqual(None, self.response['result']['leagues'][0]['name'], '医联体名称未返回')
        # self.assertIn('liangyihui' , self.response['result']['leagues'][0]['picUrl'], '医联体头像未返回')
        self.assertLessEqual(1, len(self.response['result']['leagues']), '医联体返回数量不对')

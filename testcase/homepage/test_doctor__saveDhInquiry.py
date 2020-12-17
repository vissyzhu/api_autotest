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
import datetime

confighttp = ConfigHttp()


class Test_saveDhInquiry(unittest.TestCase):
    '''
    医生主页的图文问诊
    '''

    def __init__(self, *args, **kwargs):
        super(Test_saveDhInquiry, self).__init__(*args)
        self.url = api_homepage['saveDhInquiry']  # 获取接口名称
        confighttp.set_url(self.url)  # 将接口名称传给http配置文件中
        self.date = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

    # 图文咨询和问诊重复，只能提交一个，
    # def test_saveDhInquiry_ask(self):
    #     header = {
    #         'Authorization': '%s' % self.auth,
    #         'From-Platform': 'miniapp'
    #     }
    #     data = {
    #         "type": 1,
    #         "toDoctorId": self.doctorId,
    #         "patientProfileId": self.profileId,
    #         "description": "病情描述+图文咨询+lyhccautotest" + self.date,
    #         "picUrl": [
    #             "http://7xvci0.com2.z0.glb.qiniucdn.com/data/1606274608294?e=2147483647&token=j4SBYhetYrc0sjLhIviVMGTHqzUrH6Zuh7dD0Jxh:1BJnpfrb_BsTM5BIv_2tU-66pDc="],
    #         "isPublic": 0,
    #         "status": 0
    #     }
    #     confighttp.set_headers(header)
    #     confighttp.set_data(data)
    #     self.response = confighttp.post().json()
    #     self.check_result()
    #     self.assertEqual(self.result[0][4], 1, '服务类型不一致')
    #     self.assertIn('图文咨询', self.result[0][3], '图文咨询的病情描述不全')

    # 图文问诊
    def test_saveDhInquiry(self):
        self.auth = common_data['Authorization']
        self.doctorId = common_data['doctorId']
        self.profileId = common_data['profileId']
        self.patientId = common_data['patientId']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "type": 0,
            "toDoctorId": self.doctorId,
            "patientProfileId": self.profileId,
            "description": "病情描述+图文问诊+lyhccautotest" + self.date,
            "picUrl": [
                "http://7xvci0.com2.z0.glb.qiniucdn.com/data/1606274608294?e=2147483647&token=j4SBYhetYrc0sjLhIviVMGTHqzUrH6Zuh7dD0Jxh:1BJnpfrb_BsTM5BIv_2tU-66pDc="],
            "isPublic": 0,
            "status": 0
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        common_data['inquiryId'] = self.response['result']['inquiryId']
        self.check_result()
        self.assertEqual(self.result[0][4], 0, '服务类型不一致')
        self.assertIn('图文问诊', self.result[0][3], '图文问诊的病情描述不全')

    # 视频问诊
    def test_saveDhInquiry_video(self):
        self.auth = common_data['Authorization']
        self.doctorId = common_data['doctorId']
        self.profileId = common_data['profileId']
        self.patientId = common_data['patientId']
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        tomorrow_start_time = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d')))
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "type": 2,
            "toDoctorId": self.doctorId,
            "patientProfileId": self.profileId,
            "description": "病情描述+视频问诊+lyhccautotest" + self.date,
            "picUrl": [
                "http://7xvci0.com2.z0.glb.qiniucdn.com/data/1606274608294?e=2147483647&token=j4SBYhetYrc0sjLhIviVMGTHqzUrH6Zuh7dD0Jxh:1BJnpfrb_BsTM5BIv_2tU-66pDc="],
            "isPublic": 0,
            "status": 0,
            "appointmentTime": tomorrow_start_time
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        common_data['inquiryId_video'] = self.response['result']['inquiryId']
        self.check_result()
        self.assertEqual(self.result[0][4], 2, '服务类型不一致')
        self.assertIn('视频问诊', self.result[0][3], '视频问诊的病情描述不全')
        self.assertEqual(self.result[0][6], tomorrow_start_time, '视频问诊的预约时间不一致')

    # 第二诊疗意见
    def test_saveDhInquiry_opinion(self):
        self.auth = common_data['Authorization']
        self.doctorId = common_data['doctorId']
        self.profileId = common_data['profileId']
        self.patientId = common_data['patientId']
        header = {
            'Authorization': '%s' % self.auth,
            'From-Platform': 'miniapp'
        }
        data = {
            "type": 3,
            "toDoctorId": self.doctorId,
            "patientProfileId": self.profileId,
            "description": "病情描述+第二诊疗意见+lyhtestautotest" + self.date,
            "picUrl": [
                "http://7xvci0.com2.z0.glb.qiniucdn.com/data/1606274608294?e=2147483647&token=j4SBYhetYrc0sjLhIviVMGTHqzUrH6Zuh7dD0Jxh:1BJnpfrb_BsTM5BIv_2tU-66pDc="],
            "isPublic": 0,
            "status": 0,
            "appeal": "诊疗诉求+lyhccautotest" + self.date
        }
        confighttp.set_headers(header)
        confighttp.set_data(data)
        self.response = confighttp.post().json()
        common_data['inquiryId_opinion'] = self.response['result']['inquiryId']
        self.check_result()
        self.assertEqual(self.result[0][4], 3, '服务类型不一致')
        self.assertIn('第二诊疗意见', self.result[0][3], '第二诊疗意见的病情描述不全')
        self.assertIn('诊疗诉求', self.result[0][7], '诊疗诉求不一致')

    def check_result(self):
        connect = connectdb()
        conn = connect[0]
        self.cc = connect[1]
        self.cc.execute(
            "SELECT  id,patient_profile_id,to_doctor_id,description,type,create_by,appointment_time,appeal  FROM `dh_inquiry` WHERE to_doctor_id=%s ORDER BY id DESC " % self.doctorId)  # 查询
        self.result = self.cc.fetchall()  # 获得数据库查询结果
        conn.close()
        # 结果验证
        self.assertEqual(self.response['status'], 0, '接口连接错误')
        self.assertEqual(self.response['result']['inquiryId'], self.result[0][0], 'id返回错误')
        self.assertEqual(self.result[0][1], self.profileId, '健康档案关联错误')
        self.assertEqual(self.result[0][5], self.patientId, '提问的患者id不对')

# coding=utf-8
"""
作者：vissy@zhu
"""

# 首页接口
api_homepage = {
    'getAppHomePage': '/lyhcc/app/getAppHomePage',  # 首页数据
    'getBannerList': '/lyhcc/dhCenterBanner/getBannerList',  # 首页banner列表
    'gistCenterDocuments': '/lyhcc/dh-medical-center/gistCenterDocuments',  # 首页的科普文章列表
    'gistCenterPage': '/lyhcc/dh-medical-center/gistCenterPage',  # 首页搜索推荐中心
    'getAppSearchPage': '/lyhcc/app/getAppSearchPage',  # 首页搜索中心功能
    'gistCenterTree': '/lyhcc/dh-medical-center/gistCenterTree',  # 全球肿瘤防治中心
    'getTeamPage': '/lyhcc/dh-medical-team/getTeamPage',  # 团队列表
    'getTeamMainPage': '/lyhcc/dh-medical-team/getTeamMainPage',  # 团队主页
    'thumbUp': '/lyhcc/app/thumbUp',  # 点赞
    'getHospitalDocType': '/lyhcc/dh-medical-center/getHospitalDocType',  # 单病种中心文章分类
    'getAppGistPage': '/lyhcc/app/getAppGistPage',  # 单病种中心页
    'getDocumentList': '/lyhcc/dh-document/getDocumentList',  # 单病种名医义诊
    'getDisByCenter': '/lyhcc/dh-disease/getDisByCenter',  # 单病种中心在线答疑，关联得瘤种
    'getQuestionList': '/lyhcc/dhAsk/getQuestionList',  # 单病种中心在线答疑
    'hospitallist': '/lyhcc/dh-hospital/list',  # 肿瘤名院列表
    'getAppHospitalMainPage': '/lyhcc/app/getAppHospitalMainPage',  # 医院主页
    'selectHosMainPageEvent': '/lyhcc/app/selectHosMainPageEvent',  # 医院下专家科普专题
    'getAppHospitalDocumentPage': '/lyhcc/app/getAppHospitalDocumentPage',  # 医院下的专家科普文章
    'getDocumentDetail': '/lyhcc/dh-document/getDocumentDetail',  # 义诊详情页
    'collectDocument': '/lyhcc/dh-document/collectDocument',  # 收藏公开课
    'findListByPage': '/lyhcc/dh-disease/findListByPage',  # 瘤种数据
    'addQuestion': '/lyhcc/dhAsk/addQuestion',  # 立即提问
    'getQuestionDetail': '/lyhcc/dhAsk/getQuestionDetail',  # 问题详情页
    'getAreaTree': '/lyhcc/baseArea/getAreaTree',  # 地区接口
    'getBosConDept': '/lyhcc/dh-hospital/getBosConDept',  # 科室列表
    'getDoctorList': '/lyhcc/dh-doctor-user/list',  # 专家列表
    'findLeaguePage': '/lyhcc/dh-medical-league/findLeaguePage',  # 医联体列表
    'findLeagueById': '/lyhcc/dh-medical-league/findLeagueById',  # 医联体详情
    'getLeagueHos': '/lyhcc/dh-medical-league/getLeagueHos',  # 医联体关联的医院
    'getLeagueDoc': '/lyhcc/dh-medical-league/getLeagueDoc',  # 医联体关联的医生
    'getDoctorMainPage': '/lyhcc/app/getDoctorMainPage',  # 医生主页
    'getAppDocDocumentPage': '/lyhcc/app/getAppDocDocumentPage',  # 医生的科普文章
    'saveDhInquiry': '/lyhcc/dhInquiry/saveDhInquiry',  # 图文问诊
    'getInquirySetting': '/lyhcc/dh-doctor-user/getInquirySetting',  # 查询医生的服务设置
    'getDoctorByInquiryId': '/lyhcc/dhInquiry/getDoctorByInquiryId',  # 查询问诊的医生和问题详情
    'getPayById': '/lyhcc/dhPayment/getPayById',  # 查询问诊订单的支付状态
}
# 我的页面接口
api_mypage = {
    'appletGetPatientInfo': '/lyhcc/user/appletGetPatientInfo',  # 获取患者信息
    'updatePatient': '/lyhcc/user/updatePatient',  # 更新患者信息
    'getHospitalQuestion': '/lyhcc/user/getHospitalQuestion',  # 我的提问列表
    'getPatientPayList': '/lyhcc/dhPayment/getPatientPayList',  # 我的订单列表
    'cancelInquiry': '/lyhcc/dhInquiry/cancelInquiry',  # 取消订单
    'delPayment': '/lyhcc/dhPayment/delPayment',  # 删除订单
    'getPrePage': '/lyhcc/dhPrescription/getPrePage',  # 我的处方列表
    'getPrescriptionById': '/lyhcc/dhPrescription/getPrescriptionById',  # 处方详情页
    'getMyCollectedDocument': '/lyhcc/user/getMyColletedDocument',  # 我的收藏
    'getMyFollowedDoctor': '/lyhcc/user/getMyFollowedDoctor',  # 我关注的医生列表
    'getMyFollowed': '/lyhcc/dhPatientFocus/getMyFollowed',  # 我关注的医院和科室列表
    'addOrUpdate': '/lyhcc/dhPatientProfile/addOrUpdate',  # 新增健康档案
    'getProfileById': '/lyhcc/dhPatientProfile/getProfileById',  # 根据id获取患者的健康档案
    'getMyProfile': '/lyhcc/dhPatientProfile/getMyProfile',  # 获取当前患者的健康档案
}

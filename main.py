# coding=utf-8
"""
作者：vissy@zhu
"""
from commonlib.htmlresult import result
import unittest
from commonlib.sendemail import send_email

if __name__ == '__main__':
    case_dir = "./testcase"
    discover = unittest.defaultTestLoader.discover(case_dir, pattern='test_*.py')
    result = result()
    runner = result[0]
    runner.run(discover)
    result[1].close()
    send_email('result.html')

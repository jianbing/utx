#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import time
import unittest
from utx.BSTestRunner import BSTestRunner


class TestRunner:
    def run_test(self, path="testcase", title='接口自动化测试报告'):
        if not os.path.exists("report"):
            os.mkdir("report")

        report_file = r"report\bstest-style-{}.html".format(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())))

        suite = unittest.TestLoader().discover(path)
        with open(report_file, "wb") as f:
            runner = BSTestRunner(stream=f, title=title)
            runner.run(suite)

        print("测试完成，请查看报告")
        os.system("start report")

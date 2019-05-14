#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import time
import os
import io
import datetime
import sys
import unittest
from utx.core import Tool
from . import log, setting

result_data = dict()
result_data['testResult'] = []
current_class_name = ""
STATUS = {
    0: 'Pass',
    1: 'Fail',
    2: 'Error',
    3: 'Skip',
}


class _TestResult(unittest.TestResult):
    def __init__(self, verbosity=1):
        super().__init__(verbosity)
        self.outputBuffer = io.StringIO()
        self.raw_stdout = None
        self.raw_stderr = None
        self.success_count = 0
        self.failure_count = 0
        self.skip_count = 0
        self.error_count = 0
        self.verbosity = verbosity
        self.result = []
        self._case_start_time = 0
        self._case_run_time = 0

    def startTest(self, test):
        self._case_start_time = time.time()
        super().startTest(test)
        self.raw_stdout = sys.stdout
        self.raw_stderr = sys.stderr
        sys.stdout = self.outputBuffer
        sys.stderr = self.outputBuffer

    def complete_output(self):
        self._case_run_time = time.time() - self._case_start_time
        if self.raw_stdout:
            sys.stdout = self.raw_stdout
            sys.stderr = self.raw_stderr

        result = self.outputBuffer.getvalue()
        self.outputBuffer.seek(0)
        self.outputBuffer.truncate()
        if result and setting.show_print_in_console:
            log._print(result.strip())
        return result

    def stopTest(self, test):
        self.complete_output()

    def addSuccess(self, test):
        self.success_count += 1
        super().addSuccess(test)
        output = self.complete_output()
        self.result.append((0, test, output, '', self._case_run_time))

    def addError(self, test, err):
        self.error_count += 1
        super().addError(test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        self.result.append((2, test, output, _exc_str, self._case_run_time))
        log.error('TestCase Error')
        if setting.show_error_traceback:
            log.error(_exc_str)

    def addSkip(self, test, reason):
        self.skip_count += 1
        super().addSkip(test, reason)
        self.result.append((3, test, "", "", 0.0))

    def addFailure(self, test, err):
        self.failure_count += 1
        super().addFailure(test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        self.result.append((1, test, output, _exc_str, self._case_run_time))
        log.error('TestCase Failed')
        if setting.show_error_traceback:
            log.error(_exc_str)


class _TestRunner:
    def __init__(self, report_title, report_dir, verbosity=1, description=""):
        self.report_dir = report_dir
        self.verbosity = verbosity
        self.title = report_title
        self.description = description
        self.start_time = datetime.datetime.now()
        self.stop_time = None

    def run(self, test):
        msg = "开始测试，用例数量总共{}个，跳过{}个，实际运行{}个"
        log.info(msg.format(Tool.total_case_num,
                            Tool.total_case_num - Tool.actual_case_num,
                            Tool.actual_case_num))
        result = _TestResult(self.verbosity)
        test(result)
        self.stop_time = datetime.datetime.now()
        self.analyze_test_result(result)
        log.info('Time Elapsed: {}'.format(self.stop_time - self.start_time))

        from utx.report import style_1, style_2
        if setting.create_report_by_style_1:
            file_path = os.path.join(self.report_dir,
                                     r"{}-style-1.html".format(self.start_time.strftime("%Y-%m-%d-%H-%M-%S")))
            style_1.build_report(file_path, result_data)

        if setting.create_report_by_style_2:
            file_path = os.path.join(self.report_dir,
                                     r"{}-style-2.html".format(self.start_time.strftime("%Y-%m-%d-%H-%M-%S")))
            style_2.build_report(file_path, result_data)

    @staticmethod
    def sort_result(case_results):
        rmap = {}
        classes = []
        for n, t, o, e, run_time in case_results:
            cls = t.__class__
            if cls not in rmap:
                rmap[cls] = []
                classes.append(cls)
            rmap[cls].append((n, t, o, e, run_time))
        r = [(cls, rmap[cls]) for cls in classes]
        return r

    def analyze_test_result(self, result):
        result_data["reportName"] = self.title
        result_data["beginTime"] = str(self.start_time)[:19]
        result_data["totalTime"] = str(self.stop_time - self.start_time)

        sorted_result = self.sort_result(result.result)
        for cid, (cls, cls_results) in enumerate(sorted_result):
            pass_num = fail_num = error_num = skip_num = 0
            for case_state, *_ in cls_results:
                if case_state == 0:
                    pass_num += 1
                elif case_state == 1:
                    fail_num += 1
                elif case_state == 2:
                    error_num += 1
                else:
                    skip_num += 1

            name = "{}.{}".format(cls.__module__, cls.__name__)
            global current_class_name
            current_class_name = name

            for tid, (state_id, t, o, e, run_time) in enumerate(cls_results):

                name = t.id().split('.')[-1]
                doc = t.shortDescription() or ""
                case_data = dict()
                case_data['className'] = current_class_name
                case_data['methodName'] = name
                case_data['spendTime'] = "{:.2}S".format(run_time)
                case_data['description'] = doc
                case_data['log'] = o + e
                if STATUS[state_id] == "Pass":
                    case_data['status'] = "成功"
                if STATUS[state_id] == "Fail":
                    case_data['status'] = "失败"
                if STATUS[state_id] == "Error":
                    case_data['status'] = "错误"
                if STATUS[state_id] == "Skip":
                    case_data['status'] = "跳过"
                result_data['testResult'].append(case_data)

        result_data["testPass"] = result.success_count
        result_data["testAll"] = result.success_count + result.failure_count + result.error_count + result.skip_count
        result_data["testFail"] = result.failure_count
        result_data["testSkip"] = result.skip_count
        result_data["testError"] = result.error_count


class TestRunner:

    def __init__(self):
        self.case_dirs = []

    def add_case_dir(self, dir_path):
        """添加测试用例文件夹，多次调用可以添加多个文件夹，会按照文件夹的添加顺序执行用例

            runner = TestRunner()
            runner.add_case_dir(r"testcase\chat")
            runner.add_case_dir(r"testcase\battle")
            runner.run_test(report_title='接口自动化测试报告')

        :param dir_path:
        :return:
        """
        if not os.path.exists(dir_path):
            raise Exception("测试用例文件夹不存在：{}".format(dir_path))
        if dir_path in self.case_dirs:
            log.warn("测试用例文件夹已经存在了：{}".format(dir_path))
        else:
            self.case_dirs.append(dir_path)

    def run_test(self, report_title='接口自动化测试报告'):

        if not self.case_dirs:
            raise Exception("请先调用add_case_dir方法，添加测试用例文件夹")

        if not os.path.exists("report"):
            os.mkdir("report")

        report_dir = os.path.abspath("report")
        suite = unittest.TestSuite()
        for case_path in self.case_dirs:
            suite.addTests(unittest.TestLoader().discover(case_path))
        _TestRunner(report_dir=report_dir, report_title=report_title).run(suite)

        print("测试完成，请查看报告")
        os.system("start report")

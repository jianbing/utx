#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Created by jianbing on 2017-10-30
"""
import unittest
import functools
import time
from . import log

CASE_LEVEL_FLAG = "__case_level__"
CASE_DATA_FLAG = "__case_data__"
CASE_ID_FLAG = "__case_id__"
CASE_INFO_FLAG = "__case_info__"

__all__ = ["data", "setting", "smoke_test", "full_test", "stop_patch"]


def data(*values):
    def wrap(func):
        if hasattr(func, CASE_DATA_FLAG):
            log.error(f"{func.__name__}的测试数据只能初始化一次")
        setattr(func, CASE_DATA_FLAG, values)
        return func

    return wrap


class setting:
    # 是否开启冒烟测试
    smoke_test = False

    # 每个用例的执行间隔，单位是秒
    execute_interval = 0.1


def smoke_test(func):
    setattr(func, CASE_LEVEL_FLAG, 1)
    return func


def full_test(func):
    setattr(func, CASE_LEVEL_FLAG, 2)
    return func


def _error_handler(func):
    @functools.wraps(func)
    def __error_handler(*args, **kwargs):
        time.sleep(setting.execute_interval)

        log.info(
            f"Start to test {getattr(func, CASE_INFO_FLAG)} ({int(getattr(func, CASE_ID_FLAG))}/{Tool.total_case_num})")
        result = func(*args, **kwargs)
        return result

    return __error_handler


class Tool:
    total_case_num = 0

    @classmethod
    def general_case_id(cls):
        cls.total_case_num += 1
        case_id = "{:05d}".format(cls.total_case_num)
        return case_id

    @staticmethod
    def make_test_from_case_data(funcs: dict, raw_func, raw_func_name: str):
        for index, test_data in enumerate(getattr(raw_func, CASE_DATA_FLAG), 1):
            case_id = Tool.general_case_id()
            setattr(raw_func, CASE_ID_FLAG, case_id)

            if isinstance(test_data, list):
                func_name = raw_func_name.replace("test_", f"test_{case_id}_") + \
                            "_{:05d}_{}".format(index, "_".join([str(_) for _ in test_data]))
                funcs[func_name] = _error_handler(_feed_data(*test_data)(raw_func))

            elif isinstance(test_data, dict):
                func_name = raw_func_name.replace("test_", f"test_{case_id}_") + \
                            "_{:05d}_{}".format(index, "_".join([str(_) for _ in test_data.values()]))
                funcs[func_name] = _error_handler(_feed_data(**test_data)(raw_func))

            elif isinstance(test_data, (int, str, bool, float)):
                func_name = raw_func_name.replace("test_", f"test_{case_id}_") + "_{:05d}_{}".format(index, test_data)
                funcs[func_name] = _error_handler(_feed_data(test_data)(raw_func))

            else:
                raise Exception(f"无法解析{test_data}")

    @staticmethod
    def make_simple_test(funcs: dict, raw_func, raw_func_name: str):
        case_id = Tool.general_case_id()
        setattr(raw_func, CASE_ID_FLAG, case_id)

        func_name = raw_func_name.replace("test_", "test_{}_".format(case_id))
        funcs[func_name] = _error_handler(raw_func)


def _feed_data(*args, **kwargs):
    def _wrap(func):
        @functools.wraps(func)
        def __wrap(self):
            return func(self, *args, **kwargs)

        return __wrap

    return _wrap


class Meta(type):
    @staticmethod
    def __new__(S, *more):
        funcs = dict()
        for raw_func_name in more[-1]:
            if raw_func_name.startswith("test_"):
                raw_func = more[-1][raw_func_name]

                if not hasattr(raw_func, CASE_LEVEL_FLAG):
                    setattr(raw_func, CASE_LEVEL_FLAG, 1)

                # 注入用例信息
                case_info = "{}.{}".format(raw_func.__module__, raw_func.__name__)
                setattr(raw_func, CASE_INFO_FLAG, case_info)

                # 用例描述检查
                if not raw_func.__doc__:
                    log.warn("{}没有用例描述".format(case_info))

                if setting.smoke_test and getattr(raw_func, CASE_LEVEL_FLAG) == 2:
                    continue

                # 注入测试数据
                if hasattr(raw_func, CASE_DATA_FLAG):
                    Tool.make_test_from_case_data(funcs, raw_func, raw_func_name)
                else:
                    Tool.make_simple_test(funcs, raw_func, raw_func_name)

            else:
                funcs[raw_func_name] = more[-1][raw_func_name]

        return super(Meta, S).__new__(S, *(more[0], more[1], funcs))


class _TestCase(unittest.TestCase, metaclass=Meta):
    def shortDescription(self):
        """覆盖父类的方法，获取函数的注释

        :return:
        """
        doc = self._testMethodDoc
        doc = doc and doc.split()[0].strip() or None
        return doc


raw_unittest_testcase = unittest.TestCase
unittest.TestCase = _TestCase


def stop_patch():
    unittest.TestCase = raw_unittest_testcase

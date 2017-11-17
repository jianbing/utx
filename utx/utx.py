#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Created by jianbing on 2017-10-30
"""
import functools
import time
import unittest
from utx.setting import setting
from . import log
from .case_tag import Tag

CASE_TAG_FLAG = "__case_tag__"
CASE_DATA_FLAG = "__case_data__"
CASE_ID_FLAG = "__case_id__"
CASE_INFO_FLAG = "__case_info__"
CASE_SKIP_FLAG = "__unittest_skip__"
CASE_SKIP_REASON_FLAG = "__unittest_skip_why__"

__all__ = ["data", "skip", "stop_patch", "Tag", "tag", "setting"]


def skip(reason):
    def wrap(func):
        setattr(func, CASE_SKIP_FLAG, True)
        setattr(func, CASE_SKIP_REASON_FLAG, reason)
        return func

    return wrap


def data(*values):
    def wrap(func):
        if hasattr(func, CASE_DATA_FLAG):
            log.error("{}的测试数据只能初始化一次".format(func.__name__))
        setattr(func, CASE_DATA_FLAG, values)
        return func

    return wrap


def tag(*tag_type):
    def wrap(func):
        if not hasattr(func, CASE_TAG_FLAG):
            tags = {Tag.FULL}
            tags.update(tag_type)
            setattr(func, CASE_TAG_FLAG, tags)
        else:
            getattr(func, CASE_TAG_FLAG).update(tag_type)
        return func

    return wrap


def _handler(func):
    @functools.wraps(func)
    def __handler(*args, **kwargs):
        time.sleep(setting.execute_interval)
        msg = "Start to test {} ({}/{})".format(getattr(func, CASE_INFO_FLAG),
                                                getattr(func, CASE_ID_FLAG),
                                                Tool.total_case_num)
        log.info(msg)
        result = func(*args, **kwargs)
        return result

    return __handler


class Tool:
    total_case_num = 0

    @classmethod
    def general_case_id(cls):
        cls.total_case_num += 1
        return cls.total_case_num

    @staticmethod
    def make_case_from_case_data(raw_func_name, raw_func):
        result = dict()
        for index, test_data in enumerate(getattr(raw_func, CASE_DATA_FLAG), 1):
            case_id = Tool.general_case_id()
            setattr(raw_func, CASE_ID_FLAG, case_id)
            func_name = raw_func_name.replace("test_", "test_{:05d}_".format(case_id))

            if isinstance(test_data, list):

                func_name += "_{:05d}_{}".format(index, "_".join([str(_) for _ in test_data]))
                result[func_name] = _handler(_feed_data(*test_data)(raw_func))

            elif isinstance(test_data, dict):
                func_name += "_{:05d}_{}".format(index, "_".join([str(_) for _ in test_data.values()]))
                result[func_name] = _handler(_feed_data(**test_data)(raw_func))

            elif isinstance(test_data, (int, str, bool, float)):
                func_name += "_{:05d}_{}".format(index, test_data)
                result[func_name] = _handler(_feed_data(test_data)(raw_func))

            else:
                raise Exception("无法解析{}".format(test_data))
        return result

    @staticmethod
    def make_simple_case(raw_func_name, raw_func):
        result = dict()
        case_id = Tool.general_case_id()
        setattr(raw_func, CASE_ID_FLAG, case_id)

        func_name = raw_func_name.replace("test_", "test_{:05d}_".format(case_id))
        result[func_name] = _handler(raw_func)
        return result

    @staticmethod
    def filter_test_case(funcs_dict):
        funcs = dict()
        cases = dict()
        for i in funcs_dict:
            if i.startswith("test_"):
                cases[i] = funcs_dict[i]
            else:
                funcs[i] = funcs_dict[i]

        return funcs, sorted(cases.items(), key=lambda x: x[-1].__code__.co_firstlineno)


def _feed_data(*args, **kwargs):
    def wrap(func):
        @functools.wraps(func)
        def _wrap(self):
            return func(self, *args, **kwargs)

        return _wrap

    return wrap


class Meta(type):
    @staticmethod
    def __new__(S, *more):
        funcs, cases = Tool.filter_test_case(more[-1])
        for raw_case_name, raw_case in cases:
            if not hasattr(raw_case, CASE_TAG_FLAG):
                setattr(raw_case, CASE_TAG_FLAG, {Tag.SMOKE, Tag.FULL})  # 没有指定tag的用例，默认有SMOKE和FULL标记

            # 注入用例信息
            case_info = "{}.{}".format(raw_case.__module__, raw_case.__name__)
            setattr(raw_case, CASE_INFO_FLAG, case_info)

            # 检查用例描述
            if setting.check_case_doc and not raw_case.__doc__:
                log.warn("{}没有用例描述".format(case_info))

            # 过滤不执行的用例
            if not getattr(raw_case, CASE_TAG_FLAG) & set(setting.run_case):
                continue

            # 注入测试数据
            if hasattr(raw_case, CASE_DATA_FLAG):
                funcs.update(Tool.make_case_from_case_data(raw_case_name, raw_case))
            else:
                funcs.update(Tool.make_simple_case(raw_case_name, raw_case))

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

#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import re
import functools
import time
import unittest
from .setting import setting
from . import log
from .tag import Tag

CASE_TAG_FLAG = "__case_tag__"
CASE_DATA_FLAG = "__case_data__"
CASE_DATA_UNPACK_FLAG = "__case_data_unpack__"
CASE_ID_FLAG = "__case_id__"
CASE_INFO_FLAG = "__case_info__"
CASE_RUN_INDEX_FlAG = "__case_run_index_flag__"
CASE_SKIP_FLAG = "__unittest_skip__"
CASE_SKIP_REASON_FLAG = "__unittest_skip_why__"

__all__ = ["skip", "skip_if", "data", "tag", "stop_patch", "run_case"]


def skip(reason):
    def wrap(func):
        return unittest.skip(reason)(func)

    return wrap


def skip_if(condition, reason):
    def wrap(func):
        return unittest.skipIf(condition, reason)(func)

    return wrap


def data(*values, unpack=True):
    """注入测试数据，可以做为测试用例的数据驱动
    1. 单一参数的测试用例
    @data(10001, 10002, 10003)
    def test_receive_bless_box(self, box_id):
        print(box_id)

    2. 多个参数的测试用例
    @data(["gold", 100], ["diamond", 500])
    def test_bless(self, bless_type, award):
        print(bless_type)
        print(award)

    3. 是否对测试数据进行解包
    @data({"gold": 1000, "diamond": 100}, {"gold": 2000, "diamond": 200}, unpack=False)
    def test_get_battle_reward(self, reward):
        print(reward)
        print("获得的钻石数量是：{}".format(reward['diamond']))

    :param values:测试数据
    :param unpack: 是否解包
    :return:
    """

    def wrap(func):
        if hasattr(func, CASE_DATA_FLAG):
            log.error("{}的测试数据只能初始化一次".format(func.__name__))
        else:
            setattr(func, CASE_DATA_FLAG, values)
            setattr(func, CASE_DATA_UNPACK_FLAG, unpack)
        return func

    return wrap


def tag(*tag_type):
    """指定测试用例的标签，可以作为测试用例分组使用，用例默认会有Tag.ALL标签，支持同时设定多个标签，如：
    @tag(Tag.V1_0_0, Tag.SMOKE)
    def test_func(self):
        pass

    :param tag_type:标签类型，在tag.py里边自定义
    :return:
    """

    def wrap(func):
        if not hasattr(func, CASE_TAG_FLAG):
            tags = {Tag.ALL}
            tags.update(tag_type)
            setattr(func, CASE_TAG_FLAG, tags)
        else:
            getattr(func, CASE_TAG_FLAG).update(tag_type)
        return func

    return wrap


def _handler(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        time.sleep(setting.execute_interval)
        msg = "start to test {} ({}/{})".format(getattr(func, CASE_INFO_FLAG),
                                                getattr(func, CASE_RUN_INDEX_FlAG),
                                                Tool.actual_case_num)
        log.info(msg)
        result = func(*args, **kwargs)
        return result

    return wrap


class Tool:
    actual_case_num = 0
    total_case_num = 0

    @classmethod
    def create_case_id(cls):
        cls.total_case_num += 1
        return cls.total_case_num

    @classmethod
    def create_actual_run_index(cls):
        cls.actual_case_num += 1
        return cls.actual_case_num

    @staticmethod
    def modify_func_name(func):
        """修改函数名字，实现排序 eg test_fight ---> test_00001_fight

        :param func:
        :return:
        """
        case_id = Tool.create_case_id()
        setattr(func, CASE_ID_FLAG, case_id)
        if setting.sort_case:
            func_name = func.__name__.replace("test_", "test_{:05d}_".format(case_id))
        else:
            func_name = func.__name__
        return func_name

    @staticmethod
    def general_case_name_with_test_data(func_name, index, test_data):
        if setting.full_case_name:
            params_str = "_".join([str(_) for _ in test_data]).replace(".", "")
            func_name += "_{:05d}_{}".format(index, params_str)
        else:
            func_name += "_{:05d}".format(index)
        if len(func_name) > setting.max_case_name_len:
            func_name = func_name[:setting.max_case_name_len] + "……"
        return func_name

    @staticmethod
    def create_case_with_case_data(func):
        result = dict()
        for index, test_data in enumerate(getattr(func, CASE_DATA_FLAG), 1):
            if not hasattr(func, CASE_SKIP_FLAG):
                setattr(func, CASE_RUN_INDEX_FlAG, Tool.create_actual_run_index())

            func_name = Tool.modify_func_name(func)
            if isinstance(test_data, list):
                func_name = Tool.general_case_name_with_test_data(func_name, index, test_data)
                if getattr(func, CASE_DATA_UNPACK_FLAG, None):
                    result[func_name] = _handler(_feed_data(*test_data)(func))
                else:
                    result[func_name] = _handler(_feed_data(test_data)(func))

            elif isinstance(test_data, dict):
                func_name = Tool.general_case_name_with_test_data(func_name, index, test_data.values())
                if getattr(func, CASE_DATA_UNPACK_FLAG, None):
                    result[func_name] = _handler(_feed_data(**test_data)(func))
                else:
                    result[func_name] = _handler(_feed_data(test_data)(func))

            elif isinstance(test_data, (int, str, bool, float)):
                func_name = Tool.general_case_name_with_test_data(func_name, index, [test_data])
                result[func_name] = _handler(_feed_data(test_data)(func))

            else:
                raise Exception("无法解析{}".format(test_data))

        return result

    @staticmethod
    def create_case_without_case_data(func):
        if not hasattr(func, CASE_SKIP_FLAG):
            setattr(func, CASE_RUN_INDEX_FlAG, Tool.create_actual_run_index())

        result = dict()
        func_name = Tool.modify_func_name(func)
        if len(func_name) > setting.max_case_name_len:
            func_name = func_name[:setting.max_case_name_len] + "……"
        result[func_name] = _handler(func)
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

        return funcs, cases


def _feed_data(*args, **kwargs):
    def wrap(func):
        @functools.wraps(func)
        def _wrap(self):
            return func(self, *args, **kwargs)

        return _wrap

    return wrap


class Meta(type):
    def __new__(cls, clsname, bases, attrs):
        funcs, cases = Tool.filter_test_case(attrs)
        for test_case in cases.values():
            if not hasattr(test_case, CASE_TAG_FLAG):
                setattr(test_case, CASE_TAG_FLAG, {Tag.ALL})  # 没有指定tag的用例，默认带有tag：ALL

            # 注入用例信息
            case_info = "{}.{}".format(test_case.__module__, test_case.__name__)
            setattr(test_case, CASE_INFO_FLAG, case_info)

            # 检查用例描述
            if setting.check_case_doc and not test_case.__doc__:
                log.warn("{}没有用例描述".format(case_info))

            # 过滤不执行的用例
            if not getattr(test_case, CASE_TAG_FLAG) & set(setting.run_case):
                continue

            # 注入测试数据
            if hasattr(test_case, CASE_DATA_FLAG):
                funcs.update(Tool.create_case_with_case_data(test_case))
            else:
                funcs.update(Tool.create_case_without_case_data(test_case))

        return super(Meta, cls).__new__(cls, clsname, bases, funcs)


class _TestCase(unittest.TestCase, metaclass=Meta):
    def shortDescription(self):
        """覆盖父类的方法，获取函数的注释

        :return:
        """
        doc = self._testMethodDoc
        doc = doc and doc.split()[0].strip() or None
        return doc


TestCaseBackup = unittest.TestCase
unittest.TestCase = _TestCase


def stop_patch():
    unittest.TestCase = TestCaseBackup


def run_case(case_class, case_name: str):
    setting.execute_interval = 0.3
    r = re.compile(case_name.replace("test_", "test(_\d+)?_"))
    suite = unittest.TestSuite()
    for i in unittest.TestLoader().loadTestsFromTestCase(case_class):
        if r.match(getattr(i, "_testMethodName")):
            suite.addTest(i)
    unittest.TextTestRunner(verbosity=0).run(suite)

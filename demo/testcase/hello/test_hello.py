#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
import utx


class TestHello(unittest.TestCase):
    def test_native_case(self):
        print("hi")

    @utx.data(["小红", "1"], ["小黄", "2"])
    def test_case_with_list_data(self, name, age):
        print(name)
        print(age)

    @utx.data({"name": "小绿", "age": 3}, {"name": "小紫", "age": 4})
    def test_case_with_dict_data(self, name, age):
        """字典格式的测试数据

        :param name:
        :param age:
        :return:
        """
        print(name)
        print(age)

    @utx.data("how are you", "fine")
    def test_case_with_single_param(self, value):
        print(value)

    @utx.full_test
    def test_case_with_full_level(self):
        print("full level")

    def test_case_raise_exception(self):
        raise Exception("error")
#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest
from utx import *


class TestLegion(unittest.TestCase):
    def setUp(self):
        print('运行setUp方法')

    def tearDown(self):
        print('运行tearDown方法')

    @tag(Tag.SMOKE)
    def test_create_legion(self):
        """测试创建军团

        :return:
        """

    @tag(Tag.ALL)
    @data(["gold", 100], ["diamond", 500])
    def test_bless(self, bless_type, cost):
        """测试公会祈福

        :param bless_type: 祈福类型
        :param cost: 消耗数量
        :return:
        """
        print(bless_type)
        print(cost)

    @skip("跳过的原因")
    @data(10001, 10002, 10003)
    def test_receive_bless_box(self, box_id):
        """ 测试领取祈福宝箱

        :return:
        """
        print(box_id)

    @tag(Tag.V1_0_0, Tag.ALL)
    def test_quit_legion(self):
        """测试退出军团

        :return:
        """
        print("测试退出军团")
        assert 1 == 2

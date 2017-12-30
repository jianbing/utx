#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest
from utx import *


class TestLegion(unittest.TestCase):
    def setUp(self):
        print('setUp')

    def tearDown(self):
        print('tearDown')

    @tag(Tag.SMOKE)
    def test_create_legion(self):
        """创建军团

        :return:
        """

    @tag(Tag.FULL)
    @data(["gold", 100], ["diamond", 500])
    def test_bless(self, bless_type, award):
        print(bless_type)
        print(award)

    @skip("跳过的原因")
    @data(10001, 10002, 10003)
    def test_receive_bless_box(self, box_id):
        """ 领取祈福宝箱

        :return:
        """
        print(box_id)

    @tag(Tag.SP, Tag.FULL)
    def test_quit_legion(self):
        """退出军团

        :return:
        """
        print("吧啦啦啦啦啦啦")
        assert 1 == 2

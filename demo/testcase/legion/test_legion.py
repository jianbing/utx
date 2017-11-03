#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest
import utx


class TestLegion(unittest.TestCase):
    @utx.smoke_test
    def test_create_legion(self):
        """创建军团

        :return:
        """

    @utx.full_test
    @utx.data(["gold", 100], ["diamond", 500])
    def test_bless(self, bless_type, award):
        print(bless_type)
        print(award)

    @utx.data(10001, 10002, 10003)
    def test_receive_bless_box(self, box_id):
        """ 领取祈福宝箱

        :return:
        """
        print(box_id)

    def test_quit_legion(self):
        """退出军团

        :return:
        """
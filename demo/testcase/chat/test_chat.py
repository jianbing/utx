#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest
import utx


class TestChat(unittest.TestCase):
    def test_chat_in_world_channel(self):
        """测试世界聊天

        :return:
        """
        print("测试世界聊天")
        raise Exception("运行报错了")

    @unittest.skip("跳过此用例")
    def test_chat_in_personal_channel(self):
        """测试私聊

        :return:
        """
        print("测试私聊")

    @utx.skip("跳过此用例")
    def test_chat_in_union_channel(self):
        """测试公会聊天

        :return:
        """
        print("测试公会聊天")

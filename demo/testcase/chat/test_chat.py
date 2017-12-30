#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest


class TestChat(unittest.TestCase):
    def test_chat_in_world_channel(self):
        """测试世界聊天

        :return:
        """
        print("进行聊天")

    @unittest.skip("就是跳过了")
    def test_chat_in_personal_channel(self):
        """测试私聊

        :return:
        """
        print("私聊")

#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest
from utx import *


class TestBattle(unittest.TestCase):
    def test_start_battle(self):
        """测试开始战斗

        :return:
        """
        print("测试开始战斗")

    def test_skill_buff(self):
        """测试技能buff

        :return:
        """
        print("测试技能buff")

    @tag(Tag.V1_0_0)
    def test_normal_attack(self):
        """测试普通攻击

        :return:
        """
        print("测试普通攻击")

    @data({"gold": 1000, "diamond": 100}, {"gold": 2000, "diamond": 200}, unpack=False)
    def test_get_battle_reward(self, reward):
        """ 测试领取战斗奖励

        :return:
        """
        print(reward)
        print("测试领取战斗奖励，获得的钻石数量是：{}".format(reward['diamond']))
        log.debug("测试领取战斗奖励，获得的钻石数量是：{}".format(reward['diamond']))

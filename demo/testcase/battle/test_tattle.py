#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest
from utx import *


class TestBattle(unittest.TestCase):
    def test_start_battle(self):
        """测试战斗

        :return:
        """
        print("start battle")

    def test_skill_buff(self):
        """测试技能buff

        :return:
        """
        print("over")

    def test_normal_attack(self):
        """测试普通攻击

        :return:
        """
        print("normal attack")

    @data({"gold": 1000, "diamond": 100}, {"gold": 2000, "diamond": 200}, unpack=False)
    def test_get_battle_reward(self, reward):
        """ 领取战斗奖励

        :return:
        """
        print(reward)
        print("获得的钻石数量是：{}".format(reward['diamond']))

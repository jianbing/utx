#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
测试用例标签类
"""

from enum import Enum, unique


@unique
class Tag(Enum):
    SMOKE = 1  # 冒烟测试标记，可以重命名，但是不要删除
    FULL = 1000  # 完整测试标记，可以重命名，但是不要删除

    # 以下开始为扩展标签，自行调整
    SP = 2

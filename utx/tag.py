#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
测试用例标签类
"""

from enum import Enum, unique


class NewTag:
    def __init__(self, desc=""):
        self.desc = desc


@unique
class Tag(Enum):
    SMOKE = NewTag("冒烟")  # 冒烟测试标记，可以重命名，不要删除
    ALL = NewTag("完整")  # 完整测试标记，可以重命名，不要删除

    # 以下开始为扩展标签，自行调整
    V1_0_0 = NewTag("V1.0.0版本")
    V2_0_0 = NewTag("V2.0.0版本")


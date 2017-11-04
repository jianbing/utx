#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Created by jianbing on 2017-11-04
"""
from utx.case_tag import Tag


class setting:
    # 只运行的用例类型
    run_case = {Tag.SMOKE}

    # 每个用例的执行间隔，单位是秒
    execute_interval = 0.1

    # 开启检测用例描述
    check_case_doc = True

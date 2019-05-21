#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Created by jianbing on 2017-11-04
"""
from utx.tag import Tag


class setting:
    # 只运行的用例类型
    run_case = {Tag.ALL}

    # 开启用例排序
    sort_case = True

    # 每个用例的执行间隔，单位是秒
    execute_interval = 0.1

    # 开启检测用例描述
    check_case_doc = True

    # 显示完整用例名字（函数名字+参数信息）
    full_case_name = False

    # 测试报告显示的用例名字最大程度
    max_case_name_len = 80

    # 执行用例的时候，显示报错信息
    show_error_traceback = True

    # 测试报告样式1
    create_report_by_style_1 = True

    # 测试报告样式2
    create_report_by_style_2 = True

    # 在控制台显示print打印的内容
    show_print_in_console = False

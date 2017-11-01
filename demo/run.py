#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import utx

if __name__ == '__main__':
    utx.setting.smoke_test = True
    runner = utx.TestRunner()
    runner.run_test(r"testcase")



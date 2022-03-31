# -*- coding: utf-8 -*-
"""
@Time ： 2022/3/31 15:15
@Auth ： Yan Zeyu
@File ： Main.py
@IDE ： PyCharm

"""
import sys
from LeetCodeHelper import LeetCodeHelper

if __name__ == '__main__':
    args_len = len(sys.argv)
    if args_len < 4:
        print("Missing enough arguments, at least 2: username, password, query")
        exit(1)

    leetCodeHelper = LeetCodeHelper(sys.argv[1], sys.argv[2])
    print("running")
    leetCodeHelper.do(sys.argv[3])
    print('finished')
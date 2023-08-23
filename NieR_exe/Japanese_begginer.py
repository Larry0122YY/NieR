import sys
import time

import romkan


def main():
    print("请选择要学习下面的哪一种，输入对应的番号")
    print("直接回车.平假名")
    print("1.片假名")
    print("2.罗马字拼音")
    select = input_params(["","1","2"])
    while True:
        print("请输入罗马字或者假名：")
        print()
        select_words = input()
        result = get_result(select,select_words)
        print("--------------")
        print("结果：",result)
        print("--------------")
        print()


def get_result(select,select_words):
    if select == "":
        return  romkan.to_hiragana(select_words)
    elif select == "1":
        return romkan.to_katakana(select_words)
    elif select == "2":
        return romkan.to_roma(select_words)
    else:
        print("不能走到这里啦")
        sys.exit(1)

# 给定一个list的集合，里面放入只能输入的参数
def input_params(check_collection=[]):
    while True:
        select = input()
        if select in check_collection:
            return select
        print("输入的参数不匹配！")
        time.sleep(1)
        print("请重新输入")

if __name__ == '__main__':
    main()
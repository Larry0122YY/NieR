import TOOLS_COMMON as common


def main():
    find_cmd = common.get_find_cmd()
    print("==========================")
    print("在执行这个脚本前，请确认链接上手机，并且adb好使")
    print("==========================")
    print("请输入您想做什么事儿：")
    print("直接回车.adb logcat打开，生成一个文件在当前路径下")
    print("回车以外.分析生成的文件")
    select = input()
    if select == "":
        select_1(find_cmd)
    else:
        select_2()


def select_1(find_cmd):
    print("请输入log的文件名：(直接回车的话，就叫logcat)")
    log_name = input()
    if log_name == "":
        log_name = "logcat"
    cmd = "adb logcat | %s START > %s.log" % (find_cmd, log_name)

    print("请注意，按了回车以后，开始打log文件，您开始手动点开那个app，然后ctrl+c 断开logcat")
    input()
    print("logcat开始！！！")
    common.run_shell(cmd)


def select_2():
    print("请把生成的logcat文件拖进来：")
    file_path = common.input_file()
    file = open(file_path, "r")
    lines = file.readlines()

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("以下是找到的所有Activity：")
    for line in lines:

        if "cmp=" in line:
            e1 = line.split("cmp=")[1]
            if "Activity" in e1:
                e2 = e1.split("Activity")[0] + "Activity"
                print(e2)
                print()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    file.close()

    print("请将需要的activity输入到下面这个指令的参数中：")
    print("adb shell am start -n {params}")


if __name__ == '__main__':
    main()

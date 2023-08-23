import TOOLS_COMMON as common


def main():
    find_cmd = common.get_find_cmd()
    check_battery_main(find_cmd)


def check_battery_main(find_cmd):
    battery_cmd = "adb shell dumpsys battery | %s level" % find_cmd
    result = common.run_shell(battery_cmd)
    cur_battery= result.split(" ")[3].split("\\r\\n")[0]
    battery_disp = "当前电量为"+cur_battery+"%"
    print(battery_disp)


if __name__ == '__main__':
    main()

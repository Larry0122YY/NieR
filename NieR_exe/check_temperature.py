import time
import TOOLS_COMMON as common


def main():
    find_cmd = common.get_find_cmd()
    print("请输入每过几秒后，显示一次温度：(直接回车，默认1秒)")
    select = common.input_digital_and_none()
    if select == "":
        delay_time = 1
    else:
        delay_time = int(select)
    check_temperature_main(find_cmd, delay_time)


def check_temperature_main(find_cmd, delay_time):
    while True:
        battery_cmd = "adb shell dumpsys battery | %s temperature" % find_cmd
        rw = common.run_shell(battery_cmd)
        result = rw.split(" ")[3].split("\\r\\n")[0]
        temperature = formate_temperature(result)
        battery_disp = "当前手机温度为" + temperature + "度"
        print(battery_disp)
        time.sleep(delay_time)


def formate_temperature(num):
    temperature = ""
    for i in range(len(num)):
        if i == len(num) - 1:
            temperature += "."
        temperature += num[i]
    return temperature


if __name__ == '__main__':
    main()

import datetime, platform, socket, threading, subprocess, os, sys, time
from decimal import Decimal
import cv2, numpy, librosa

RETRY_TIMES = 5


# 获取当前系统的查找指令
def get_find_cmd():
    os = get_os()
    if os == "w":
        return "findstr"
    elif os == "l":
        return "grep"


# 获取一个视频的fps，resolution和全部的frames数量
def get_fps_resolution_allFrames(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    resolution = [width, height]

    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    return fps, resolution, frames


# 获取peak_amplitudes
def get_peak_amplitudes(video_path):
    # 将给入的fps给四舍五入一下，获得新的fps
    fps = round_to_the_neares(get_fps_resolution_allFrames(video_path)[0])
    print("fps:", fps)

    # 使用librosa处理video file，通过获取的y和sr的对象以及某个算法，算出peak_amplitudes后返回
    y, sr = librosa.load(video_path)
    frame_size = sr // int(fps)
    num_frames = len(y) // frame_size
    peak_amplitudes = [numpy.max(numpy.abs(y[i * frame_size:(i + 1) * frame_size])) for i in range(num_frames)]

    return peak_amplitudes


# 四舍五入
def round_to_the_neares(num):
    return Decimal(num).quantize(Decimal("1."), rounding="ROUND_HALF_UP")


# 给我一个file路径，返回这个file名，如：入力：/home/aaa.txt，出力：aaa
def get_filename_only(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]


# 入力：file full path，出力：只是换了新后缀；不给new_ext参数的话，相当于不要后缀
def switch_ext(file_path, new_ext=""):
    new_ext_path = os.path.join(os.path.dirname(file_path), os.path.splitext(os.path.basename(file_path))[0] + new_ext)
    return new_ext_path


# 判断当前系统是windows还是linux
def get_os():
    os = platform.system()
    if os == "Windows":
        return "w"
    elif os == "Linux":
        return "l"
    else:
        return "o"


# 写一个方法，获取path下，所有的.xxx文件的全路径
def get_all_file_path_list(path, ext):
    # 创建一个list对象all_file_list，用来装所有ext后缀文件的全路径
    all_file_list = []
    # 遍历当前path下的全部文件和文件夹对象temp
    temp = os.walk(path)
    # 遍历temp的全部文件夹
    for i in temp:
        # 遍历当前文件夹下的全部文件
        for file in i[2]:
            # 如果当前文件的后缀为ext
            if file.endswith(ext):
                # 获取当前文件的全路径
                cur_full_path = os.path.join(i[0], file)
                # 添加到all_file_list里
                all_file_list.append(cur_full_path)
    # 返回all_file_list
    return all_file_list


# 这个方法只能输入一个正确的路径
def input_path():
    # 不主动退出循环
    while True:
        # 让用户输入或者拖取一个路径
        path = input()
        # 如果是拖取的情况(此时是'打头的)
        if path.startswith("'"):
            # 去掉'号，变为一个python可以读的路径
            path = path.split("'")[1]
        # 在此确认，输入的路径是否存在
        if os.path.exists(path):
            # 存在的情况，返回此路径，循环结束
            return path
        # 不存在的情况，提示让用户重新输入
        print("请输入一个正确的路径!")
        time.sleep(1)
        print("请重新输入")


# 这个方法只能输入一个正确的folder path
def input_folder():
    # 不主动退出循环
    while True:
        # 让用户输入或者拖取一个路径
        path = input()
        # 如果是拖取的情况(此时是'打头的)
        if path.startswith("'"):
            # 去掉'号，变为一个python可以读的路径
            path = path.split("'")[1]
        # 在此确认，输入的路径是否存在 并且是一个folder
        if os.path.exists(path) and os.path.isdir(path):
            # 存在并是个folder的情况，返回此路径，循环结束
            return path
        # 不存在的情况，提示让用户重新输入
        print("请输入一个正确的folder路径!")
        time.sleep(1)
        print("请重新输入")


# 这个方法只能输入一个正确的file path
def input_file():
    # 不主动退出循环
    while True:
        # 让用户输入或者拖取一个路径
        path = input()
        # 如果是拖取的情况(此时是'打头的)
        if path.startswith("'"):
            # 去掉'号，变为一个python可以读的路径
            path = path.split("'")[1]
        # 在此确认，输入的路径是否存在 并且是一个file
        if os.path.exists(path) and os.path.isfile(path):
            # 存在并且是一个file的情况，返回此路径，循环结束
            return path
        # 不存在的情况，提示让用户重新输入
        print("请输入一个正确的file路径!")
        time.sleep(1)
        print("请重新输入")


# 给定一个list的集合，里面放入只能输入的参数
def input_params(check_collection=[]):
    while True:
        select = input()
        if select in check_collection:
            return select
        print("输入的参数不匹配！")
        time.sleep(1)
        print("请重新输入")


# 这个方法只能输入数字
def input_digital():
    while True:
        select = input()
        if select.isdigit():
            return select
        print("请输入数字～～")
        time.sleep(1)
        print("请重新输入")


# 这个方法不能输入什么都不输入
def input_not_none():
    while True:
        select = input()
        if select != "":
            return select
        print("不能什么都不输入！！")
        time.sleep(1)
        print("请重新输入")


# 这个方法只能输入数字或者空格
def input_digital_and_none():
    while True:
        select = input()
        if select.isdigit() or select == "":
            return select
        print("请输入数字～～")
        time.sleep(1)
        print("请重新输入")


# 执行batch的方法
def run_shell(cmd_list, if_thread=False):
    if isinstance(cmd_list, str):
        cmd = cmd_list
    else:
        cmd = " && ".join(cmd_list)
    rw = None
    if if_thread:
        subprocess.run(cmd, shell=True)
    else:
        return_bytes = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read()
        rw = str(return_bytes)

    return rw


# root并且remount手机
def root_and_remount():
    ROOT = "adb root"
    REMOUNT = "adb remount"
    REMOUNT_SUCCESS_FLAG = "remount succeeded"
    REBOOT_REMINDER = "Now reboot your device for settings to take effect"

    cmd = "&&".join([ROOT, REMOUNT])
    root_remount_rw = run_shell(cmd)
    print("root_remount_rw:" + root_remount_rw)
    if REBOOT_REMINDER in root_remount_rw:
        print("好像是刷机后的第一次root and remount，要不要重启？")
        print("enter.重启\t enter以外的任意键.不重启")
        select_reboot = input()
        if select_reboot == "":
            reboot_for_wait()
            root_and_remount()
        else:
            print("root remount失败，正在退出程序")
            sys.exit(3)
    else:
        if REMOUNT_SUCCESS_FLAG in root_remount_rw:
            print("root和remount成功，adb可以使用")
        else:
            print("root remount失败，正在退出程序")
            sys.exit(3)


def reboot_for_wait():
    run_shell("adb reboot")
    while True:
        un_connect_words = "no devices/emulators found"
        rw = run_shell("adb root")
        if not un_connect_words in rw:
            break
        print("didn't connected")
        time.sleep(10)
    print("phone is wake up!")
    time.sleep(20)


# 获取当前时间
def get_time_now():
    formate_words = "%Y%m%d_%H%M%S"
    date_time_now = datetime.datetime.now().strftime(formate_words)
    return date_time_now


# 获取当前电脑的ip
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


class adb_logcat_thread(threading.Thread):

    def __init__(self, path="/home/managelocal/Desktop", file="logcat.txt"):
        threading.Thread.__init__(self)
        self.path = path
        self.file = file

    def run(self) -> None:
        self.__run_adb_logcat()

    def __run_adb_logcat(self):
        clean_adb_logcat = "adb logcat -c"
        adb_logcat = "adb logcat > %s/%s" % (self.path, self.file)
        cmd = "&&".join([clean_adb_logcat, adb_logcat])
        print(cmd)
        run_shell(cmd)

    def stop_logcat(self):
        cur_port = self.__get_cur_logcat_port()
        cmd_kill_adb_logcat = "adb shell kill %s" % cur_port
        kill_result = run_shell(cmd_kill_adb_logcat)
        ret_num = -1
        if kill_result == "b''":
            ret_num = 0
        elif "No such process" in kill_result:
            ret_num = 1

        return ret_num

    def __get_cur_logcat_port(self):
        cmd = "adb shell ps -A | grep logcat"
        return_words = run_shell(cmd).split(" ")
        cur_port = None
        for cur_element in return_words:
            if cur_element.isdigit():
                cur_port = cur_element
                break
        return cur_port

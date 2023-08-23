import os, sys, time
import TOOLS_COMMON as common, EXCEL_SERVICE as SERVICE, EXCEL_DAO as DAO

# 执行py文件的路径在excel里的对应name
exe_path_name = "NieR_exe_path"


def main(argv):
    # 创建本文件的yuanye类对象yy
    yy = yuanye()
    # 判断是否给的参数大于1(因为本身就有1个参数，就是当前的py的路径，所以必须大于1)
    # 参数大于1的情况(调用aa时，给了参数的情况)：
    if len(argv) > 1:
        # 调用yy.run(exe_code)方法，参数为给入的第二个参数，
        yy.run(argv[1])

    # 参数不大于1的情况(调用aa时，没有给参数的情况)：
    else:
        # while无限循环：
        while True:
            # 打印信息提示用户，退出的方法
            print("退出想退出程序的话：ctrl+c")
            # 展示执行的所有选项，并让用户选择要执行的exe_code
            exe_code = yy.select_what_you_wanna_do()
            # 调用yy.run(exe_code)方法，参数为用户选择的exe_code
            yy.run(exe_code)


class yuanye:

    # yuanye类，初始化成员变量
    def __init__(self):
        # 拿到py files的执行路径，赋予成员变量self.exe_path
        self.exe_path = SERVICE.get_cur_value_by_search(search_words="NieR_exe_path")

        # 拿到所有的exe_code list，赋予成员变量self.list_for_check_exe_code
        self.list_for_check_exe_code = DAO.get_the_whole_column_data(sheet_name="py_files", column_name="exe_code")

        # 拿到展示用的list，赋予成员变量self.dict_for_show
        self.dict_for_show, self.dict_for_show_type, self.dict_for_description = SERVICE.get_dict_for_show(
            sheet_name="py_files")

        # 拿到exe_code :py file的字典，赋予成员变量self.exe_py_dict
        self.exe_py_dict = SERVICE.get_exe_py_dict()

        # 获取python的执行器，linux是python3，windows就是python
        cur_os = common.get_os()
        if cur_os == "l":
            self.python_exe = "python3"
        elif cur_os == "w":
            self.python_exe = "python"
        else:
            print("不是win也不是lin，不知道是啥系统，程序结束")
            sys.exit(4)

    # check exe code是否正确
    def direct_exe_check(self, exe_code):

        # 给入的exe code 是否在list_for_check_exe_code里
        # 如果在
        if exe_code in self.list_for_check_exe_code:
            # 返回true
            return True

        # 如果不在
        else:
            # 返回False
            return False

    # 展示所有的功能
    def select_what_you_wanna_do(self):
        # 展示所有的类型
        # 遍历self.dict_for_show_type的所有key，然后以下面的形式进行打印
        # key + "." + self.dict_for_show_type[key]
        for key in self.dict_for_show_type.keys():
            print(key + "." + self.dict_for_show_type[key])

        # 延迟0.5秒后
        time.sleep(.5)

        # 打印提示信息，让用户输入选择的type，输入后，check是否输入正确
        print("请输入序号，选择您想要的分类：")
        type_key_select = common.input_params(self.dict_for_show_type.keys())

        # 通过用户输入的序号，拿到type
        cur_select_type = self.dict_for_show_type[type_key_select]
        # 以用户选择的type放入dict_for_show字典中，拿到所有case的展示信息
        cando_case_list = self.dict_for_show[cur_select_type]
        print("============================")

        # 展示当前用户选择的type的所有case
        for case in cando_case_list:
            print(case)

        # 延迟0.5秒后
        time.sleep(.5)

        # 打印提示信息，让用户输入选择的exe code，输入后，check是否输入正确
        print("请输入你想做的事情的序号：")
        run_select = common.input_params(self.list_for_check_exe_code)

        # 返回用后选择的exe code
        return run_select

    # 执行选中的功能
    def run(self, exe_code):
        # 将給入exe code进行check是否输入正确
        exe_code_checked = self.direct_exe_check(exe_code)
        # 如果输入正确
        if exe_code_checked:
            # 打印log，展示当前执行的exe code
            print("===============================")
            print("exe_code:" + str(exe_code))
            print("description:" + self.dict_for_description[exe_code])
            print("===============================")

            # 通过当前的exe_code，获取py file全路径名
            cur_py_full_path = os.path.join(self.exe_path, self.exe_py_dict[exe_code])

            # 调用python的执行指令，执行当前的py file
            cmd = ("%s " + cur_py_full_path + ".py") % self.python_exe
            common.run_shell(cmd, if_thread=True)
            # print("cur_python_cmd:\t" + cmd)

            # 退出程序
            sys.exit(2)

        # 如果输入不正确
        else:
            # 打印log，退出程序
            print("执行玛输入错误！")
            sys.exit(3)


if __name__ == '__main__':
    main(sys.argv)

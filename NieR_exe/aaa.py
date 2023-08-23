import os, openpyxl, sys, shutil
import EXCEL_SERVICE as SERVICE, EXCEL_DAO as DAO


# 这个类的主要作用就是：
# 1 check NieR.xlsx里的路径是否都正确
# 2 pycharm的file和excel的file是否一致
# 3 check一下所有的exe code 不能重名，必须为数字
# final 删除目前执行路径的所有执行文件，然后复制pycharm的路径的文件过去


def main(argv):
    yy = yuanye()
    yy.run()


class yuanye:

    def __init__(self):
        # pycharm和exe的py path
        self.pycharm_path, self.exe_path = DAO.get_pycharm_exe_path()

    # final 删除目前执行路径的所有执行文件，然后复制pycharm的路径的文件过去
    def StepF_update_exe_py_path(self):
        # 删除exe 路径下的所有.py文件
        old_exe_files = os.listdir(self.exe_path)
        for old_file in old_exe_files:
            # 获取当前遍历到的文件的全路径
            cur_file_absolute_path = os.path.join(self.exe_path, old_file)
            # 当当前文件是文件，并且是py文件的时候，并且不是自己aaa.py的时候
            if cur_file_absolute_path.endswith(".py") and os.path.isfile(
                    cur_file_absolute_path) and not old_file != "aaa.py":
                # 删除当前文件
                os.remove(cur_file_absolute_path)

        # 遍历pycharm path里的所有文件
        cur_pycharm_files = os.listdir(self.pycharm_path)
        for pycharm_file in cur_pycharm_files:
            # 获取当前遍历到的文件的全路径
            cur_pycharm_absolute_file = os.path.join(self.pycharm_path, pycharm_file)
            # 当当前文件是文件，并且是py文件的时候
            if cur_pycharm_absolute_file.endswith(".py") and os.path.isfile(cur_pycharm_absolute_file):
                # 将当前文件复制到目标exe path下
                shutil.copy(cur_pycharm_absolute_file, self.exe_path)

    # 遍历pycharm里的所有文件，然后获取py的文件，然后萃取没有.py的所有文件名，返回到list_pycharm_files中
    def __get_pycharm_files_list(self):
        list_pycharm_files = []

        files = os.listdir(self.pycharm_path)
        for file in files:
            # 将所有的pycharm里NieR folder里的py文件给放入pycharm list里
            cur_file_path = os.path.join(self.pycharm_path, file)
            if os.path.isfile(cur_file_path):
                if file.endswith(".py"):
                    cur_file = file.split(".")[0]
                    list_pycharm_files.append(cur_file)

        return list_pycharm_files

    # 3 check一下所有的exe code 不能重名，必须唯一
    def Step3_check_exe_code(self):
        # 创建一个返回值对象result，默认list中没有重复的exe code
        result = "OK"
        # 找到list中重名的exe code
        exe_code_list = DAO.get_the_whole_column_data(column_name="exe_code")
        # 创建一个set，将list去除重名后，放入
        set_list = set(exe_code_list)
        # 遍历当前这个set
        for i in set_list:
            # 如果这个set里的元素与list里的相同
            if i in exe_code_list:
                # 在list中删除这个元素
                exe_code_list.remove(i)
        # 最终，这个list如果大于0，说明，list中有重复的元素
        if len(exe_code_list) > 0:
            # 将重复的元素的list变为string类型，放入返回值对象result中
            result = str(exe_code_list)

        # 返回返回值
        return result

    # 2 pycharm的file和excel的file是否一致
    def Step2_compare_pycharm_with_excel(self):
        # 获取基础的py files的文件，因为不是执行用的py files，在excel constructs sheet里
        constructs_py_files = DAO.get_the_whole_column_data(sheet_name="constructs", column_name="py_file")

        # 从excel的py_files sheet里拿到所有的没有后缀名的py file
        py_file_list_excel = DAO.get_the_whole_column_data()

        # 遍历pycharm里的所有去除了.py的py文件名，返回到list_pycharm_files中
        list_pycharm_files = self.__get_pycharm_files_list()

        # 用list_pycharm_files和py_file_list_excel进行比较
        # 遍历整个list_pycharm_files的元素，一一测试是否在py_file_list_excel中也存在同样的元素
        pycharm_only = []
        for pycharm_files in list_pycharm_files:
            #   如果py_file_list_excel里没有，而pycharm里有的情况
            if pycharm_files not in py_file_list_excel and pycharm_files not in constructs_py_files:
                pycharm_only.append(pycharm_files)

        # 遍历整个py_file_list_excel的元素，一一测试是否在list_pycharm_files中也存在同样的元素
        excel_only = []
        for py_file_excel in py_file_list_excel:
            #   如果py_file_list_excel里有，而pycharm里没有的情况
            if py_file_excel not in list_pycharm_files:
                excel_only.append(py_file_excel)

        if len(pycharm_only) == 0:
            print("NieR.xlsx里包含所有pycharm里的pyfile！")
            print("++++++++++++++OK+++++++++++++++++++++++")
        else:
            print("NieR.xlsx里不包含所有pycharm里的pyfile！不包含的(只有pycharm里有的)如下：")
            print(pycharm_only)
            print("-----------------------------NG--------------------------------------")

        if len(excel_only) == 0:
            print("pycharm里包含所有NieR.xlsx里的pyfile！")
            print("++++++++++++++OK+++++++++++++++++++++++")
        else:
            print("pycharm里不包含所有NieR.xlsx里的pyfile！不包含的(只有NieR.xlsx里有的)如下：")
            print(excel_only)
            print("-----------------------------NG--------------------------------------")

        if len(pycharm_only) == 0 and len(excel_only) == 0:
            return True
        else:
            return False

    # 1 check NieR.xlsx里的路径是否都正确
    def Step1_check_params_from_excel(self):
        print("请确认：NieR的路径是不是下面这样的")
        print("\t" + DAO.NIER_FILE_PATH)
        print("如果是，直接按回车继续")
        print("如果不是，按ctrl+c，退出程序，修改TOOLS_EXCEL_PROCESS.py里的代码")
        input()

        try:
            # 拿到NieR.xlsx的路径,以及book对象
            book = openpyxl.load_workbook(DAO.NIER_FILE_PATH)
        except:
            print("NieR的路径不正确！退出程序")
            sys.exit(3)

        # 创建一个字典，将需要检索的值，带入
        dict_for_check = {}
        dict_for_check["NieR_pycharm_path"] = ""
        dict_for_check["NieR_exe_path"] = ""
        dict_for_check["WORK_SPACE_FILE"] = ""
        # 将字典更新，更新后字典里会出现检索出来的值
        dict_for_check = SERVICE.get_dict_value_by_search(dict_for_check)

        print("在执行之前，请确认以下3点")
        print("1 pycharm 执行用的py文件是不是在这个文件夹下，" + dict_for_check["NieR_pycharm_path"])
        print("2 系统中执行py用的路径是不是 " + dict_for_check["NieR_exe_path"])
        print("3 下面这个路径下的文件是否存在？并且里面的workspace是正确的？")
        print("\t" + dict_for_check["WORK_SPACE_FILE"])
        print("确认好以后，直接按回车～")
        input()

        # excel的操作全部完成，关闭book流
        book.close()

    def run(self):
        # 1 check NieR.xlsx里的路径是否都正确
        self.Step1_check_params_from_excel()
        print("Step1:确认完毕！")
        print("=================================================")

        # 2 pycharm的file和excel的file是否一致
        # 用当前的pycharm里的pyfile和excel里的pyfile进行比较
        # 展示比较的结果，然后请手动修改，修改后，再次比较，直到完全统一
        while True:
            result = self.Step2_compare_pycharm_with_excel()
            if result:
                print("pycharm和excel里的pyfiles没有差分！")
                break
            print("pycharm和excel里有差分，请手动修改好差分后再次比较，或者退出程序")
            print("再次比较：按回车；退出程序：回车以外任意键")
            compare_again_cmd = input()
            if compare_again_cmd != "":
                print("程序正在退出")
                sys.exit(4)
        print("Step2:比较完毕！")
        print("=================================================")

        # 3 check一下所有的exe code 不能重名，必须唯一
        while True:
            result3 = self.Step3_check_exe_code()
            if result3 == "OK":
                print("exe_code正常，没有重复的")
                break

            print("exe_code中，有重复的指令" + result3 + ",请手动修改好差分后再次check，或者退出程序")
            print("再次check：按回车；退出程序：回车以外任意键")
            compare_again_cmd = input()
            if compare_again_cmd != "":
                print("程序正在退出")
                sys.exit(4)
        print("Step 3:check execode完毕！")
        print("=================================================")

        # final 删除目前执行路径的所有执行文件，然后复制pycharm的路径的文件过去
        self.StepF_update_exe_py_path()
        print("Step Final:删除完毕！")


if __name__ == '__main__':
    main(sys.argv)

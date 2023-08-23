import os

import TOOLS_COMMON as common

def main():
    print("请拖进来一个folder,将在这个folder里进行删除：")
    select_path = common.input_path()
    print("select_path:", select_path)
    print("请输入一个后缀，将在这个folder下删除所有这个后缀的文件：")
    suffix = common.input_not_none()
    delete_all_file_by_given_ext(select_path,suffix)
    print("删除完成！")


def delete_all_file_by_given_ext(folder_name,ext):
    temp = os.walk(folder_name)
    for i in temp:
        for file in i[2]:
            if file.endswith(ext):
                cur_full_file_path = os.path.join(i[0],file)
                os.remove(cur_full_file_path)



if __name__ == '__main__':
    main()
import sys, openpyxl, os

NIER_FILE_PATH = os.path.join(os.path.dirname(__file__), "resource", "NieR.xlsx")

# 封装方法，通过row column，sheet拿到单元格里的value
def get_cur_value(sheet, row, column):
    cur_value = sheet.cell(row=row, column=column).value
    return cur_value


# 拿到book
def get_book():
    book = openpyxl.load_workbook(NIER_FILE_PATH)
    return book


# 关闭book流
def close_book(book):
    book.close()


# 拿到pycharm和exe的path
def get_pycharm_exe_path():
    book = get_book()
    sheet = book["base"]

    pycharm_path, exe_path = None, None

    # 遍历所有的行
    for row in range(1, sheet.max_row + 1):
        # 再每次的行中，遍历所有的列
        for column in range(1, sheet.max_column + 1):
            # 获取当前单元格中的value
            cur_value = get_cur_value(row=row, column=column, sheet=sheet)
            # 如果第二列(name)的值是NieR_pycharm_path的话，那么获取同行的第三列的value并且赋值给pycharm_path
            if column == 2 and cur_value == "NieR_pycharm_path":
                pycharm_path = get_cur_value(row=row, column=column + 1, sheet=sheet)
                # 如果第二列(name)的值是NieR_exe_path的话，那么获取同行的第三列的value并且赋值给exe_path
            if column == 2 and cur_value == "NieR_exe_path":
                exe_path = get_cur_value(row=row, column=column + 1, sheet=sheet)

    close_book(book)

    return pycharm_path, exe_path


# 从excel的某列列名中，拿到这一列的所有数据
def get_the_whole_column_data(sheet_name="py_files", column_name="py_file"):
    book = get_book()
    sheet = book[sheet_name]
    py_file_list_excel = []

    # 通过给入的column_name，找到列数
    column_number = get_column_by_name(sheet, column_name)

    # 遍历NieR.xlsx中sheet py_files的所有行
    for row in range(2, sheet.max_row + 1):
        # 将除了第一行以外的py_file那一列的数据放入list self.py_file_list_excel中
        cur_value = get_cur_value(row=row, column=column_number, sheet=sheet)
        py_file_list_excel.append(str(cur_value))

    # 关闭book流
    close_book(book)
    # 返回获取到的当前列的数据
    return py_file_list_excel


# 通过列名，找到列数
def get_column_by_name(sheet, column_name):
    # param1 当前sheet
    # parma2 需要search的列名

    # 列数的变量，默认设置为0
    column_number = 0
    # 遍历所有列
    for column in range(1, sheet.max_column + 1):
        # 拿到当前列第一行的cell的value
        cur_value = sheet.cell(row=1, column=column).value
        # 当前给入的列名和当前的cell 的value相同的时候
        if cur_value == column_name:
            # 获取当前的value列数
            column_number = column

    # 当整个第一行的所有列，都没有和当前给的列名相同时
    if column_number == 0:
        # 打印log
        print("没有" + column_name + "这一列！")
        # 退出程序
        sys.exit(2)

    return column_number

import EXCEL_DAO as DAO


# 通过查找列的一个数据，来找到结果列那一行的数据
# param:
# search_words：需要检索的cell的值
# sheet_name : 操作sheet的名字
# search_words_title：给出检索的cell的列名
# result_words_title：结果列的cell的列名

# return words：检索出来的cell的value
def get_cur_value_by_search(search_words, sheet_name="base", search_words_title="name",
                            result_words_title="value"):
    cur_value = None

    # 通过sheet_name拿到sheet的对象
    book = DAO.get_book()
    sheet = book[sheet_name]
    # 通过search_words_title拿到search_words_column 查找列的列数
    search_words_column = DAO.get_column_by_name(sheet, search_words_title)
    # 通过result_words_title拿到result_words_column 结果列的列数
    result_words_column = DAO.get_column_by_name(sheet, result_words_title)

    # 遍历所有行
    for row in range(1, sheet.max_row + 1):
        # 拿到当前查找列的，当前行的cell的数据
        cur_name = sheet.cell(row=row, column=search_words_column).value
        # 如果当前的cell的数据和给入的查找words相同的时候
        if cur_name == search_words:
            # 获取结果列和当前行的这个cell的value
            cur_value = sheet.cell(row=row, column=result_words_column).value
    # 关闭book流
    DAO.close_book(book)

    # 将获取的结果的value返回
    return cur_value


# 批量的：通过查找列的一个数据，来找到结果列那一行的数据
# param:
# dict_for_check：需要检索的多个cell组成的字典：
#       字典中一个元素的格式：需要检索的cell的value:""
# sheet_name : 操作sheet的名字
# search_words_title：给出检索的cell的列名
# result_words_title：结果列的cell的列名

# return words：检索出来的值，带入字典后的字典
#     格式：需要检索的cell的value:value
def get_dict_value_by_search(dict_for_check, sheet_name="base", search_words_title="name",
                             result_words_title="value"):
    # 通过sheet_name拿到sheet的对象
    book = DAO.get_book()
    sheet = book[sheet_name]

    # 通过search_words_title拿到search_words_column 查找列的列数
    search_words_column = DAO.get_column_by_name(sheet, search_words_title)
    # 通过result_words_title拿到result_words_column 结果列的列数
    result_words_column = DAO.get_column_by_name(sheet, result_words_title)

    # 遍历所有行
    for row in range(1, sheet.max_row + 1):
        # 拿到当前查找列的，当前行的cell的数据
        cur_value = DAO.get_cur_value(row=row, column=search_words_column, sheet=sheet)
        # 如果当前的cell的数据和给入的查找words相同的时候
        if cur_value in dict_for_check.keys():
            # 获取结果列和当前行的这个cell的value
            dict_for_check[cur_value] = DAO.get_cur_value(row=row, column=result_words_column, sheet=sheet)

    # 关闭book流
    DAO.close_book(book)

    return dict_for_check


# 取得一个{exe code:py file name没有后缀}的字典
def get_exe_py_dict(sheet_name="py_files"):
    book = DAO.get_book()
    sheet = book[sheet_name]

    # 创建一个用来装exe code 和py file 的字典
    exe_py_dict = {}

    # 拿到exe_code的列数
    exe_column_number = DAO.get_column_by_name(sheet, "exe_code")
    # 拿到py_file的列数
    pyfile_column_number = DAO.get_column_by_name(sheet, "py_file")
    # 遍历所有行
    for row in range(2, sheet.max_row+1):
        # 获取当前行的 exe_code列的cell的value
        cur_execode = str(DAO.get_cur_value(sheet=sheet, row=row, column=exe_column_number))
        # 获取当前行的 py_file列的cell的value
        cur_pyfile_name = DAO.get_cur_value(sheet=sheet, row=row, column=pyfile_column_number)
        # 如果当前exe_code列的value不为0的时候，也就是不是aa或者aaa这些基础py的exe code的时候
        if cur_execode != "0":
            # 将当前exe code 对应的py file都添加进字典
            exe_py_dict[cur_execode] = cur_pyfile_name

    DAO.close_book(book)

    # 返回当前的装exe code 和py file 的字典
    return exe_py_dict


# 拿到展示用的list
def get_dict_for_show(sheet_name = "py_files"):
    # 拿到book对象
    book = DAO.get_book()
    # 通过给入的sheet_name，拿到当前sheet对象
    sheet = book[sheet_name]

    # 创建一个字典用来装所有需要展示的信息：dict_for_show = {}
    # 格式：key是type，值是case 展示信息:cur_execode + "." + cur_description; 如：1.杀掉camera的process
    dict_for_show = {}
    # 为了让用户选择type的大类，创建一个字典：dict_for_show_type = {}
    # 格式：key是index，值是type；# 如：1.common
    dict_for_show_type = {}
    # 为了每次执行code的时候打印出他的description来，创建一个字典dict_for_description
    # 格式{exe_code:description}
    dict_for_description = {}


    # 拿到exe_code的列数
    exe_column_number = DAO.get_column_by_name(sheet, "exe_code")
    # 拿到description的列数
    description_column_number = DAO.get_column_by_name(sheet, "description")
    # 拿到type的列数
    type_column_number = DAO.get_column_by_name(sheet, "type")

    # 给dict_for_show赋予数据
    # 遍历所有的行
    for row in range(2, sheet.max_row + 1):
        # 拿到"当前行"x"type列"cell的value：cur_type
        cur_type = DAO.get_cur_value(sheet, row=row, column=type_column_number)
        # 如果cur_type不在dict_for_show的keys()里，说明在这个excel里第一次1遇到(因为后面会有添加cur_type的操作)
        if cur_type not in dict_for_show.keys():
            # 以当前的cur_type为key，值暂时用一个空的list
            dict_for_show[cur_type] = []

        # 拿到当前行的exe_code的cell的value：cur_execode
        cur_execode = str(DAO.get_cur_value(sheet, row=row, column=exe_column_number))
        # 拿到当前行的description的cell的value：cur_description
        cur_description = DAO.get_cur_value(sheet, row=row, column=description_column_number)

        # 如下：exe code和description的组合字符串，为当前case 的展示信息：cur_show_words
        # cur_show_words = cur_execode + "." + cur_description
        cur_show_words = cur_execode + "." + cur_description
        # 在dict_for_show中，拿到key为cur_type的value list并且添加cur_typecur_show_words
        dict_for_show[cur_type].append(cur_show_words)
        # {exe_code:description}
        dict_for_description[cur_execode] = cur_description

    # 给dict_for_show_type赋予数据
    # 设置初始序号为1：count
    count = 1
    # 遍历dict_for_show的所有key，也就是所有的type
    for key in dict_for_show.keys():
        # 用当前的count为key(count变为string类型)，当前的dict_for_show的key为值，加入字典
        dict_for_show_type[str(count)] = key
        # 每次赋予完成，序号的好数加一
        count += 1

    # 关闭当前book的流
    DAO.close_book(book)

    # 将开头的3个字典返回dict_for_show, dict_for_show_type,dict_for_description
    return dict_for_show, dict_for_show_type,dict_for_description

# 拿到pycharm和exe的path
def get_pycharm_exe_path():
    book = DAO.get_book()
    sheet = book["base"]

    pycharm_path, exe_path = None, None

    # 遍历所有的行
    for row in range(1, sheet.max_row + 1):
        # 再每次的行中，遍历所有的列
        for column in range(1, sheet.max_column + 1):
            # 获取当前单元格中的value
            cur_value = DAO.get_cur_value(row=row, column=column, sheet=sheet)
            # 如果第二列(name)的值是NieR_pycharm_path的话，那么获取同行的第三列的value并且赋值给pycharm_path
            if column == 2 and cur_value == "NieR_pycharm_path":
                pycharm_path = DAO.get_cur_value(row=row, column=column + 1, sheet=sheet)
                # 如果第二列(name)的值是NieR_exe_path的话，那么获取同行的第三列的value并且赋值给exe_path
            if column == 2 and cur_value == "NieR_exe_path":
                exe_path = DAO.get_cur_value(row=row, column=column + 1, sheet=sheet)

    DAO.close_book(book)

    return pycharm_path, exe_path
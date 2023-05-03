import openpyxl


def get_cis_list():
    # 加载工作簿
    workbook = openpyxl.load_workbook('benchmarks_comparison.xlsx')

    # 选择工作表
    worksheet = workbook.active

    # 获取B列的所有内容和字体属性
    cis_list = []
    for row in worksheet.iter_rows(min_row=1, min_col=2, max_col=2):
        cell = row[0]
        cell_value = cell.value
        cell_font = cell.font
        if cell.value is not None and cell_font.bold is False:
            cis_list.append(cell_value)
    return cis_list


# 输出B列的内容和字体属性
print(len(get_cis_list()))

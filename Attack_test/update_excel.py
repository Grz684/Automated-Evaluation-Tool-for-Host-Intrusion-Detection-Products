import os
import pandas as pd

folder_path = 'Attack'
attack_file_names = []
for dirpath, dirnames, filenames in os.walk(folder_path):
    for file_name in filenames:
        attack_file_names.append(file_name)

# 读取Excel文件
file_path = "attack_test.xlsx"
df = pd.read_excel(file_path)

# 创建新列并将其值初始化为空字符串
df["新列"] = ""

# 进行匹配
for index, row in df.iterrows():
    matched_elements = []
    for attack_file_name in attack_file_names:
        if row["攻击技术"][:5] == attack_file_name[:5]:
            matched_elements.append(attack_file_name)

    # 如果有匹配的元素，将它们用逗号分隔并添加到新列中
    if matched_elements:
        df.loc[index, "新列"] = ', '.join(matched_elements)

# 将结果保存到新的Excel文件
output_file_path = "output_excel_file.xlsx"
df.to_excel(output_file_path, index=False, engine='openpyxl')

import sqlite3
import numpy as np
import openpyxl
from transformers import AutoTokenizer, AutoModel
import torch
from scipy.spatial.distance import cosine
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple


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


def gpu_similarity_batch(texts1: List[str], texts2: List[str]) -> List[List[float]]:
    texts1_embeddings = get_sentence_embedding_batch(texts1)
    texts2_embeddings = get_sentence_embedding_batch(texts2)
    print(texts1_embeddings)
    print(texts2_embeddings)
    similarity_matrix = cosine_similarity(texts1_embeddings, texts2_embeddings)
    return similarity_matrix


def get_sentence_embedding_batch(sentences: List[str]) -> np.ndarray:
    inputs = tokenizer(sentences, return_tensors="pt", padding=True, truncation=True).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
    return embeddings


def find_best_matches(cn_desc_list, check_item_list, similarity_func, similarity_threshold=0.5):
    similarity_matrix = similarity_func(cn_desc_list, check_item_list)

    # 找到最佳匹配的索引
    best_matches_from_cn_desc = np.argmax(similarity_matrix, axis=1)
    best_matches_from_check_item = np.argmax(similarity_matrix, axis=0)

    # 确定最佳匹配的相似度
    max_similarity_from_cn_desc = np.max(similarity_matrix, axis=1)
    max_similarity_from_check_item = np.max(similarity_matrix, axis=0)

    matched_pairs = []

    for i, j in enumerate(best_matches_from_cn_desc):
        # print(f"单向匹配：{cn_desc_list[i]} - {check_item_list[j]}，相似度：{max_similarity_from_cn_desc[i]}")
        if max_similarity_from_cn_desc[i] >= similarity_threshold and best_matches_from_check_item[j] == i:
            matched_pairs.append((cn_desc_list[i], check_item_list[j], max_similarity_from_cn_desc[i]))

    return matched_pairs


# 示例用法
if __name__ == '__main__':
    # 连接云锁数据库并读取cn_desc列
    db1 = sqlite3.connect('../PF_test/yunsuo_pf_test/yunsuo_cis_baseline_scan_items.db')
    cursor1 = db1.cursor()
    cursor1.execute('SELECT cn_desc FROM items')
    cn_desc_data = cursor1.fetchall()

    # 连接阿里cis数据库并读取check_item列
    db2 = sqlite3.connect('../PF_test/ali_pf_test/ali_cis_baseline_scan_items.db')
    cursor2 = db2.cursor()
    cursor2.execute('SELECT check_item FROM items')
    check_item_data = cursor2.fetchall()

    # 连接腾讯cis数据库并读取item_name列
    db2 = sqlite3.connect('../PF_test/tencent_pf_test/tencent_cis_baseline_scan_items.db')
    cursor2 = db2.cursor()
    cursor2.execute('SELECT item_name FROM items')
    item_name_data = cursor2.fetchall()

    # 处理结果
    cn_desc_list = [row[0] for row in cn_desc_data]
    check_item_list = [row[0] for row in check_item_data]
    item_name_list = [row[0] for row in item_name_data]
    cis_list = get_cis_list()

    # 关闭数据库连接
    cursor1.close()
    db1.close()
    cursor2.close()
    db2.close()

    # 如果有可用的 GPU，将模型和输入放在 GPU 上
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    # 使用预训练模型
    model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name).to(device)

    # cn_desc_list = ['确保已禁用SSH HostbasedAuthentication', '确保禁止用户向ssh守护程序提供环境选项', '确保仅使用经过批准的MAC算法', '确保SSH LoginGraceTime设置为一分钟或更短']
    # check_item_list = ['确保只使用了已批准的MAC算法', '确保SSH LoginGraceTime设置为小于60秒', '确保SSH的PermitUserEnvironment被禁用', '确保SSH的HostbasedAuthentication被禁用']

    # 使用 gpu_similarity_batch 作为相似度函数
    matched_pairs = find_best_matches(cn_desc_list, cis_list, gpu_similarity_batch, similarity_threshold=0.3)
    print("匹配的句子对：")
    print(len(matched_pairs))
    for pair in matched_pairs:
        print(pair)

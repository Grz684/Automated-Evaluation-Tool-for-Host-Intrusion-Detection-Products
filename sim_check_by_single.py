import sqlite3

from transformers import AutoTokenizer, AutoModel
import torch
from scipy.spatial.distance import cosine


def get_sentence_embedding(sentence):
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    embedding = outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy()
    return embedding


def gpu_similarity(text1: str, text2: str) -> float:
    text1_embedding = get_sentence_embedding(text1)
    text2_embedding = get_sentence_embedding(text2)
    return 1 - cosine(text1_embedding, text2_embedding)


def find_best_matches(cn_desc_list, check_item_list, similarity_func, similarity_threshold=0.5):
    matches_from_cn_desc = {}
    matches_from_check_item = {}

    for i, cn_desc in enumerate(cn_desc_list):
        best_match_index = -1
        best_match_score = -1

        for j, check_item in enumerate(check_item_list):
            similarity = similarity_func(cn_desc, check_item)
            print(f"cn_desc:{cn_desc} - check_item:{check_item}: {similarity}")

            if similarity > best_match_score:
                best_match_score = similarity
                best_match_index = j

        if best_match_score >= similarity_threshold:
            matches_from_cn_desc[i] = (best_match_index, best_match_score)

    for j, check_item in enumerate(check_item_list):
        best_match_index = -1
        best_match_score = -1

        for i, cn_desc in enumerate(cn_desc_list):
            similarity = similarity_func(cn_desc, check_item)
            print(f"cn_desc:{cn_desc} - check_item:{check_item}: {similarity}")

            if similarity > best_match_score:
                best_match_score = similarity
                best_match_index = i

        if best_match_score >= similarity_threshold:
            matches_from_check_item[j] = (best_match_index, best_match_score)

    matched_pairs = []
    print(matches_from_cn_desc)
    print(matches_from_check_item)

    for i, (j, score_from_cn_desc) in matches_from_cn_desc.items():
        if j in matches_from_check_item and matches_from_check_item[j] == (i, score_from_cn_desc):
            matched_pairs.append((cn_desc_list[i], check_item_list[j]))

    return matched_pairs


# 示例用法
if __name__ == '__main__':
    # 连接云锁数据库并读取cn_desc列
    db1 = sqlite3.connect('yunsuo_pf_test/yunsuo_cis_baseline_scan_items.db')
    cursor1 = db1.cursor()
    cursor1.execute('SELECT cn_desc FROM items')
    cn_desc_data = cursor1.fetchall()

    # 连接阿里cis数据库并读取check_item列
    db2 = sqlite3.connect('ali_pf_test/ali_cis_baseline_scan_items.db')
    cursor2 = db2.cursor()
    cursor2.execute('SELECT check_item FROM items')
    check_item_data = cursor2.fetchall()

    # 处理结果
    cn_desc_list = [row[0] for row in cn_desc_data]
    check_item_list = [row[0] for row in check_item_data]

    # 关闭数据库连接
    cursor1.close()
    db1.close()
    cursor2.close()
    db2.close()

    # print("yunsuo 列：", cn_desc_list)
    # print("ali 列：", check_item_list)

    # 如果有可用的 GPU，将模型和输入放在 GPU 上
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    # 加载预训练模型和分词器
    model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name).to(device)

    matched_pairs = find_best_matches(cn_desc_list, check_item_list, similarity_func=gpu_similarity,
                                      similarity_threshold=0.5)
    print(matched_pairs)

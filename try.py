import sqlite3
import time

import requests
import json


def simnet_check(text1, text2):
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v2/simnet?charset=&access_token=" + get_access_token()

    payload = json.dumps({
        "text_1": text1,
        "text_2": text2
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    jsonData = json.loads(response.text)

    return jsonData['score']


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": "uL0P7on65vGyw8Za8DLQesly",
              "client_secret": "s0QPmxh0GYK5hc7APIzZmj5NMMo9jKdF"}
    return str(requests.post(url, params=params).json().get("access_token"))


if __name__ == '__main__':
    # 连接第一个数据库并读取cn_desc列
    db1 = sqlite3.connect('yunsuo_pf_test/all_yunsuo_baseline_scan_items.db')
    cursor1 = db1.cursor()
    cursor1.execute('SELECT cn_desc FROM items')
    cn_desc_data = cursor1.fetchall()

    # 连接第二个数据库并读取check_item列
    db2 = sqlite3.connect('ali_pf_test/all_ali_baseline_scan_items.db')
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
    scores = []

    for text in cn_desc_list:
        text1 = text
        text2 = check_item_list[0]
        print(text1)
        print(text2)
        score = simnet_check(text1, text2)
        time.sleep(1)
        scores.append(score)

    print(scores)

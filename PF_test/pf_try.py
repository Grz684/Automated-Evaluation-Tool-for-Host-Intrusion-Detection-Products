import json

# 打开你的json文件
with open('bio_YDService.json', 'r') as f:
    datas = json.load(f)
    for data in datas:
        print(data)
        print(data["I/O"])

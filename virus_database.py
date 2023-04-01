import json
import os
import sqlite3

from ali_pf_test.aliapi import AliApi
from tencent_pf_test.tencentapi import TencentApi
import sqlite3


class VirusDatabase:
    def __init__(self, db_name, accessKeyId, accessKeySecret, uuid):
        self.db_name = db_name
        self.accessKeyId = accessKeyId
        self.accessKeySecret = accessKeySecret
        self.uuid = uuid
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS virus_info
                              (md5 TEXT PRIMARY KEY,
                               ali_id INTEGER,
                               ali_level TEXT,
                               ali_feature TEXT,
                               ali_check INTEGER,
                               tencent_id INTEGER,
                               tencent_level TEXT,
                               tencent_virus_name TEXT,
                               tencent_check INTEGER)''')
            conn.commit()

    def initial_table(self, malwares_folder):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            for file in os.listdir(malwares_folder):
                if os.path.isfile(os.path.join(malwares_folder, file)):
                    md5 = file
                    cursor.execute("INSERT OR IGNORE INTO virus_info (md5) VALUES (?)", (md5,))
                conn.commit()

    def update_ali_data(self, md5, ali_id, ali_level, ali_feature):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''UPDATE virus_info
                              SET ali_id = ?, ali_level = ?, ali_feature = ?, ali_check = ?
                              WHERE md5 = ?''', (ali_id, ali_level, ali_feature, 1, md5))
            conn.commit()

    def update_tencent_data(self, md5, tencent_id, tencent_level, tencent_virus_name):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''UPDATE virus_info
                              SET tencent_id = ?, tencent_level = ?, tencent_virus_name = ?, tencent_check = ?
                              WHERE md5 = ?''', (tencent_id, tencent_level, tencent_virus_name, 1, md5))
            conn.commit()

    def fetch_and_update_tencent_data(self, ip):
        tencentapi = TencentApi(self.accessKeyId, self.accessKeySecret, self.uuid)
        json_str = tencentapi.describe_malware_list(ip)
        data = json.loads(json_str)
        for item in data['MalWareList']:
            id_value = item['Id']
            level_value = item['Level']
            md5_value = item['MD5']
            virus_name_value = item['VirusName']

            # 插入数据
            self.update_tencent_data(md5_value, tencent_id=id_value, tencent_level=level_value,
                                     tencent_virus_name=virus_name_value)

        # 将未经过 update_tencent_data 更新的条目的 tencent_check 值置为 0
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE virus_info SET tencent_check = 0 WHERE tencent_check IS NULL")
            conn.commit()

    def fetch_and_insert_ali_data(self):
        aliapi = AliApi(self.accessKeyId, self.accessKeySecret, self.uuid)
        data = aliapi.describe_susp_events()

        for event in data['SuspEvents']:
            malware_flag = False
            id_value = event['Id']
            level_value = event['Level']
            md5_value = None
            feature_value = None

            for detail in event['Details']:
                if detail["NameDisplay"] in ("恶意文件md5", "文件MD5"):
                    malware_flag = True
                    md5_value = detail["Value"]
                if detail["NameDisplay"] == "样本家族与特征":
                    feature_value = detail["Value"]

            if malware_flag:
                self.update_ali_data(md5_value, ali_id=id_value, ali_level=level_value, ali_feature=feature_value)
        # 将未经过 update_ali_data 更新的条目的 ali_check 值置为 0
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE virus_info SET ali_check = 0 WHERE ali_check IS NULL")
            conn.commit()

    def get_all_ali_ids(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ali_id FROM virus_info WHERE ali_id IS NOT NULL")
            result = cursor.fetchall()
            ali_ids = [row[0] for row in result]
        return ali_ids

    def get_all_tencent_ids(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT tencent_id FROM virus_info WHERE tencent_id IS NOT NULL")
            result = cursor.fetchall()
            tencent_ids = [row[0] for row in result]
        return tencent_ids

    def remove_all_ali_alarms(self):
        # 从安全中心的告警中删除
        aliapi = AliApi(self.accessKeyId, self.accessKeySecret, self.uuid)
        aliapi.handle_security_events(self.get_all_ali_ids())

    def remove_all_tencent_alarms(self):
        # 从安全中心的告警中删除
        tencentapi = TencentApi(self.accessKeyId, self.accessKeySecret, self.uuid)
        tencentapi.modify_risk_events_status(self.get_all_tencent_ids())

    def clear_database(self):
        # 从数据库中删除
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM virus_info")
            conn.commit()


if __name__ == '__main__':
    accessKeyId = "AKIDqbGl9NyRkrwxpfNwEPO8jAQTL5iQG1b2"
    accessKeySecret = "MckjeP0QfhYCg2tX5RiKrCMN4iCZlolY"
    uuid = "ebb72142-e05d-e812-505e-05bf0d7b4907"
    ip = "10.10.21.203"

    virus_db = VirusDatabase('virus_info.db', accessKeyId, accessKeySecret, uuid, )
    virus_db.fetch_and_update_tencent_data(ip)
    # virus_db.fetch_and_update_ali_data()
    # virus_db.remove_all_tencent_data()
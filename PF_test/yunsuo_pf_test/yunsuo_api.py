import configparser
import os
import sqlite3
import traceback
import warnings

import openpyxl
import requests
import json

import yaml
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class YunSuoAPI:
    def __init__(self, hostname, manage_center_ip, token, machine_uuid, baseline_database):
        self.baseline_database = baseline_database
        self.token = token
        self.machine_uuid = machine_uuid
        self.manage_center_ip = manage_center_ip
        self.hostname = hostname

    def create_baseline_scan_task(self, timeout=-1, sub_task_count=1):
        url = f"https://{self.manage_center_ip}/kernelApi/kernelScanSrv/seTaskController/scanTask"
        headers = {'Content-Type': 'application/json'}
        item_ids = self.get_baseline_scan_items()
        items = [{'itemId': item_id, 'op': 'check'} for item_id in item_ids]

        payload = {
            'token': self.token,
            'machineUuids': [self.machine_uuid],
            'operate': 'run',
            'items': items,
            'timeout': timeout,
            'subTaskCount': sub_task_count
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
        response_data = response.json()

        if response.status_code == 200:
            if response_data['code'] == '1':
                return response_data['data']['taskUuid']
            else:
                raise Exception(f"Error {response_data['code']}: {response_data['msg']}")
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")

    # def get_authorize_info(self):
    #     url = f"https://{self.manage_center_ip}/kernelApi/kernelCommonSrv/dictionaryController/getAuthorizeInfo"
    #     headers = {'Content-Type': 'application/json'}
    #     payload = {
    #         'token': self.token
    #     }
    #
    #     response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
    #     response_data = response.json()
    #     print(response_data)
    #
    #     if response.status_code == 200:
    #         if response_data['code'] == '1':
    #             return response_data['data']
    #         else:
    #             raise Exception(f"Error {response_data['code']}: {response_data['msg']}")
    #     else:
    #         raise Exception(f"Error {response.status_code}: {response.text}")

    def get_baseline_scan_items(self):
        # 创建数据库连接和表格
        def create_table_and_connect_db(database_name):
            conn = sqlite3.connect(database_name)
            cursor = conn.cursor()

            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS items (
                        item_id INTEGER PRIMARY KEY,
                        cn_desc TEXT,
                        group_name TEXT,
                        item_intro TEXT,
                        is_passed_check TEXT
                    )
                """)

            conn.commit()
            return conn

        # 将数据插入到数据库
        def insert_data_to_db(conn, item_id, cn_desc, group_name=None, item_intro=None, is_passed_check=None):
            cursor = conn.cursor()
            cursor.execute("""
                    INSERT OR REPLACE INTO items (item_id, cn_desc, group_name, item_intro, is_passed_check) VALUES (?, ?, ?, ?, ?)
                """, (item_id, cn_desc, group_name, item_intro, is_passed_check))
            conn.commit()

        def get_item_id_by_cn_desc(conn, cn_desc):
            cursor = conn.cursor()
            cursor.execute("SELECT item_id FROM items WHERE cn_desc = ?", (cn_desc,))
            result = cursor.fetchone()
            return result[0] if result else None

        # 连接数据库
        if os.path.exists(self.baseline_database):
            os.remove(self.baseline_database)
        conn = create_table_and_connect_db(self.baseline_database)
        # 设置API的URL和请求头
        url = f"https://{self.manage_center_ip}/kernelApi/kernelScanSrv/seBaseItemController/listBaselineItems"
        headers = {"Content-Type": "application/json"}

        # 设置请求参数
        payload = {
            "token": self.token
        }

        # 发送POST请求（忽略证书验证）
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)

        # 检查响应状态码
        if response.status_code == 200:
            # 解析响应内容
            response_data = response.json()

            if response_data["code"] == "1":  # 请求成功
                for item in response_data["data"]:
                    itemId = item["itemId"]
                    cnDesc = item["cnDesc"]
                    osType = item["osType"]
                    ifModifyValue = item["ifModifyValue"]
                    ifRepair = item["ifRepair"]
                    level = item["level"]
                    groupName = item["groupName"]
                    itemDetail = item["itemDetail"]
                    itemIntro = item["itemIntro"]
                    repairSuggestionCn = item["repairSuggestionCn"]

                    # print(
                    #     f"扫描项ID: {itemId} | 扫描项中文描述: {cnDesc} | 扫描项支持的操作系统类型: {osType} | 是否支持修改检查标准值: "
                    #     f"{ifModifyValue} | 是否支持修复: {ifRepair} | 危险等级: {level} | 检查项所属分组: {groupName} | "
                    #     f"检查项检查内容: {itemDetail} | 检查说明: {itemIntro} | 修复建议: {repairSuggestionCn}")

                    insert_data_to_db(conn, itemId, cnDesc, groupName, itemIntro)
            else:
                raise Exception(f"请求失败，错误码：{response_data['code']}, 错误信息：{response_data['msg']}")

        else:
            raise Exception(f"请求失败，HTTP状态码：{response.status_code}")

        # 读取需要的基线扫描项
        baseline_scan_itemNames = YunSuoAPI.read_column_from_xlsx()
        # 查询对应的id
        item_ids = []
        for cn_desc in baseline_scan_itemNames:
            item_id = get_item_id_by_cn_desc(conn, cn_desc)
            # print(f"ID: {item_id} for cn_desc: {cn_desc}")
            if item_id is not None:
                item_ids.append(item_id)
            # else:
            #     print(cn_desc)

        cursor = conn.cursor()
        item_ids_str = ','.join(str(i) for i in item_ids)
        # 构建 SQL 查询以删除不在 item_ids_str 中的项
        delete_sql = f"DELETE FROM items WHERE item_id NOT IN ({item_ids_str})"

        # 执行删除操作
        cursor.execute(delete_sql)

        # 提交更改并关闭连接
        conn.commit()
        cursor.close()
        conn.close()
        return item_ids

    @staticmethod
    def read_column_from_xlsx(skip_header=True):
        current_dir = os.getcwd()  # 获取当前工作目录
        file_path = os.path.join(current_dir, "CIS_V3.0.xlsx")  # 构建文件路径
        sheet_name = "Sheet1"  # 替换为您的工作表名称
        column_index = "A"  # “检查项名”列的索引

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")  # 忽略警告
            workbook = openpyxl.load_workbook(file_path)
        sheet = workbook[sheet_name]
        column_data = []

        for i, cell in enumerate(sheet[column_index]):
            if skip_header and i == 0:
                continue
            column_data.append(cell.value)

        return column_data

    @staticmethod
    def chunks(lst, n):
        """将 lst 分成大小为 n 的块"""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    # def get_machines_by_ip(self, extranet_ip=None, current_page=1, max_results=10):
    #     # 设置API的URL和请求头
    #     url = f"https://{self.manage_center_ip}/kernelApi/kernelCommonSrv/machineController/listMachinesByIp"
    #     headers = {"Content-Type": "application/json"}
    #
    #     # 设置请求参数
    #     payload = {
    #         "token": self.token,
    #         "intranetIp": self.hostname,
    #         "extranetIp": extranet_ip,
    #         "currentPage": current_page,
    #         "maxResults": max_results
    #     }
    #
    #     # 发送POST请求（忽略证书验证）
    #     response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
    #
    #     # 检查响应状态码
    #     if response.status_code == 200:
    #         # 解析响应内容
    #         response_data = response.json()
    #
    #         if response_data["code"] == "1":  # 请求成功
    #             print("服务器列表：")
    #             for machine in response_data["data"]:
    #                 print(
    #                     f"服务器唯一标识: {machine['uuid']}, 服务器名称: {machine['machineName']}, MAC地址: {machine['mac']}, 外网IP: {machine['extranetIp']}, 内网IP: {machine['intranetIp']}, 在线状态: {machine['onlineStatus']}, 操作系统类型: {machine['osType']}, 操作系统名称: {machine['operatingSystem']}, 安装时间戳: {machine['installTimestamp']}, 更新时间戳: {machine['updateTimestamp']}, 软件版本: {machine['softwareVersion']}, 是否卸载: {machine['ifDelete']}, 绑定设备唯一标识: {machine['bindUuid']}, 备注: {machine['remark']}, adv版本: {machine['advVersion']}")
    #         else:
    #             raise Exception(
    #                 f"请求失败，错误码：{response_data['code']}, 错误信息：{response_data['msg']}")
    #
    #     else:
    #         raise Exception(f"请求失败，HTTP状态码：{response.status_code}")

    def get_scan_results(self, task_uuid, weak_pwd=None):
        # 设置API的URL和请求头
        url = f"https://{self.manage_center_ip}/kernelApi/kernelScanSrv/seTaskController/scanResults"
        headers = {"Content-Type": "application/json"}

        # 设置请求参数
        payload = {
            "token": self.token,
            "taskUuid": task_uuid,
            "machineUuid": self.machine_uuid,
            "weakPwd": weak_pwd
        }

        # 发送POST请求（忽略证书验证）
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)

        # 检查响应状态码
        if response.status_code == 200:
            # 解析响应内容
            response_data = response.json()

            if response_data["code"] == "1":  # 请求成功
                return response_data["data"]
            else:
                raise Exception(
                    f"请求失败，错误码：{response_data['code']}, 错误信息：{response_data['msg']}")

        else:
            raise Exception(f"请求失败，HTTP状态码：{response.status_code}")

    def get_task_status(self, task_uuid):
        # 设置API的URL和请求头
        url = f"https://{self.manage_center_ip}/kernelApi/kernelScanSrv/seTaskController/getTaskStatus"
        headers = {"Content-Type": "application/json"}

        # 设置请求参数
        payload = {
            "token": self.token,
            "taskUuid": task_uuid
        }

        # 发送POST请求（忽略证书验证）
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)

        # 检查响应状态码
        if response.status_code == 200:
            # 解析响应内容
            response_data = response.json()

            if response_data["code"] == "1":  # 请求成功
                return response_data["data"]['status']
            else:
                raise Exception(
                    f"请求失败，错误码：{response_data['code']}, 错误信息：{response_data['msg']}")

        else:
            raise Exception(f"请求失败，HTTP状态码：{response.status_code}")

    def list_asset_itemIds(self):
        # 设置API的URL和请求头
        url = f"https://{self.manage_center_ip}/kernelApi/kernelScanSrv/seBaseItemController/listAssetItems"
        headers = {"Content-Type": "application/json"}

        # 设置请求参数
        payload = {
            "token": self.token
        }

        # 发送POST请求（忽略证书验证）
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)

        # 检查响应状态码
        if response.status_code == 200:
            # 解析响应内容
            response_data = response.json()

            if response_data["code"] == "1":  # 请求成功
                assests_scan_items = {}
                for item in response_data["data"]:
                    # print(item['cnDesc'])
                    # print(item['osType'])
                    # itemIds.append(item['itemId'])
                    assests_scan_items[item['itemId']] = item['cnDesc']
                return assests_scan_items
            else:
                raise Exception(
                    f"请求失败，错误码：{response_data['code']}, 错误信息：{response_data['msg']}")

        else:
            raise Exception(f"请求失败，HTTP状态码：{response.status_code}")

    def list_vul_itemIds(self):
        # 设置API的URL和请求头
        url = f"https://{self.manage_center_ip}/kernelApi/kernelScanSrv/seBaseItemController/listVulnerabilityItems"
        headers = {"Content-Type": "application/json"}

        # 设置请求参数
        payload = {
            "token": self.token
        }

        # 发送POST请求（忽略证书验证）
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)

        # 检查响应状态码
        if response.status_code == 200:
            # 解析响应内容
            response_data = response.json()

            if response_data["code"] == "1":  # 请求成功
                itemIds = []
                for item in response_data["data"]:
                    itemIds.append(item['itemId'])
                return itemIds
            else:
                raise Exception(
                    f"请求失败，错误码：{response_data['code']}, 错误信息：{response_data['msg']}")

        else:
            raise Exception(f"请求失败，HTTP状态码：{response.status_code}")

    def create_scan_asset_task(self, timeout=-1, sub_task_count=1):
        # 设置API的URL和请求头
        url = f"https://{self.manage_center_ip}/kernelApi/kernelScanSrv/seTaskController/scanAssetTask"
        headers = {"Content-Type": "application/json"}
        assets_scan_items = self.list_asset_itemIds()
        item_ids = list(assets_scan_items.keys())
        # 设置请求参数
        payload = {
            "token": self.token,
            "machineUuids": [self.machine_uuid],
            "itemIds": item_ids,
            "timeout": timeout,
            "subTaskCount": sub_task_count
        }

        # 发送POST请求（忽略证书验证）
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)

        # 检查响应状态码
        if response.status_code == 200:
            # 解析响应内容
            response_data = response.json()

            if response_data["code"] == "1":  # 请求成功
                task_uuid = response_data["data"]["taskUuid"]
                return task_uuid
            else:
                raise Exception(
                    f"请求失败，错误码：{response_data['code']}, 错误信息：{response_data['msg']}")

        else:
            raise Exception(f"请求失败，HTTP状态码：{response.status_code}")

    def create_scan_vul_task(self, timeout=-1, sub_task_count=1):
        # 设置API的URL和请求头
        url = f"https://{self.manage_center_ip}/kernelApi/kernelScanSrv/seTaskController/scanVulnerabilityTask"
        headers = {"Content-Type": "application/json"}
        item_ids = self.list_vul_itemIds()
        # 设置请求参数
        payload = {
            "token": self.token,
            "machineUuids": [self.machine_uuid],
            "itemIds": item_ids,
            "timeout": timeout,
            "subTaskCount": sub_task_count
        }

        # 发送POST请求（忽略证书验证）
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)

        # 检查响应状态码
        if response.status_code == 200:
            # 解析响应内容
            response_data = response.json()

            if response_data["code"] == "1":  # 请求成功
                task_uuid = response_data["data"]["taskUuid"]
                return task_uuid
            else:
                raise Exception(
                    f"请求失败，错误码：{response_data['code']}, 错误信息：{response_data['msg']}")

        else:
            raise Exception(f"请求失败，HTTP状态码：{response.status_code}")

    def stop_task(self, task_uuid):
        # 设置API的URL和请求头
        url = f"https://{self.manage_center_ip}/kernelApi/kernelScanSrv/seTaskController/stopTask"
        headers = {"Content-Type": "application/json"}

        # 设置请求参数
        payload = {
            "token": self.token,
            "taskUuid": task_uuid
        }

        # 发送POST请求（忽略证书验证）
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)

        # 检查响应状态码
        if response.status_code == 200:
            # 解析响应内容
            response_data = response.json()

            if response_data["code"] == "1":  # 请求成功
                print(response_data)
            else:
                raise Exception(
                    f"请求失败，错误码：{response_data['code']}, 错误信息：{response_data['msg']}")

        else:
            raise Exception(f"请求失败，HTTP状态码：{response.status_code}")

    def update_baseline_scan_result(self, task_uuid):
        scan_results = self.get_scan_results(task_uuid)
        # 连接数据库
        conn = sqlite3.connect(self.baseline_database)
        cursor = conn.cursor()

        for scan_result in scan_results:
            scan_result = json.loads(scan_result)
            if 'compliance' in scan_result.keys():
                # 定义要更新的item_id和is_passed_check的值
                if scan_result['compliance']:
                    is_passed_check = "yes"
                else:
                    is_passed_check = "no"
                item_id = scan_result['base_item_id']

                # 执行更新操作
                cursor.execute(f"UPDATE items SET is_passed_check = ? WHERE item_id = ?",
                               (is_passed_check, item_id))
            else:
                pass

        # 提交更改并关闭连接
        conn.commit()
        conn.close()


if __name__ == "__main__":
    cf = configparser.ConfigParser()
    current_dir = os.getcwd()  # 获取当前工作目录
    parent_dir = os.path.dirname(current_dir)  # 获取上一级目录
    config_path = os.path.join(parent_dir, "config.yaml")  # 构建文件路径
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    agent = config["pfinfo"]["yunsuo_agent"]
    ssh_hostname = str(agent["ssh_hostname"])
    ssh_username = str(agent["ssh_username"])
    ssh_password = str(agent["ssh_password"])
    manage_center_ip = str(agent["manage_center_ip"])
    token = str(agent["token"])
    uuid = str(agent["uuid"])

    # yunsuo_pf_test_assets()

    # yunsuo_pf_test_baseline()

    # yunsuo_vul_test_assets()

    try:
        yunosuo_api = YunSuoAPI(ssh_hostname, manage_center_ip, token, uuid)
        itemIds = yunosuo_api.update_baseline_scan_result("c84e67fac6f04abba53b6d41e6e82151")

    except Exception as e:
        traceback.print_exc()

    # task_uuid = "49097f65993f4bb6a3ef8628bf4bc492"

    # try:
    #     yunosuo_api = YunSuoAPI(ssh_hostname, manage_center_ip, token, uuid)
    #     print("停止扫描任务")
    #     yunosuo_api.stop_task(task_uuid)
    #
    # except Exception as e:
    #     traceback.print_exc()
    #
    # try:
    #     yunsuo_api = YunSuoAPI(ssh_hostname, manage_center_ip, token, uuid)
    #     task_status = yunsuo_api.get_task_status(task_uuid)
    #     print("任务状态：")
    #     print(task_status)
    #
    # except Exception as e:
    #     traceback.print_exc()

    # try:
    #     yunsuo_api = YunSuoAPI(ssh_hostname, manage_center_ip, token, uuid)
    #     assets_scan_items = yunsuo_api.list_asset_itemIds()
    #     print(assets_scan_items)
    #
    # except Exception as e:
    #     traceback.print_exc()

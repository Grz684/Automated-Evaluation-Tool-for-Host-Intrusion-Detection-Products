import configparser
import os
import sqlite3
import warnings

import openpyxl
import requests
import json

import yaml
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class YunSuoAPI:
    def __init__(self, hostname, manage_center_ip, token, machine_uuid):
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

    def get_authorize_info(self):
        url = f"https://{self.manage_center_ip}/kernelApi/kernelCommonSrv/dictionaryController/getAuthorizeInfo"
        headers = {'Content-Type': 'application/json'}
        payload = {
            'token': self.token
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
        response_data = response.json()
        print(response_data)

        if response.status_code == 200:
            if response_data['code'] == '1':
                return response_data['data']
            else:
                raise Exception(f"Error {response_data['code']}: {response_data['msg']}")
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")

    def get_baseline_scan_items(self):
        # 创建数据库连接和表格
        def create_table_and_connect_db(database_name):
            conn = sqlite3.connect(database_name)
            cursor = conn.cursor()

            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS items (
                        id INTEGER PRIMARY KEY,
                        cn_desc TEXT
                    )
                """)

            conn.commit()
            return conn

        # 将数据插入到数据库
        def insert_data_to_db(conn, item_id, cn_desc):
            cursor = conn.cursor()
            cursor.execute("""
                    INSERT OR IGNORE INTO items (id, cn_desc) VALUES (?, ?)
                """, (item_id, cn_desc))
            conn.commit()

        def get_item_id_by_cn_desc(conn, cn_desc):
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM items WHERE cn_desc = ?", (cn_desc,))
            result = cursor.fetchone()
            return result[0] if result else None

        conn = create_table_and_connect_db("all_yunsuo_baseline_scan_items.db")
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
                    item_id = item["itemId"]
                    cn_desc = item["cnDesc"]
                    # print(f"扫描项ID: {item_id}, 中文描述: {cn_desc}")
                    insert_data_to_db(conn, item_id, cn_desc)
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
            item_ids.append(item_id)

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

    def get_machines_by_ip(self, extranet_ip=None, current_page=1, max_results=10):
        # 设置API的URL和请求头
        url = f"https://{self.manage_center_ip}/kernelApi/kernelCommonSrv/machineController/listMachinesByIp"
        headers = {"Content-Type": "application/json"}

        # 设置请求参数
        payload = {
            "token": self.token,
            "intranetIp": self.hostname,
            "extranetIp": extranet_ip,
            "currentPage": current_page,
            "maxResults": max_results
        }

        # 发送POST请求（忽略证书验证）
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)

        # 检查响应状态码
        if response.status_code == 200:
            # 解析响应内容
            response_data = response.json()

            if response_data["code"] == "1":  # 请求成功
                print("服务器列表：")
                for machine in response_data["data"]:
                    print(
                        f"服务器唯一标识: {machine['uuid']}, 服务器名称: {machine['machineName']}, MAC地址: {machine['mac']}, 外网IP: {machine['extranetIp']}, 内网IP: {machine['intranetIp']}, 在线状态: {machine['onlineStatus']}, 操作系统类型: {machine['osType']}, 操作系统名称: {machine['operatingSystem']}, 安装时间戳: {machine['installTimestamp']}, 更新时间戳: {machine['updateTimestamp']}, 软件版本: {machine['softwareVersion']}, 是否卸载: {machine['ifDelete']}, 绑定设备唯一标识: {machine['bindUuid']}, 备注: {machine['remark']}, adv版本: {machine['advVersion']}")
            else:
                raise Exception(
                    f"请求失败，错误码：{response_data['code']}, 错误信息：{response_data['msg']}")

        else:
            raise Exception(f"请求失败，HTTP状态码：{response.status_code}")

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
            print(response_data)

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
                itemIds = []
                for item in response_data["data"]:
                    if item['osType'] == 2:
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
        item_ids = self.list_asset_itemIds()
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


def yunsuo_pf_test_baseline():
    try:
        yunsuo_api = YunSuoAPI(ssh_hostname, manage_center_ip, token, uuid)
        task_uuid = yunsuo_api.create_baseline_scan_task()
        print("任务创建成功，任务UUID：")
        print(task_uuid)
    except Exception as e:
        print("任务创建失败，错误信息：")
        print(e)


def yunsuo_pf_test_assets():
    try:
        yunsuo_api = YunSuoAPI(ssh_hostname, manage_center_ip, token, uuid)
        task_uuid = yunsuo_api.create_scan_asset_task()
        print("任务创建成功，任务UUID：")
        print(task_uuid)
    except Exception as e:
        print("任务创建失败，错误信息：")
        print(e)


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

    # try:
    #     yunosuo_api = YunSuoAPI(ssh_hostname, manage_center_ip, token, uuid)
    #     yunosuo_api.get_machines_by_ip()
    #
    # except Exception as e:
    #     print(e)

    task_uuid = "10f18d3e5e014bb1a58690654017b69b"
    # try:
    #     yunosuo_api = YunSuoAPI(ssh_hostname, manage_center_ip, token, uuid)
    #     scan_results = yunosuo_api.get_scan_results(task_uuid)
    #     print("扫描结果：")
    #     print(scan_results)
    #
    # except Exception as e:
    #     print(e)

    # try:
    #     yunosuo_api = YunSuoAPI(ssh_hostname, manage_center_ip, token, uuid)
    #     print("停止扫描任务")
    #     yunosuo_api.stop_task(task_uuid)
    #
    # except Exception as e:
    #     print(e)

    try:
        yunsuo_api = YunSuoAPI(ssh_hostname, manage_center_ip, token, uuid)
        task_status = yunsuo_api.get_task_status(task_uuid)
        print("任务状态：")
        print(task_status)

    except Exception as e:
        print(e)

    # try:
    #     yunsuo_api = YunSuoAPI(ssh_hostname, manage_center_ip, token, uuid)
    #     itemIds = yunsuo_api.list_asset_itemIds()
    #     print(itemIds)
    #
    # except Exception as e:
    #     print(e)

import time
import traceback
from datetime import datetime

import yaml
from matplotlib import pyplot as plt

from PF_test.pf_util import PFUtil
from ssh import SSH
import os
from tencentapi import TencentApi
import json

# 测试功能id
# 无 0
# web_cms_scan 1
# app_scan 2
# linux_software_scan 3
# win_sys_scan 4
# emg_vul_scan 5
# assets_scan 6
# malware_scan 7
# baseline_scan 8


class TencentPFTest:
    def __init__(self, ssh_hostname, ssh_username, ssh_password, accessKeyId, accessKeySecret, uuid):
        self.ssh_hostname = ssh_hostname
        self.ssh_username = ssh_username
        self.ssh_password = ssh_password
        self.tencent_target_processes = ["YDService", "YDLive", "YDPython", "YDFlame", "YDUtils"]
        self.tencent_test_functions = ["nothing_open", "vul_scan", "assets_scan", "malware_scan", "baseline_scan"]
        self.accessKeyId = accessKeyId
        self.accessKeySecret = accessKeySecret
        self.uuid = uuid
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.commands_file_path = os.path.join(self.base_dir, '..', "pf_test_commands.txt")
        self.tencent_dir = os.path.join(self.base_dir, "tencent")
        self.tencent_translation = {"vul_scan": "漏洞扫描", "assets_scan": "资产扫描", "malware_scan": "病毒扫描",
                            "baseline_scan": "基线扫描"}
        self.baseline_database = os.path.join(self.base_dir, "tencent_cis_baseline_scan_items.db")

        self.pf_util = PFUtil(self.tencent_test_functions, self.tencent_dir, self.tencent_target_processes,
                              self.tencent_translation)
        self.handle_test_data = self.pf_util.handle_test_data
        self.display_test_data = self.pf_util.display_test_data

    def tencent_agent_func_pf_test(self, function_id, test_time=30):
        test_function = self.tencent_test_functions[function_id]
        # 打开ssh连接
        ssh = SSH(self.ssh_hostname, self.ssh_username, self.ssh_password)

        if function_id == 3:
            pass
        else:
            while True:
                start_flag = self.check_current_status(test_function, ssh)
                # print("start_flag: " + str(start_flag))
                if start_flag:
                    break
                # 1秒检查一次
                time.sleep(1)

        # 后台挂起检测任务
        ssh_task = SSH(self.ssh_hostname, self.ssh_username, self.ssh_password)
        ssh_task.exec_command_without_stdout_infile(self.commands_file_path, 9)
        ssh_task.close()

        if function_id == 3:
            while True:
                start_flag = self.check_current_status(test_function, ssh)
                # print("start_flag: " + str(start_flag))
                if start_flag:
                    break
                # 1秒检查一次
                time.sleep(1)

        if function_id == 0:
            time.sleep(test_time)
        else:
            while True:
                stop_flag = not self.check_current_status(test_function, ssh)
                # print("stop_flag: " + str(stop_flag))
                if stop_flag:
                    break
                # 1秒检查一次
                time.sleep(1)

        # 结束检测任务
        ssh_task = SSH(self.ssh_hostname, self.ssh_username, self.ssh_password)
        ssh_task.exec_command_infile(self.commands_file_path, 5)
        ssh_task.close()
        # 获取检测结果
        time.sleep(5)
        ini_test_result = ssh.exec_command_infile(self.commands_file_path, 7)
        ini_test_result = ini_test_result.decode().strip()

        os.makedirs(self.tencent_dir, exist_ok=True)
        file_name = os.path.join(self.tencent_dir, f"init_{test_function}.txt")
        f = open(file_name, mode='w', encoding='utf-8')
        f.write(ini_test_result)
        ssh.close()
        f.close()

    def check_current_status(self, test_function, ssh):
        # 得到正在运行的process
        process_paths = ssh.exec_command_infile(self.commands_file_path, 10)
        process_paths = process_paths.decode().strip()
        process_paths = process_paths.split("\n")
        running_processes = []
        for process_path in process_paths:
            path = process_path.split("/")
            running_processes.append(path[-1])

        # 查看是否进入预设状态
        # target_process_flag标志此轮数据中是否包含function对应进程，如包含则置为True
        target_process_flag = False

        # 静默状态
        if test_function == self.tencent_test_functions[0]:
            target_process_flag = True

        # 漏洞扫描
        if test_function == self.tencent_test_functions[1]:
            if self.tencent_target_processes[2] in running_processes:
                target_process_flag = True

        # 资产采集
        if test_function == self.tencent_test_functions[2]:
            if self.tencent_target_processes[3] in running_processes:
                target_process_flag = True

        # 恶意软件扫描
        if test_function == self.tencent_test_functions[3]:
            if self.tencent_target_processes[4] in running_processes:
                target_process_flag = True

        # 基线扫描
        if test_function == self.tencent_test_functions[4]:
            if self.tencent_target_processes[2] in running_processes:
                target_process_flag = True

        activ_status = False

        if target_process_flag:
            activ_status = True

        return activ_status

    def tencent_pf_test_all_funcs(self):
        self.tencent_pf_test_nothing()
        self.tencent_pf_test_vul()
        self.tencent_pf_test_assets()
        self.tencent_pf_test_virus()
        self.tencent_pf_test_baseline()

    def tencent_pf_test_nothing(self):
        self.tencent_agent_func_pf_test(0)
        self.handle_test_data(0)
        self.display_test_data(0)

    def tencent_pf_test_vul(self):
        tencentapi = TencentApi(self.accessKeyId, self.accessKeySecret, self.uuid)
        # tencentapi.scan_vul()
        # self.tencent_agent_func_pf_test(1)
        self.handle_test_data(1)
        self.display_test_data(1)
        # 获取相应功能的扫描结果
        result_file_path = os.path.join(self.tencent_dir, 'vul_scan_result.md')
        self.get_vul_scan_result(result_file_path)

    def tencent_pf_test_assets(self):
        tencentapi = TencentApi(self.accessKeyId, self.accessKeySecret, self.uuid)
        # tencentapi.scan_asset()
        # self.tencent_agent_func_pf_test(2)
        self.handle_test_data(2)
        self.display_test_data(2)
        # 获取相应功能的扫描结果
        result_file_path = os.path.join(self.tencent_dir, 'assets_scan_result.md')
        self.get_assets_scan_result(result_file_path)

    def tencent_pf_test_virus(self):
        tencentapi = TencentApi(self.accessKeyId, self.accessKeySecret, self.uuid)
        # tencentapi.scan_malware()
        # self.tencent_agent_func_pf_test(3)
        self.handle_test_data(3)
        self.display_test_data(3)

    def tencent_pf_test_baseline(self):
        tencentapi = TencentApi(self.accessKeyId, self.accessKeySecret, self.uuid)
        # tencentapi.start_baseline_detect()
        # self.tencent_agent_func_pf_test(4)
        self.handle_test_data(4)
        self.display_test_data(4)
        # 获取相应功能的扫描结果
        result_file_path = os.path.join(self.tencent_dir, 'baseline_scan_result.md')
        self.get_baseline_scan_result(result_file_path)

    def get_vul_scan_result(self, file_path):
        tencentapi = TencentApi(self.accessKeyId, self.accessKeySecret, self.uuid)
        try:
            vul_info = tencentapi.describe_vul_list()

            with open(file_path, 'a', encoding='utf-8') as f:
                f.write("### 漏洞扫描结果：" + '\n\n')
                f.write(f"共扫描到{len(vul_info)}个漏洞，漏洞cve编号分别为：" + '\n\n')
                for vul_id in vul_info.keys():
                    f.write(f'{vul_id} ({vul_info[vul_id]})' + '\n\n')

        except Exception as e:
            traceback.print_exc()

    def get_assets_scan_result(self, file_path):
        tencentapi = TencentApi(self.accessKeyId, self.accessKeySecret, self.uuid)

        try:
            assets_info = tencentapi.describe_asset_host_total_count()
            # 把assets_info的value全部加起来
            total_assets = 0
            for value in assets_info.values():
                total_assets += value

            with open(file_path, 'a', encoding='utf-8') as f:
                f.write("### 资产扫描结果：" + '\n\n')
                f.write(f"共扫描到{total_assets}项资产，资产分类情况为：" + '\n\n')
                # 循环classified_scan_results的键值对
                for asset_id in assets_info.keys():
                    f.write(f'{asset_id}: {assets_info[asset_id]}' + '\n\n')

        except Exception as e:
            traceback.print_exc()

    def get_baseline_scan_result(self, file_path):
        tencentapi = TencentApi(self.accessKeyId, self.accessKeySecret, self.uuid)
        try:

            tencentapi.describe_baseline_item_info()
            tencentapi.describe_baseline_item_detect_list()
            query = "SELECT item_name, is_passed_check FROM items"
            rows, markdown_table = PFUtil.turn_database_to_table(self.baseline_database, query)

            with open(file_path, "a", encoding='utf-8') as f:
                f.write("### 基线检测结果" + '\n\n')
                f.write(f"共检测CIS基线{rows}项，基线检测结果为：" + '\n\n')
                f.write(markdown_table)

        except Exception as e:
            traceback.print_exc()


if __name__ == '__main__':
    with open("../../config.yaml", "r") as f:
        config = yaml.safe_load(f)
    agent = config["pfinfo"]["tencent_agent"]
    ssh_hostname = str(agent["ssh_hostname"])
    ssh_username = str(agent["ssh_username"])
    ssh_password = str(agent["ssh_password"])
    accessKeyId = str(agent["accessKeyId"])
    accessKeySecret = str(agent["accessKeySecret"])
    uuid = str(agent["uuid"])
    tencent = TencentPFTest(ssh_hostname, ssh_username, ssh_password, accessKeyId, accessKeySecret, uuid)
    tencent.tencent_pf_test_virus()

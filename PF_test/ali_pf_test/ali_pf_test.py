import time

import yaml

from PF_test.pf_util import PFUtil
from ssh import SSH
import os
from PF_test.ali_pf_test.aliapi import AliApi
import json

# 目标进程id
# AliDetect 0
# AliYunDunUpdate 1
# AliYunDun 2
# AliYunDunMonitor 3
# AliSecGuard 4
# AliHips 5
# AliNet 6
# AliSecureCheckAdvanced 7

class AliPFTest:
    def __init__(self, ssh_hostname, ssh_username, ssh_password, accessKeyId, accessKeySecret, uuid):
        self.ssh_hostname = ssh_hostname
        self.ssh_username = ssh_username
        self.ssh_password = ssh_password
        self.ali_target_processes = ["AliDetect", "AliYunDunUpdate", "AliYunDun", "AliYunDunMonitor", "AliSecGuard",
                                     "AliHips", "AliNet", "AliSecureCheckAdvanced"]
        self.ali_test_functions = ["nothing_open", "self_protection", "Web_backdoor_connection_defense",
                                   "Network_defense", "anti_virus",
                                   "vul_scan", "assets_scan", "virus_scan", "baseline_scan"]
        self.ali_static_funcs_api_types = ["alisecguard", "webshell_cloud_breaking", "alinet", "auto_breaking"]
        self.accessKeyId = accessKeyId
        self.accessKeySecret = accessKeySecret
        self.uuid = uuid
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.command_file_path = os.path.join(self.script_dir, '../..', 'pf_test_commands.txt')
        self.ali_dir_path = os.path.join(self.script_dir, 'ali')

        self.ali_translation = {"vul_scan": "漏洞扫描", "assets_scan": "资产扫描", "virus_scan": "病毒扫描",
                                    "baseline_scan": "基线扫描"}
        self.baseline_database = os.path.join(self.script_dir, "ali_cis_baseline_scan_items.db")

        self.pf_util = PFUtil(self.ali_test_functions, self.ali_dir_path, self.ali_target_processes,
                              self.ali_translation)
        self.handle_test_data = self.pf_util.handle_test_data
        self.display_test_data = self.pf_util.display_test_data


    def ali_agent_func_pf_test(self, function_id, test_time=30):
        test_function = self.ali_test_functions[function_id]
        # 打开ssh连接
        ssh = SSH(self.ssh_hostname, self.ssh_username, self.ssh_password)

        while True:
            start_flag = self.check_current_status(test_function, ssh)
            # print("start_flag: " + str(start_flag))
            if start_flag:
                break
            # 1秒检查一次
            time.sleep(1)

        # 后台挂起检测任务
        print(f"{test_function}场景已建立，开始采集性能数据.....")
        ssh_task = SSH(self.ssh_hostname, self.ssh_username, self.ssh_password)
        ssh_task.exec_command_without_stdout_infile(self.command_file_path, 4)
        ssh_task.close()

        if function_id >= 5:
            # 扫描情况
            while True:
                stop_flag = not self.check_current_status(test_function, ssh)
                # print("stop_flag: " + str(stop_flag))
                if stop_flag:
                    break
                # 1秒检查一次
                time.sleep(1)
        else:
            time.sleep(test_time)

        # 结束检测任务
        print(f"本场景已结束，正在停止采集性能数据.....")
        ssh_task = SSH(self.ssh_hostname, self.ssh_username, self.ssh_password)
        ssh_task.exec_command_infile(self.command_file_path, 5)
        ssh_task.close()
        # 获取检测结果
        time.sleep(5)
        ini_test_result = ssh.exec_command_infile(self.command_file_path, 7)
        ini_test_result = ini_test_result.decode().strip()

        os.makedirs(self.ali_dir_path, exist_ok=True)
        file_name = os.path.join(self.ali_dir_path, "init_" + test_function + ".txt")
        f = open(file_name, mode='w', encoding='utf-8')
        f.write(ini_test_result)
        ssh.close()
        f.close()

    def check_current_status(self, test_function, ssh):
        # 得到正在运行的process
        process_paths = ssh.exec_command_infile(self.command_file_path, 6)
        process_paths = process_paths.decode().strip()
        process_paths = process_paths.split("\n")
        running_processes = []
        for process_path in process_paths:
            path = process_path.split("/")
            running_processes.append(path[-1])

        # 查看是否进入预设状态
        # no_loader_flag标志此轮数据中是否包含AliSecureCheckAdvanced进程，如包含则置为False
        no_loader_flag = True
        # target_process_flag标志此轮数据中是否包含function对应进程，如包含则置为True
        target_process_flag = False

        if test_function == self.ali_test_functions[0]:
            target_process_flag = True

        # 自保护
        elif test_function == self.ali_test_functions[1]:
            if self.ali_target_processes[-1] in running_processes:
                no_loader_flag = False
            if self.ali_target_processes[4] in running_processes:
                target_process_flag = True

        # 网站后门连接防御
        elif test_function == self.ali_test_functions[2]:
            if self.ali_target_processes[-1] in running_processes:
                no_loader_flag = False
            if self.ali_target_processes[5] in running_processes:
                target_process_flag = True

        # 网络防御
        elif test_function == self.ali_test_functions[3]:
            if self.ali_target_processes[-1] in running_processes:
                no_loader_flag = False
            if self.ali_target_processes[6] in running_processes:
                target_process_flag = True

        # 防病毒
        elif test_function == self.ali_test_functions[4]:
            if self.ali_target_processes[-1] in running_processes:
                no_loader_flag = False
            if self.ali_target_processes[5] in running_processes:
                target_process_flag = True

        # 漏洞扫描
        elif test_function == self.ali_test_functions[5]:
            if self.ali_target_processes[-1] in running_processes:
                target_process_flag = True

        # 资产采集
        elif test_function == self.ali_test_functions[6]:
            if self.ali_target_processes[-1] in running_processes:
                target_process_flag = True

        # 病毒扫描
        elif test_function == self.ali_test_functions[7]:
            if self.ali_target_processes[-1] in running_processes:
                target_process_flag = True

        # 基线扫描
        elif test_function == self.ali_test_functions[8]:
            if self.ali_target_processes[-1] in running_processes:
                target_process_flag = True

        activ_status = False

        if no_loader_flag and target_process_flag:
            activ_status = True

        return activ_status

    def ali_pf_test_static_funcs(self, test_time):
        self.ali_agent_func_pf_test(0, test_time)
        self.handle_test_data(0)
        self.display_test_data(0)
        aliapi = AliApi(self.accessKeyId, self.accessKeySecret, self.uuid)

        for i in range(4):
            aliapi.operate_suspicious_target_config(self.ali_static_funcs_api_types[i], 'add')
            time.sleep(90)

            self.ali_agent_func_pf_test(i + 1, test_time)
            self.handle_test_data(i + 1)
            self.display_test_data(i + 1)

            aliapi.operate_suspicious_target_config(self.ali_static_funcs_api_types[i], 'del')

    def ali_pf_test_all_funcs(self):
        self.ali_pf_test_nothing()
        print(" ")
        self.ali_pf_test_vul()
        print(" ")
        self.ali_pf_test_assets()
        print(" ")
        self.ali_pf_test_virus()
        print(" ")
        self.ali_pf_test_baseline()

    def ali_pf_test_nothing(self):
        self.ali_agent_func_pf_test(0)
        self.handle_test_data(0)
        self.display_test_data(0)

    def ali_pf_test_vul(self):
        aliapi = AliApi(self.accessKeyId, self.accessKeySecret, self.uuid)
        # aliapi.vul_scan()
        # self.ali_agent_func_pf_test(5)
        self.handle_test_data(5)
        self.display_test_data(5)

    def ali_pf_test_assets(self):
        aliapi = AliApi(self.accessKeyId, self.accessKeySecret, self.uuid)
        # aliapi.assets_scan()
        # self.ali_agent_func_pf_test(6)
        self.handle_test_data(6)
        self.display_test_data(6)

    def ali_pf_test_virus(self):
        aliapi = AliApi(self.accessKeyId, self.accessKeySecret, self.uuid)
        # aliapi.start_virus_scan_task()
        # self.ali_agent_func_pf_test(7)
        self.handle_test_data(7)
        self.display_test_data(7)

    def ali_pf_test_baseline(self):
        aliapi = AliApi(self.accessKeyId, self.accessKeySecret, self.uuid)
        # aliapi.baseline_scan()
        # self.ali_agent_func_pf_test(8)
        self.handle_test_data(8)
        self.display_test_data(8)

if __name__ == '__main__':
    with open("../../config.yaml", "r") as f:
        config = yaml.safe_load(f)
    agent = config["pfinfo"]["aliyun_agent"]
    ssh_hostname = str(agent["ssh_hostname"])
    ssh_username = str(agent["ssh_username"])
    ssh_password = str(agent["ssh_password"])
    accessKeyId = str(agent["accessKeyId"])
    accessKeySecret = str(agent["accessKeySecret"])
    uuid = str(agent["uuid"])
    ali = AliPFTest(ssh_hostname, ssh_username, ssh_password, accessKeyId, accessKeySecret, uuid)
    ali.ali_pf_test_assets()

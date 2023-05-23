import time

import yaml

from PF_test.pf_util import PFUtil
from ssh import SSH
import os
import json

class HisecPFTest:
    def __init__(self, ssh_hostname, ssh_username, ssh_password):
        self.ssh_hostname = ssh_hostname
        self.ssh_username = ssh_username
        self.ssh_password = ssh_password
        self.hisec_target_processes = ["wsssr_defence_service", "wsssr_defence_daemon"]
        self.hisec_test_functions = ["nothing_open", "vul_scan", "assets_scan", "virus_scan", "baseline_scan"]

        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.command_file_path = os.path.join(self.script_dir, '..', "pf_test_commands.txt")
        self.hisec_dir_path = os.path.join(self.script_dir, 'hisec')

        self.hisec_translation = {"nothing_open": "静默状态", "vul_scan": "漏洞扫描", "assets_scan": "资产扫描", "virus_scan": "病毒扫描",
                                  "baseline_scan": "基线扫描"}

        self.pf_util = PFUtil(self.hisec_test_functions, self.hisec_dir_path, self.hisec_target_processes,
                              self.hisec_translation)
        self.handle_test_data = self.pf_util.handle_test_data
        self.display_test_data = self.pf_util.display_test_data

    def hisec_agent_func_pf_test(self, function_id):
        test_function = self.hisec_test_functions[function_id]
        # 打开ssh连接
        ssh = SSH(self.ssh_hostname, self.ssh_username, self.ssh_password)

        self.wait_for_start()

        # 后台挂起检测任务
        print(f"{test_function}场景已建立，开始采集性能数据.....")
        ssh_task = SSH(self.ssh_hostname, self.ssh_username, self.ssh_password)
        ssh_task.exec_command_without_stdout_infile(self.command_file_path, 11)
        ssh_task.close()

        self.wait_for_end()

        # 结束检测任务
        print(f"本场景已结束，正在停止采集性能数据.....")
        ssh_task = SSH(self.ssh_hostname, self.ssh_username, self.ssh_password)
        ssh_task.exec_command_infile(self.command_file_path, 5)
        ssh_task.close()
        # 获取检测结果
        time.sleep(5)
        ini_test_result = ssh.exec_command_infile(self.command_file_path, 7)
        ini_test_result = ini_test_result.decode().strip()

        os.makedirs(self.hisec_dir_path, exist_ok=True)
        file_name = os.path.join(self.hisec_dir_path, "init_" + test_function + ".txt")
        f = open(file_name, mode='w', encoding='utf-8')
        f.write(ini_test_result)
        ssh.close()
        f.close()

    def wait_for_start(self):
        input("请按回车键开始采集性能数据...")

    def wait_for_end(self):
        input("请按回车键停止采集性能数据...")

    def hisec_pf_test_all_funcs(self):
        self.hisec_pf_test_nothing()
        print(" ")
        self.hisec_pf_test_vul()
        print(" ")
        self.hisec_pf_test_assets()
        print(" ")
        self.hisec_pf_test_virus()
        print(" ")
        self.hisec_pf_test_baseline()

    def hisec_pf_test_nothing(self):
        self.hisec_agent_func_pf_test(0)
        self.handle_test_data(0)
        self.display_test_data(0)

    def hisec_pf_test_vul(self):
        # hisecapi = hisecApi(self.accessKeyId, self.accessKeySecret, self.uuid)
        # hisecapi.vul_scan()
        self.hisec_agent_func_pf_test(1)
        self.handle_test_data(1)
        self.display_test_data(1)

    def hisec_pf_test_assets(self):
        # hisecapi = hisecApi(self.accessKeyId, self.accessKeySecret, self.uuid)
        # hisecapi.assets_scan()
        # self.hisec_agent_func_pf_test(2)
        self.handle_test_data(2)
        self.display_test_data(2)

    def hisec_pf_test_virus(self):
        # hisecapi = hisecApi(self.accessKeyId, self.accessKeySecret, self.uuid)
        # hisecapi.start_virus_scan_task()
        self.hisec_agent_func_pf_test(3)
        self.handle_test_data(3)
        self.display_test_data(3)

    def hisec_pf_test_baseline(self):
        # hisecapi = hisecApi(self.accessKeyId, self.accessKeySecret, self.uuid)
        # hisecapi.baseline_scan()
        self.hisec_agent_func_pf_test(4)
        self.handle_test_data(4)
        self.display_test_data(4)


if __name__ == '__main__':
    with open("../../config.yaml", "r") as f:
        config = yaml.safe_load(f)
    agent = config["pfinfo"]["hisec_agent"]
    ssh_hostname = str(agent["ssh_hostname"])
    ssh_username = str(agent["ssh_username"])
    ssh_password = str(agent["ssh_password"])
    # accessKeyId = str(agent["accessKeyId"])
    # accessKeySecret = str(agent["accessKeySecret"])
    # uuid = str(agent["uuid"])
    hisec = HisecPFTest(ssh_hostname, ssh_username, ssh_password)
    hisec.hisec_pf_test_assets()

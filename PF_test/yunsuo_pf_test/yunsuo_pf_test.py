import time
import traceback
from datetime import datetime
import yaml
from matplotlib import pyplot as plt

from PF_test.pf_util import PFUtil
from ssh import SSH
import json
import os
from yunsuo_api import YunSuoAPI


class YunSuoPFTest:
    def __init__(self, ssh_hostname, ssh_username, ssh_password, uuid, manage_center_ip, token):
        self.yunsuo_target_processes = ["wsssr_defence_service", "wsssr_defence_daemon", "lbaselinescan", "icsfilesec"]
        self.yunsuo_test_functions = ["nothing_open", "vul_scan", "assets_scan", "malware_scan", "baseline_scan",
                                      "os_solid", "intrusion_detection"]
        self.yunsuo_translation = {"nothing_open": "无功能开启", "vul_scan": "漏洞扫描", "assets_scan": "资产扫描", "malware_scan": "病毒扫描",
                            "baseline_scan": "基线扫描"}
        self.ssh_hostname = ssh_hostname
        self.ssh_username = ssh_username
        self.ssh_password = ssh_password
        self.uuid = uuid
        self.manage_center_ip = manage_center_ip
        self.token = token

        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.commands_file_path = os.path.join(self.base_dir, '..', "pf_test_commands.txt")
        self.yunsuo_dir = os.path.join(self.base_dir, "yunsuo")
        self.baseline_database = os.path.join(self.base_dir, "yunsuo_cis_baseline_scan_items.db")

        self.pf_util = PFUtil(self.yunsuo_test_functions, self.yunsuo_dir, self.yunsuo_target_processes,
                              self.yunsuo_translation, self.ssh_hostname, self.ssh_username, self.ssh_password, "wss", "yunsuo")
        self.handle_test_data = self.pf_util.handle_test_data
        self.display_test_data = self.pf_util.display_test_data_new

    def yunsuo_agent_func_pf_test(self, function_id):
        test_function = self.yunsuo_test_functions[function_id]
        # 打开ssh连接
        ssh = SSH(self.ssh_hostname, self.ssh_username, self.ssh_password)

        while True:
            task_status = self.check_current_status(test_function, ssh)
            # print("start_flag: " + str(start_flag))
            if task_status:
                break
            # 1秒检查一次
            time.sleep(1)

        ssh.close()
        # 后台挂起检测任务
        print(f"{test_function}场景已建立，开始采集性能数据.....")
        yunsuo.pf_util.start_test(function_id)
        time.sleep(300)
        yunsuo.pf_util.end_test(function_id)

    def check_current_status(self, test_function, ssh):
        # 得到正在运行的process
        process_paths = ssh.exec_command_infile(self.commands_file_path, 12)
        process_paths = process_paths.decode().strip()
        process_paths = process_paths.split("\n")
        running_processes = []
        for process_path in process_paths:
            path = process_path.split("/")
            running_processes.append(path[-1])

        print(running_processes)

        # 查看是否进入预设状态
        # target_process_flag标志此轮数据中是否包含function对应进程，如包含则置为True
        target_process_flag = False

        # 静默状态
        if test_function in [self.yunsuo_test_functions[0], self.yunsuo_test_functions[5],
                             self.yunsuo_test_functions[6]]:
            target_process_flag = True

        # 漏洞、基线、资产扫描
        if test_function in [self.yunsuo_test_functions[1], self.yunsuo_test_functions[2],
                             self.yunsuo_test_functions[4]]:
            if self.yunsuo_target_processes[2] in running_processes:
                target_process_flag = True

        # 病毒扫描
        if test_function == self.yunsuo_test_functions[3]:
            if self.yunsuo_target_processes[3] in running_processes:
                target_process_flag = True

        activ_status = False

        if target_process_flag:
            activ_status = True

        return activ_status

    def yunsuo_pf_test_all_funcs(self):
        self.yunsuo_pf_test_nothing()
        self.yunsuo_pf_test_vul()
        self.yunsuo_pf_test_assets()
        self.yunsuo_pf_test_virus()
        self.yunsuo_pf_test_baseline()

    def yunsuo_pf_test_nothing(self):
        self.yunsuo_agent_func_pf_test(0)
        yunsuo.pf_util.handle_pidstat_data(0)
        yunsuo.pf_util.handle_bio_data(0)
        yunsuo.pf_util.handle_btcp_data(0)
        yunsuo.display_test_data(0)

    def yunsuo_pf_test_vul(self):
        yunsuo_api = YunSuoAPI(self.ssh_hostname, self.manage_center_ip, self.token, self.uuid, self.baseline_database)
        try:
            # task_uuid = yunsuo_api.create_scan_vul_task()
            # print("任务创建成功，任务UUID：")
            # print(task_uuid)
            # self.yunsuo_agent_func_pf_test(1, task_uuid)
            task_uuid = "49097f65993f4bb6a3ef8628bf4bc492"
            self.handle_test_data(1)
            self.display_test_data(1)
            # 获取相应功能的扫描结果
            file_path = os.path.join(self.yunsuo_dir, 'vul_scan_result.md')
            self.get_vul_scan_result(task_uuid, file_path)
        except Exception as e:
            print("错误信息：")
            traceback.print_exc()

    def yunsuo_pf_test_assets(self):
        yunsuo_api = YunSuoAPI(self.ssh_hostname, self.manage_center_ip, self.token, self.uuid, self.baseline_database)
        try:
            # task_uuid = yunsuo_api.create_scan_asset_task()
            # print("任务创建成功，任务UUID：")
            # print(task_uuid)
            # self.yunsuo_agent_func_pf_test(2, task_uuid)
            task_uuid = "bc3b24ce2b8344b1b95a58cc564a7f8d"
            self.handle_test_data(2)
            self.display_test_data(2)
            # 获取相应功能的扫描结果
            file_path = os.path.join(self.yunsuo_dir, 'assets_scan_result.md')
            self.get_assets_scan_result(task_uuid, file_path)
        except Exception as e:
            print("错误信息：")
            traceback.print_exc()

    def yunsuo_pf_test_virus(self):
        self.yunsuo_agent_func_pf_test(3)
        yunsuo.pf_util.handle_pidstat_data(3)
        yunsuo.pf_util.handle_bio_data(3)
        yunsuo.pf_util.handle_btcp_data(3)
        yunsuo.display_test_data(3)

    def yunsuo_pf_test_baseline(self):
        yunsuo_api = YunSuoAPI(self.ssh_hostname, self.manage_center_ip, self.token, self.uuid, self.baseline_database)
        try:
            task_uuid = yunsuo_api.create_baseline_scan_task()
            print("任务创建成功，任务UUID：")
            print(task_uuid)
            self.yunsuo_agent_func_pf_test(4)
            yunsuo.pf_util.handle_pidstat_data(4)
            yunsuo.pf_util.handle_bio_data(4)
            yunsuo.pf_util.handle_btcp_data(4)
            yunsuo.display_test_data(4)
            # 获取相应功能的扫描结果
            # file_path = os.path.join(self.yunsuo_dir, 'baseline_scan_result.md')
            # self.get_baseline_scan_result(task_uuid, file_path)
        except Exception as e:
            print("错误信息：")
            traceback.print_exc()

    def get_vul_scan_result(self, task_uuid, file_path):
        yunsuo_api = YunSuoAPI(self.ssh_hostname, self.manage_center_ip, self.token, self.uuid, self.baseline_database)
        try:
            scan_results = yunsuo_api.get_scan_results(task_uuid)

            with open(file_path, 'a', encoding='utf-8') as f:
                f.write("### 漏洞扫描结果：" + '\n\n')
                f.write(f"共扫描到{len(scan_results)}个漏洞，漏洞cve编号分别为：" + '\n\n')
                for scan_result in scan_results:
                    scan_result = json.loads(scan_result)
                    f.write(f'{scan_result["cveid"]} ({json.loads(scan_result["cnDesc"])["cn"]})' + '\n\n')

        except Exception as e:
            traceback.print_exc()

    def get_assets_scan_result(self, task_uuid, file_path):
        yunsuo_api = YunSuoAPI(self.ssh_hostname, self.manage_center_ip, self.token, self.uuid, self.baseline_database)
        try:
            scan_results = yunsuo_api.get_scan_results(task_uuid)

            assets_scan_items = yunsuo_api.list_asset_itemIds()
            # 初始化一个字典，字典的键为assets_scan_items的键，值初始为0
            assets_scan_items_dict = dict.fromkeys(assets_scan_items, 0)

            for scan_result in scan_results:
                scan_result = json.loads(scan_result)
                if "asset_code" in scan_result.keys():
                    assets_scan_items_dict[scan_result["asset_code"]] += 1
                else:
                    # print(scan_result)
                    pass

            # 将asset_code替换成中文描述
            classified_scan_results = {}
            for key in assets_scan_items_dict.keys():
                classified_scan_results[assets_scan_items[key]] = assets_scan_items_dict[key]

            # 把classified_scan_results的value全部加起来
            total_assets = 0
            for value in classified_scan_results.values():
                total_assets += value

            with open(file_path, 'a', encoding='utf-8') as f:
                f.write("### 资产扫描结果：" + '\n\n')
                f.write(f"共扫描到{total_assets}项资产，资产分类情况为：" + '\n\n')
                # 循环classified_scan_results的键值对
                for key, value in classified_scan_results.items():

                    f.write(f'{key}: {value}' + '\n\n')

        except Exception as e:
            traceback.print_exc()

    def get_baseline_scan_result(self, task_uuid, file_path):
        yunsuo_api = YunSuoAPI(self.ssh_hostname, self.manage_center_ip, self.token, self.uuid, self.baseline_database)
        try:

            yunsuo_api.update_baseline_scan_result(task_uuid)
            query = "SELECT cn_desc, is_passed_check FROM items"
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
    agent = config["pfinfo"]["yunsuo_agent"]
    ssh_hostname = str(agent["ssh_hostname"])
    ssh_username = str(agent["ssh_username"])
    ssh_password = str(agent["ssh_password"])
    manage_center_ip = str(agent["manage_center_ip"])
    token = str(agent["token"])
    uuid = str(agent["uuid"])
    yunsuo = YunSuoPFTest(ssh_hostname, ssh_username, ssh_password, uuid, manage_center_ip, token)
    yunsuo.yunsuo_pf_test_virus()
    # 测试漏洞扫描：yunsuo.display_test_data(1, "49097f65993f4bb6a3ef8628bf4bc492")
    # 测试资产扫描：yunsuo.display_test_data(2, "bc3b24ce2b8344b1b95a58cc564a7f8d")
    # 基线扫描"f58a6a11d4eb469c9a01db0d7af7849e"
    # yunsuo.yunsuo_pf_test_baseline()
    # yunsuo.yunsuo_pf_test_vul()
    # yunsuo.yunsuo_pf_test_assets()

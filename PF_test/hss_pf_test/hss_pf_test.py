import time
import yaml

from PF_test.pf_util import PFUtil
from ssh import SSH
import os


class HssPFTest:
    def __init__(self, ssh_hostname, ssh_username, ssh_password):
        self.ssh_hostname = ssh_hostname
        self.ssh_username = ssh_username
        self.ssh_password = ssh_password

        self.hss_target_processes = ["hostwatch", "hostguard", "python"]
        self.hss_test_functions = ["nothing_open", "baseline_scan"]

        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.command_file_path = os.path.join(self.script_dir, '..', 'pf_test_commands.txt')
        self.hss_dir_path = os.path.join(self.script_dir, 'hss')

        self.hss_translation = {"nothing_open": "无功能开启", "baseline_scan": "基线扫描"}

        self.pf_util = PFUtil(self.hss_test_functions, self.hss_dir_path, self.hss_target_processes,
                              self.hss_translation, self.ssh_hostname, self.ssh_username, self.ssh_password, "hostguard",
                              "hss")
        self.handle_test_data = self.pf_util.handle_test_data
        self.display_test_data = self.pf_util.display_test_data_new

    def hss_agent_func_pf_test(self, function_id, test_time=30):
        test_function = self.hss_test_functions[function_id]
        ssh = SSH(self.ssh_hostname, self.ssh_username, self.ssh_password)

        while True:
            start_flag = self.check_current_status(test_function, ssh)
            # print("start_flag: " + str(start_flag))
            if start_flag:
                break
            # 1秒检查一次
            time.sleep(1)

        ssh.close()

        # 后台挂起检测任务
        print(f"{test_function}场景已建立，开始采集性能数据.....")
        hss.pf_util.start_test(function_id)
        time.sleep(300)
        hss.pf_util.end_test(function_id)

    def check_current_status(self, test_function, ssh):
        # 得到正在运行的process
        process_paths = ssh.exec_command_infile(self.command_file_path, 13)
        process_paths = process_paths.decode().strip()
        process_paths = process_paths.split("\n")
        running_processes = []
        print(process_paths)
        for process_path in process_paths:
            running_processes.append(process_path)

        # target_process_flag标志此轮数据中是否包含function对应进程，如包含则置为True
        target_process_flag = False

        if test_function == self.hss_test_functions[0]:
            target_process_flag = True

        # 基线扫描
        if test_function == self.hss_test_functions[1]:
            if "/usr/local/hostguard/data/benchmark/module/SSH/playbook.py" in running_processes:
                target_process_flag = True

        activ_status = False

        if target_process_flag:
            activ_status = True

        return activ_status

    def hss_pf_test_all_funcs(self):
        self.hss_pf_test_nothing()
        print(" ")
        self.hss_pf_test_baseline()

    def hss_pf_test_nothing(self):
        self.hss_agent_func_pf_test(0)
        hss.pf_util.handle_pidstat_data(0)
        hss.pf_util.handle_bio_data(0)
        hss.pf_util.handle_btcp_data(0)
        hss.display_test_data(0)

    def hss_pf_test_baseline(self):
        self.hss_agent_func_pf_test(1)
        hss.pf_util.handle_pidstat_data(1)
        hss.pf_util.handle_bio_data(1)
        hss.pf_util.handle_btcp_data(1)
        hss.display_test_data(1)


if __name__ == '__main__':
    with open("../../config.yaml", "r") as f:
        config = yaml.safe_load(f)
    agent = config["pfinfo"]["hss_agent"]
    ssh_hostname = str(agent["ssh_hostname"])
    ssh_username = str(agent["ssh_username"])
    ssh_password = str(agent["ssh_password"])

    hss = HssPFTest(ssh_hostname, ssh_username, ssh_password)
    hss.hss_pf_test_baseline()

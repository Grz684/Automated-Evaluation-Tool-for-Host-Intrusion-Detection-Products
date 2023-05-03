import time
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
                                   "Network_defense",
                                   "anti_virus", "vul_scan", "assets_scan", "virus_scan", "baseline_scan"]
        self.ali_static_funcs_api_types = ["alisecguard", "webshell_cloud_breaking", "alinet", "auto_breaking"]
        self.accessKeyId = accessKeyId
        self.accessKeySecret = accessKeySecret
        self.uuid = uuid
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.command_file_path = os.path.join(self.script_dir, '../..', 'pf_test_commands.txt')
        self.ali_dir_path = os.path.join(self.script_dir, 'ali')


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

    def handle_test_data(self, function_id):
        print("性能数据统计处理中.....")
        test_function = self.ali_test_functions[function_id]
        init_file_name = os.path.join(self.ali_dir_path, "init_" + test_function + ".txt")
        dirname = os.path.join(self.ali_dir_path, test_function)
        os.makedirs(dirname, exist_ok=True)
        result_files = dict()
        for index in range(len(self.ali_target_processes)):
            file_name = os.path.join(dirname, self.ali_target_processes[index])
            f = open(file_name, mode='w', encoding='utf-8')
            # f.write("//handle time: " + time.ctime() + "\n")
            result_files[self.ali_target_processes[index]] = f

        init_f = open(init_file_name, mode='r', encoding='utf-8')
        line = init_f.readline()
        json_start_line = json.loads(line)

        start_time = json_start_line['time']
        start_time = "2001-4-4 " + start_time
        start_timeArray = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        start_time_stamp = int(time.mktime(start_timeArray))
        stop_time_stamp = 0

        while line:
            json_line = json.loads(line)
            command = json_line['command']
            command_parts = command.split('/')
            command_process = command_parts[-1]

            if command_process in result_files.keys():
                result_files[command_process].write(line)

            stop_time = "2001-4-4 " + json_line['time']
            stop_timeArray = time.strptime(stop_time, "%Y-%m-%d %H:%M:%S")
            stop_time_stamp = int(time.mktime(stop_timeArray))

            line = init_f.readline()

        time_f = open(os.path.join(dirname, "time"), mode='w', encoding='utf-8')
        test_time = str(stop_time_stamp - start_time_stamp)
        time_f.write(test_time)
        # 关闭文件句柄
        for index in range(len(self.ali_target_processes)):
            result_files[self.ali_target_processes[index]].close()
        init_f.close()
        time_f.close()

    def display_test_data(self, function_id):
        test_function = self.ali_test_functions[function_id]
        dirname = os.path.join(self.ali_dir_path, test_function)

        time_f = open(os.path.join(dirname, "time"), mode='r', encoding='utf-8')
        test_time = int(time_f.readline())
        time_f.close()

        print("在 {} 场景下，各进程组件性能测试结果如下（场景持续时间{}s）：".format(test_function, test_time))

        func_average_cpu = 0.0
        func_average_mem = 0.0
        func_average_disk_read = 0.0
        func_average_disk_write = 0.0

        for index in range(len(self.ali_target_processes)):
            total_cpu = 0.0
            total_mem = 0.0
            total_disk_read = 0.0
            total_disk_write = 0.0

            file_name = os.path.join(dirname, self.ali_target_processes[index])
            f = open(file_name, mode='r', encoding='utf-8')
            line = f.readline()
            while line:
                json_line = json.loads(line)
                total_cpu += float(json_line['cpu'])
                total_mem += float(json_line['mem'])
                total_disk_read += float(json_line['kB_rd'])
                total_disk_write += float(json_line['kB_wr'])

                line = f.readline()

            f.close()
            average_cpu = total_cpu / test_time
            average_mem = total_mem / test_time
            average_disk_rd = total_disk_read / test_time
            average_disk_wr = total_disk_write / test_time

            func_average_cpu += average_cpu
            func_average_mem += average_mem
            func_average_disk_read += average_disk_rd
            func_average_disk_write += average_disk_wr
            print(
                "进程{}:\naverage_cpu: {:.2f} %, average_mem: {:.2f} %, average_disk_rd: {:.2f} kb/s, average_disk_write: {:.2f} kb/s"
                .format(self.ali_target_processes[index], average_cpu, average_mem, average_disk_rd, average_disk_wr))

        print(
            "总资源占用:\naverage_cpu: {:.2f} %, average_mem: {:.2f} %, average_disk_rd: {:.2f} kb/s, average_disk_write: {:.2f} kb/s"
            .format(func_average_cpu, func_average_mem, func_average_disk_read, func_average_disk_write))

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
        aliapi.vul_scan()
        self.ali_agent_func_pf_test(5)
        self.handle_test_data(5)
        self.display_test_data(5)

    def ali_pf_test_assets(self):
        aliapi = AliApi(self.accessKeyId, self.accessKeySecret, self.uuid)
        aliapi.assets_scan()
        self.ali_agent_func_pf_test(6)
        self.handle_test_data(6)
        self.display_test_data(6)

    def ali_pf_test_virus(self):
        aliapi = AliApi(self.accessKeyId, self.accessKeySecret, self.uuid)
        aliapi.start_virus_scan_task()
        self.ali_agent_func_pf_test(7)
        self.handle_test_data(7)
        self.display_test_data(7)

    def ali_pf_test_baseline(self):
        aliapi = AliApi(self.accessKeyId, self.accessKeySecret, self.uuid)
        aliapi.baseline_scan()
        self.ali_agent_func_pf_test(8)
        self.handle_test_data(8)
        self.display_test_data(8)

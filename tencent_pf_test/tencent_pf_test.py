import time
from ssh import SSH
import os
from tencent_pf_test.tencentapi import TencentApi
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

    def handle_test_data(self, function_id):
        test_function = self.tencent_test_functions[function_id]
        init_file_name = os.path.join(self.tencent_dir, f"init_{test_function}.txt")
        dirname = os.path.join(self.tencent_dir, test_function)
        os.makedirs(dirname, exist_ok=True)
        result_files = dict()
        for index in range(len(self.tencent_target_processes)):
            file_name = os.path.join(dirname, self.tencent_target_processes[index])
            f = open(file_name, mode='w', encoding='utf-8')
            # f.write("//handle time: " + time.ctime() + "\n")
            result_files[self.tencent_target_processes[index]] = f

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

        time_f = open(os.path.join(dirname, 'time'), mode='w', encoding='utf-8')
        test_time = str(stop_time_stamp - start_time_stamp)
        time_f.write(test_time)
        # 关闭文件句柄
        for index in range(len(self.tencent_target_processes)):
            result_files[self.tencent_target_processes[index]].close()
        init_f.close()
        time_f.close()

    def display_test_data(self, function_id):
        test_function = self.tencent_test_functions[function_id]
        dirname = os.path.join(self.tencent_dir, test_function)

        time_f = open(os.path.join(dirname, 'time'), mode='r', encoding='utf-8')
        test_time = int(time_f.readline())
        time_f.close()

        print("在仅开启 {} 功能的情况下，各进程组件性能测试结果如下（测试时间{}s）：".format(test_function, test_time))

        func_average_cpu = 0.0
        func_average_mem = 0.0
        func_average_disk_read = 0.0
        func_average_disk_write = 0.0

        for index in range(len(self.tencent_target_processes)):
            total_cpu = 0.0
            total_mem = 0.0
            total_disk_read = 0.0
            total_disk_write = 0.0

            file_name = os.path.join(dirname, self.tencent_target_processes[index])
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
                .format(self.tencent_target_processes[index], average_cpu, average_mem, average_disk_rd,
                        average_disk_wr))

        print(
            "总资源占用:\naverage_cpu: {:.2f} %, average_mem: {:.2f} %, average_disk_rd: {:.2f} kb/s, average_disk_write: {:.2f} kb/s"
            .format(func_average_cpu, func_average_mem, func_average_disk_read, func_average_disk_write))

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
        tencentapi.scan_vul()
        self.tencent_agent_func_pf_test(1)
        self.handle_test_data(1)
        self.display_test_data(1)

    def tencent_pf_test_assets(self):
        tencentapi = TencentApi(self.accessKeyId, self.accessKeySecret, self.uuid)
        tencentapi.scan_asset()
        self.tencent_agent_func_pf_test(2)
        self.handle_test_data(2)
        self.display_test_data(2)

    def tencent_pf_test_virus(self):
        tencentapi = TencentApi(self.accessKeyId, self.accessKeySecret, self.uuid)
        tencentapi.scan_malware()
        self.tencent_agent_func_pf_test(3)
        self.handle_test_data(3)
        self.display_test_data(3)

    def tencent_pf_test_baseline(self):
        tencentapi = TencentApi(self.accessKeyId, self.accessKeySecret, self.uuid)
        tencentapi.start_baseline_detect()
        self.tencent_agent_func_pf_test(4)
        self.handle_test_data(4)
        self.display_test_data(4)

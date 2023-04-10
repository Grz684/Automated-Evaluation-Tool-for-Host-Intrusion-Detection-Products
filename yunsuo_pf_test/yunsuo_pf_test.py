import time
from datetime import datetime

import yaml
from matplotlib import pyplot as plt

from ssh import SSH
import json
import os

from yunsuo_api import YunSuoAPI


class YunSuoPFTest:
    def __init__(self, ssh_hostname, ssh_username, ssh_password, uuid, manage_center_ip, token):
        self.yunsuo_target_processes = ["wsssr_defence_service", "wsssr_defence_daemon", "lbaselinescan", "icsfilesec"]
        self.yunsuo_test_functions = ["nothing_open", "vul_scan", "assets_scan", "malware_scan", "baseline_scan",
                                      "os_solid", "intrusion_detection"]
        self.ssh_hostname = ssh_hostname
        self.ssh_username = ssh_username
        self.ssh_password = ssh_password
        self.uuid = uuid
        self.manage_center_ip = manage_center_ip
        self.token = token

        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.commands_file_path = os.path.join(self.base_dir, '..', "pf_test_commands.txt")
        self.yunsuo_dir = os.path.join(self.base_dir, "yunsuo")

    def yunsuo_agent_func_pf_test(self, function_id, task_uuid, test_time=30):
        test_function = self.yunsuo_test_functions[function_id]
        # 打开ssh连接
        ssh = SSH(self.ssh_hostname, self.ssh_username, self.ssh_password)

        while True:
            task_status = self.check_current_status(task_uuid)
            # print("start_flag: " + str(start_flag))
            if task_status == 1:
                break
            # 1秒检查一次
            time.sleep(1)

        # 后台挂起检测任务
        ssh_task = SSH(self.ssh_hostname, self.ssh_username, self.ssh_password)
        ssh_task.exec_command_without_stdout_infile(self.commands_file_path, 11)
        ssh_task.close()

        if function_id in [0, 5, 6]:
            time.sleep(test_time)
        else:
            while True:
                task_status = self.check_current_status(task_uuid)
                # print("stop_flag: " + str(stop_flag))
                if task_status == 2:
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

        os.makedirs(self.yunsuo_dir, exist_ok=True)
        file_name = os.path.join(self.yunsuo_dir, f"init_{test_function}.txt")
        f = open(file_name, mode='w', encoding='utf-8')
        f.write(ini_test_result)
        ssh.close()
        f.close()

    def check_current_status(self, task_uuid):
        yunsuo_api = YunSuoAPI(self.ssh_hostname, self.manage_center_ip, self.token, self.uuid)
        try:
            task_status = yunsuo_api.get_task_status(task_uuid)
            print("任务状态：")
            print(task_status)
            return task_status

        except Exception as e:
            print(e)

    def handle_test_data(self, function_id):
        test_function = self.yunsuo_test_functions[function_id]
        init_file_name = os.path.join(self.yunsuo_dir, f"init_{test_function}.txt")
        dirname = os.path.join(self.yunsuo_dir, test_function)
        os.makedirs(dirname, exist_ok=True)
        result_files = dict()
        for index in range(len(self.yunsuo_target_processes)):
            file_name = os.path.join(dirname, self.yunsuo_target_processes[index])
            f = open(file_name, mode='w', encoding='utf-8')
            # f.write("//handle time: " + time.ctime() + "\n")
            result_files[self.yunsuo_target_processes[index]] = f

        init_f = open(init_file_name, mode='r', encoding='utf-8')
        line = init_f.readline().strip()
        json_start_line = json.loads(line)

        start_time = json_start_line['time']
        start_timeArray = time.strptime("2001-4-4 " + start_time, "%Y-%m-%d %H:%M:%S")
        start_time_stamp = int(time.mktime(start_timeArray))
        stop_time = ""
        stop_time_stamp = 0

        while line:
            json_line = json.loads(line)
            command = json_line['command']
            command_parts = command.split('/')
            command_process = command_parts[-1]
            if command_process in result_files.keys():
                result_files[command_process].write(line)

            stop_time = json_line['time']
            stop_timeArray = time.strptime("2001-4-4 " + stop_time, "%Y-%m-%d %H:%M:%S")
            stop_time_stamp = int(time.mktime(stop_timeArray))

            line = init_f.readline().strip()

        time_f = open(os.path.join(dirname, 'time'), mode='w', encoding='utf-8')
        test_time = str(stop_time_stamp - start_time_stamp)
        time_f.write(test_time + '\n')
        time_f.write(start_time + '\n')
        time_f.write(stop_time + '\n')
        # 关闭文件句柄
        for index in range(len(self.yunsuo_target_processes)):
            result_files[self.yunsuo_target_processes[index]].close()
        init_f.close()
        time_f.close()

    @staticmethod
    def is_file_empty(file_path):
        try:
            # 获取文件大小
            file_size = os.path.getsize(file_path)

            # 判断文件大小是否大于0
            if file_size > 0:
                return False
            else:
                return True
        except FileNotFoundError:
            print(f"The file '{file_path}' does not exist.")
            return False

    def display_test_data(self, function_id):
        test_function = self.yunsuo_test_functions[function_id]
        dirname = os.path.join(self.yunsuo_dir, test_function)

        with open(os.path.join(dirname, 'time'), mode='r', encoding='utf-8') as time_f:
            test_time = int(time_f.readline().strip())
            start_time = time_f.readline().strip()
            time_format = '%H:%M:%S'
            start_time_object = datetime.strptime(start_time, time_format)

        print("在仅开启 {} 功能的情况下，各进程组件性能测试结果如下（测试时间{}s）：".format(test_function, test_time))

        func_average_cpu = 0.0
        func_average_mem = 0.0
        fig, axs = plt.subplots(2, 2, figsize=(20, 8))
        processes_pf_list = []

        for index in range(len(self.yunsuo_target_processes)):

            process_cpu_total = 0.0
            process_mem_total = 0.0
            process_cpu_usage = []
            process_mem_usage = []
            process_time = []

            file_name = os.path.join(dirname, self.yunsuo_target_processes[index])
            if YunSuoPFTest.is_file_empty(file_name):
                continue
            f = open(file_name, mode='r', encoding='utf-8')
            line = f.readline().strip()

            while line:
                json_line = json.loads(line)

                time_object = datetime.strptime(json_line['time'], time_format)
                time_zeroed = (time_object - start_time_object).total_seconds()
                process_time.append(time_zeroed)

                process_cpu_total += float(json_line['cpu'])
                process_mem_total += float(json_line['mem'])
                process_cpu_usage.append(float(json_line['cpu']))
                process_mem_usage.append(float(json_line['mem']))

                line = f.readline().strip()

            f.close()

            # 将当前进程的性能数据放入列表中
            processes_pf_list.append(zip(process_time, process_cpu_usage, process_mem_usage))

            process_average_cpu = process_cpu_total / test_time
            process_average_mem = process_mem_total / test_time

            func_average_cpu += process_average_cpu
            func_average_mem += process_average_mem

            print("进程{}:\naverage_cpu: {:.2f} %, average_mem: {:.2f} %"
                  .format(self.yunsuo_target_processes[index], process_average_cpu, process_average_mem))

        # 绘制单个进程消耗的曲线
        func_cpu_data = {x: 0 for x in range(test_time + 1)}
        func_mem_data = {x: 0 for x in range(test_time + 1)}
        for index in range(len(processes_pf_list)):
            process_cpu_data = {x: 0 for x in range(test_time + 1)}
            process_mem_data = {x: 0 for x in range(test_time + 1)}
            for time, cpu, mem in processes_pf_list[index]:
                func_cpu_data[time] += cpu
                func_mem_data[time] += mem
                process_cpu_data[time] += cpu
                process_mem_data[time] += mem

            axs[0, 0].plot(list(process_cpu_data.keys()), list(process_cpu_data.values()),
                           label=self.yunsuo_target_processes[index])
            axs[0, 1].plot(list(process_mem_data.keys()), list(process_mem_data.values()),
                           label=self.yunsuo_target_processes[index])

        # 绘制总资源消耗的曲线
        axs[1, 0].plot(list(func_cpu_data.keys()), list(func_cpu_data.values()),
                       label='total')
        axs[1, 1].plot(list(func_mem_data.keys()), list(func_mem_data.values()),
                       label='total')

        # 设置子图标题、轴标签和图例
        axs[0, 0].set_xlabel('time (seconds)')
        axs[0, 1].set_xlabel('time (seconds)')
        axs[0, 0].set_ylabel('cpu (%)')
        axs[0, 1].set_ylabel('memory (%)')
        axs[0, 0].set_title('process CPU usage')
        axs[0, 1].set_title('process MEM usage')
        axs[0, 0].legend()
        axs[0, 1].legend()

        axs[1, 0].set_xlabel('time (seconds)')
        axs[1, 0].set_ylabel('cpu (%)')
        axs[1, 1].set_xlabel('time (seconds)')
        axs[1, 1].set_ylabel('memory (%)')
        axs[1, 0].set_title('total CPU usage')
        axs[1, 1].set_title('total MEM usage')

        plt.tight_layout()
        plt.savefig('sine_wave.png', dpi=300)
        print(
            "总资源占用:\naverage_cpu: {:.2f} %, average_mem: {:.2f} %"
            .format(func_average_cpu, func_average_mem))

    def yunsuo_pf_test_all_funcs(self):
        self.yunsuo_pf_test_nothing()
        self.yunsuo_pf_test_vul()
        self.yunsuo_pf_test_assets()
        self.yunsuo_pf_test_virus()
        self.yunsuo_pf_test_baseline()

    def yunsuo_pf_test_nothing(self):
        self.yunsuo_agent_func_pf_test(0)
        self.handle_test_data(0)
        self.display_test_data(0)

    def yunsuo_pf_test_vul(self):
        self.yunsuo_agent_func_pf_test(1)
        self.handle_test_data(1)
        self.display_test_data(1)

    def yunsuo_pf_test_assets(self):
        yunsuo_api = YunSuoAPI(self.ssh_hostname, self.manage_center_ip, self.token, self.uuid)
        try:
            task_uuid = yunsuo_api.create_scan_asset_task()
            print("任务创建成功，任务UUID：")
            print(task_uuid)
            self.yunsuo_agent_func_pf_test(2, task_uuid)
            self.handle_test_data(2)
            self.display_test_data(2)
        except Exception as e:
            print("错误信息：")
            print(e)

    def yunsuo_pf_test_virus(self):
        self.yunsuo_agent_func_pf_test(3)
        self.handle_test_data(3)
        self.display_test_data(3)

    def yunsuo_pf_test_baseline(self):
        self.yunsuo_agent_func_pf_test(4)
        self.handle_test_data(4)
        self.display_test_data(4)


if __name__ == '__main__':
    with open("../config.yaml", "r") as f:
        config = yaml.safe_load(f)
    agent = config["pfinfo"]["yunsuo_agent"]
    ssh_hostname = str(agent["ssh_hostname"])
    ssh_username = str(agent["ssh_username"])
    ssh_password = str(agent["ssh_password"])
    manage_center_ip = str(agent["manage_center_ip"])
    token = str(agent["token"])
    uuid = str(agent["uuid"])
    yunsuo = YunSuoPFTest(ssh_hostname, ssh_username, ssh_password, uuid, manage_center_ip, token)
    yunsuo.display_test_data(2)

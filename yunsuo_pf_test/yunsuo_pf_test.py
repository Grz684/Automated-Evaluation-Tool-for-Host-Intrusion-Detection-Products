import time
from ssh import SSH
import json
import os

from yunsuo_pf_test.yunsuo_api import YunSuoAPI


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
        for index in range(len(self.yunsuo_target_processes)):
            result_files[self.yunsuo_target_processes[index]].close()
        init_f.close()
        time_f.close()

    def display_test_data(self, function_id):
        test_function = self.yunsuo_test_functions[function_id]
        dirname = os.path.join(self.yunsuo_dir, test_function)

        time_f = open(os.path.join(dirname, 'time'), mode='r', encoding='utf-8')
        test_time = int(time_f.readline())
        time_f.close()

        print("在仅开启 {} 功能的情况下，各进程组件性能测试结果如下（测试时间{}s）：".format(test_function, test_time))

        func_average_cpu = 0.0
        func_average_mem = 0.0
        func_average_disk_read = 0.0
        func_average_disk_write = 0.0

        for index in range(len(self.yunsuo_target_processes)):
            total_cpu = 0.0
            total_mem = 0.0
            total_disk_read = 0.0
            total_disk_write = 0.0

            file_name = os.path.join(dirname, self.yunsuo_target_processes[index])
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

            print("进程{}:\naverage_cpu: {:.2f}, average_mem: {:.2f}, average_disk_rd: {:.2f}, average_disk_write: {:.2f}"
                  .format(self.yunsuo_target_processes[index], average_cpu, average_mem, average_disk_rd,
                          average_disk_wr))

        print(
            "总资源占用:\naverage_cpu: {:.2f} %, average_mem: {:.2f} %, average_disk_rd: {:.2f} kb/s, average_disk_write: {:.2f} kb/s"
            .format(func_average_cpu, func_average_mem, func_average_disk_read, func_average_disk_write))

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

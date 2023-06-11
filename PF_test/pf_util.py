import os
import json
import sqlite3
import time
from datetime import datetime
import re

import numpy as np
from ssh import SSH
from matplotlib import pyplot as plt


class PFUtil:
    def __init__(self, test_functions, dir, target_processes, translation, ssh_hostname, ssh_username,
                 ssh_password, agent_name, agent_type):
        self.test_functions = test_functions
        self.dir = dir
        self.target_processes = target_processes
        self.translation = translation
        self.ssh_hostname = ssh_hostname
        self.ssh_username = ssh_username
        self.ssh_password = ssh_password
        self.agent_name = agent_name
        self.agent_type = agent_type

    def start_test(self, function_id):
        """
        阿里云性能测试，使用pidstat测试vcpu，mem，disk读写速率
        :param function_id: 测试的功能序号
        :param test_time: 测试时间
        :return:
        """
        # 测试cpu，内存，读写
        ssh_pidstat = SSH(self.ssh_hostname, self.ssh_username, self.ssh_password)
        # 执行pidstat命令，并将输出重定向到文件中
        if self.agent_type == "ali":
            pidstat_command = "pidstat -urd -l -h 3 10000 | grep ae[g]is | awk '{printf \"{" \
                              "\\\"cpu\\\":\\\"%s\\\"," \
                              "\\\"VSZ\\\":\\\"%s\\\", \\\"RSS\\\":\\\"%s\\\"," \
                              "\\\"kB_rd\\\":\\\"%s\\\", \\\"kB_wr\\\":\\\"%s\\\"," \
                              "\\\"command\\\":\\\"%s\\\"," \
                              "\\\"time\\\":\\\"%s\\\"}\\n\",$8,$12,$13,$15,$16,$19,$1}' 1> /tmp/test.txt " \
                              "2>/dev/null"
        elif self.agent_type == "tencent":
            pidstat_command = "pidstat -urd -l -h 3 10000 | grep Y[D] | awk '{printf \"{" \
                              "\\\"cpu\\\":\\\"%s\\\"," \
                              "\\\"VSZ\\\":\\\"%s\\\", \\\"RSS\\\":\\\"%s\\\"," \
                              "\\\"kB_rd\\\":\\\"%s\\\", \\\"kB_wr\\\":\\\"%s\\\"," \
                              "\\\"command\\\":\\\"%s\\\"," \
                              "\\\"time\\\":\\\"%s\\\"}\\n\",$8,$12,$13,$15,$16,$19,$1}' 1> /tmp/test.txt " \
                              "2>/dev/null"
        elif self.agent_type == "yunsuo":
            pidstat_command = "pidstat -urd -l -h 3 10000 | grep w[s]s | awk '{printf \"{" \
                              "\\\"cpu\\\":\\\"%s\\\"," \
                              "\\\"VSZ\\\":\\\"%s\\\", \\\"RSS\\\":\\\"%s\\\"," \
                              "\\\"kB_rd\\\":\\\"%s\\\", \\\"kB_wr\\\":\\\"%s\\\"," \
                              "\\\"command\\\":\\\"%s\\\"," \
                              "\\\"time\\\":\\\"%s\\\"}\\n\",$8,$12,$13,$15,$16,$19,$1}' 1> /tmp/test.txt " \
                              "2>/dev/null"
        elif self.agent_type == "hss":
            pidstat_command = "pidstat -urd -l -h 3 10000 | grep host[g]uard | awk '{printf \"{" \
                              "\\\"cpu\\\":\\\"%s\\\"," \
                              "\\\"VSZ\\\":\\\"%s\\\", \\\"RSS\\\":\\\"%s\\\"," \
                              "\\\"kB_rd\\\":\\\"%s\\\", \\\"kB_wr\\\":\\\"%s\\\"," \
                              "\\\"command\\\":\\\"%s\\\"," \
                              "\\\"time\\\":\\\"%s\\\"}\\n\",$8,$12,$13,$15,$16,$19,$1}' 1> /tmp/test.txt " \
                              "2>/dev/null"

        print("-" * 50)
        print(f"Executing pidstat performance test for {self.agent_type}......")
        print("-" * 50)
        session_name = f'{self.agent_type}-pidstat={function_id}'
        ssh_pidstat.exec_command_without_stdout(f"tmux new-session -d -s {session_name}")
        ssh_pidstat.exec_command_without_stdout(f"tmux attach -t {session_name}")
        ssh_pidstat.exec_command_without_stdout(pidstat_command)
        ssh_pidstat.close()

        # 开始测试bcc指标
        ssh_bcc = SSH(self.ssh_hostname, self.ssh_username, self.ssh_password)
        print("-" * 50)
        print(f"Executing bcc performance test for {self.agent_type}......")
        print("-" * 50)
        # 选择bcc_command
        if self.agent_type == "ali":
            bcc_command = "bash /home/ubuntu/bcc-AliAll.sh"
        elif self.agent_type == "tencent":
            bcc_command = "bash /home/ubuntu/bcc-TencentAll.sh"
        elif self.agent_type == "yunsuo":
            bcc_command = "bash /home/ubuntu/bcc-YunSuoAll.sh"
        elif self.agent_type == "hss":
            bcc_command = "bash /home/ubuntu/bcc-HssAll.sh"

        session_name = f'{self.agent_type}-bcc={function_id}'
        ssh_bcc.exec_command_without_stdout(f"tmux new-session -d -s {session_name}")
        ssh_bcc.exec_command_without_stdout(f'tmux send-keys -t {session_name} "{bcc_command}" Enter')
        ssh_bcc.close()

    def end_test(self, function_id):
        # 结束检测任务
        session_name = f'{self.agent_type}-pidstat={function_id}'
        ssh_end = SSH(self.ssh_hostname, self.ssh_username, self.ssh_password)
        ssh_end.exec_command("killall pidstat")
        ssh_end.exec_command(f"tmux kill-session -t {session_name}")

        # 获取检测结果
        time.sleep(5)
        test_result = ssh_end.exec_command("cat /tmp/test.txt").strip()
        ssh_end.exec_command("rm /tmp/test.txt")
        test_function = self.test_functions[function_id]
        file_name = os.path.join(self.dir, "init_" + test_function + ".txt")
        f = open(file_name, mode='w', encoding='utf-8')
        f.write(test_result)
        f.close()

        # 获取数据
        bio_procs = self.target_processes
        for bio_proc in bio_procs:
            time.sleep(5)
            test_bio_result = ssh_end.exec_command(f"cat /tmp/bio-{bio_proc}.txt").strip()
            ssh_end.exec_command(f"rm /tmp/bio-{bio_proc}.txt")
            test_function = self.test_functions[function_id]
            file_name = os.path.join(self.dir, "init_bio_{}_{}.txt".format(test_function, bio_proc))
            with open(file_name, 'w', encoding='utf-8') as f:
                if test_bio_result:
                    f.write(test_bio_result)
                    f.close()

        tcp_procs = self.target_processes
        for tcp_proc in tcp_procs:
            time.sleep(5)
            test_btcp_result = ssh_end.exec_command(f"cat /tmp/btcp-{tcp_proc}.txt").strip()
            ssh_end.exec_command(f"rm /tmp/btcp-{tcp_proc}.txt")
            test_function = self.test_functions[function_id]
            file_name = os.path.join(self.dir, "init_btcp_{}_{}.txt".format(test_function, tcp_proc))
            with open(file_name, 'w', encoding='utf-8') as f:
                if test_btcp_result:
                    f.write(test_btcp_result)
                    f.close()

        ssh_end.close()

    def handle_pidstat_data(self, function_id):
        """
        处理测试数据
        :param function_id: 测试功能序号
        :return:
        """
        test_function = self.test_functions[function_id]
        init_file_name = os.path.join(self.dir, 'init_{}'.format(test_function)+".txt")

        dirname = os.path.join(self.dir, test_function)
        os.makedirs(dirname, exist_ok=True)

        result_files = dict()
        output_data = {process: [] for process in self.target_processes}
        for process in self.target_processes:
            output_filename = os.path.join(dirname, f"pidstat_{process}.json")
            f = open(output_filename, mode='w', encoding='utf-8')
            result_files[process] = f

        with open(init_file_name, mode='r', encoding='utf-8') as init_file:
            for line in init_file:
                json_line = json.loads(line)
                command = json_line['command'].split('/')[-1]
                if command in result_files.keys():
                    time_info = json_line['time']
                    cpu_info = json_line['cpu']
                    vsz_info = '{:.2f}'.format(int(json_line['VSZ']) / (1024 * 1024))
                    rss_info = '{:.2f}'.format(int(json_line['RSS']) / (1024 * 1024))
                    disk_rd = json_line['kB_rd']
                    disk_wr = json_line['kB_wr']

                    # 组织数据为字典形式
                    data = {
                        "Time": time_info,
                        "Command": command,
                        "CPU": cpu_info,
                        "VSZ": vsz_info,
                        "RSS": rss_info,
                        "Disk_rd": disk_rd,
                        "Disk_wr": disk_wr,
                    }
                    output_data[command].append(data)

        # 分别写入json
        for process in self.target_processes:
            json.dump(output_data[process], result_files[process], indent=4)
            result_files[process].write('\n')

        # 关闭文件句柄
        for process in self.target_processes:
            result_files[process].close()

    def handle_bio_data(self, function_id):
        # 改一下
        process_names = self.target_processes
        test_function = self.test_functions[function_id]

        for process_name in process_names:
            filename = os.path.join(self.dir, "init_bio_{}_{}.txt".format(test_function, process_name))

            with open(filename, "r") as file:
                lines = file.readlines()

            groups = []
            group = []
            for line in lines:
                line = line.strip()
                if line.startswith("Tracing") or line.startswith("Detaching"):
                    continue
                if re.match(r"\d{2}:\d{2}:\d{2}", line):
                    if group:
                        groups.append(group)
                        group = []
                if line:
                    group.append(line)

            if group:
                groups.append(group)

            output_data = []

            for group in groups:
                time_info = group[0].split()[0]  # 提取时间信息
                pid_info = group[-1].split()[0]  # 提取pid
                command_info = group[-1].split()[1]  # 提取命令
                io_info = group[-1].split()[6]  # 提取IO
                if io_info == 'I/O':
                    io_info = "0"

                # 组织数据为字典形式
                data = {
                    "Time": time_info,
                    "PID": pid_info,
                    "Command": command_info,
                    "I/O": io_info
                }
                output_data.append(data)

            # print(output_data)
            # 构建输出文件路径
            output_dir = os.path.join(self.dir, test_function)
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, "bio_{}.json".format(process_name))

            # 将数据写入 JSON 文件
            with open(output_file, "w") as outfile:
                json.dump(output_data, outfile, indent=4)

    def handle_btcp_data(self, function_id):
        process_names = self.target_processes
        test_function = self.test_functions[function_id]

        for process_name in process_names:
            filename = os.path.join(self.dir, "init_btcp_{}_{}.txt".format(test_function, process_name))

            with open(filename, "r") as file:
                lines = file.readlines()

            groups = []
            group = []
            for line in lines:
                line = line.strip()
                if line.startswith("Tracing") or line.startswith("Detaching"):
                    continue
                if re.match(r"\d{2}:\d{2}:\d{2}", line):
                    if group:
                        groups.append(group)
                        group = []
                if line:
                    group.append(line)

            if group:
                groups.append(group)

            output_data = []

            for group in groups:
                time_info = group[0].split()[0]  # 提取时间信息
                pid_info = group[-1].split()[0]  # 提取pid
                command_info = group[-1].split()[1]  # 提取命令
                total_rx = sum([int(row.split()[-2]) for row in group[2:]])
                total_tx = sum([int(row.split()[-1]) for row in group[2:]])

                # 组织数据为字典形式
                data = {
                    "Time": time_info,
                    "PID": pid_info,
                    "Command": command_info,
                    "RX_KB": total_rx,
                    "TX_KB": total_tx,
                }
                output_data.append(data)

            # print(output_data)
            # 构建输出文件路径
            output_dir = os.path.join(self.dir, test_function)
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, "btcp_{}.json".format(process_name))

            # 将数据写入 JSON 文件
            with open(output_file, "w") as outfile:
                json.dump(output_data, outfile, indent=4)

    def handle_test_data(self, function_id):
        test_function = self.test_functions[function_id]
        init_file_name = os.path.join(self.dir, f"init_{test_function}.txt")
        dirname = os.path.join(self.dir, test_function)
        os.makedirs(dirname, exist_ok=True)
        result_files = dict()
        for index in range(len(self.target_processes)):
            file_name = os.path.join(dirname, self.target_processes[index])
            f = open(file_name, mode='w', encoding='utf-8')
            # f.write("//handle time: " + time.ctime() + "\n")
            result_files[self.target_processes[index]] = f

        init_f = open(init_file_name, mode='r', encoding='utf-8')
        line = init_f.readline()
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

            line = init_f.readline()
        time_f = open(os.path.join(dirname, 'time'), mode='w', encoding='utf-8')
        test_time = str(stop_time_stamp - start_time_stamp)
        time_f.write(test_time + '\n')
        time_f.write(start_time + '\n')
        time_f.write(stop_time + '\n')
        # 关闭文件句柄
        for index in range(len(self.target_processes)):
            result_files[self.target_processes[index]].close()
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

    def display_test_data_new(self, function_id):
        test_function = self.test_functions[function_id]
        file_path = os.path.join(self.dir, f'{test_function}_result.md')
        if os.path.exists(file_path):
            os.remove(file_path)
        # 保存当前功能测试数据的文件夹
        dirname = os.path.join(self.dir, test_function)
        time_format = '%H:%M:%S'

        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f"### {self.translation[test_function]}性能数据：" + '\n\n')
            f.write("在仅开启 {} 功能的情况下，各进程组件性能测试结果如下（测试时间{}s）：".format(test_function,
                                                                                               300) + '\n\n')
        # print("在仅开启 {} 功能的情况下，各进程组件性能测试结果如下（测试时间{}s）：".format(test_function, test_time))

        func_average_cpu = 0.0
        func_average_mem = 0.0
        func_average_rd = 0.0
        func_average_wd = 0.0
        func_average_iops = 0.0
        func_average_network_io = 0.0

        # 采样点个数
        wid_pidstat = 3  # 采样间隔
        wid_bio = 10  # 采样间隔
        wid_btcp = 10  # 采样间隔
        len_pidstat = 100+1  # 300秒，每3秒采一个样
        len_bio = 30  # 300秒，每10秒采一个样
        len_btcp = 30  # 300秒，每10秒采一个样

        fig, axs = plt.subplots(6, 2, figsize=(12, 20))
        processes_pf_list = []

        # 打开结果文件
        result_f = open(file_path, 'a', encoding='utf-8')

        # 写入平均值
        header = "| 进程名 | vcpu平均占用率 | RSS平均大小 | 读数据平均速率 | 写数据平均速率 | IOPS平均值 | network_io平均值 \n" \
                 "| --- | --- | --- | --- | --- | --- | --- |\n"
        result_f.write(header)

        for index in range(len(self.target_processes)):

            process_cpu_total = 0.0
            process_mem_total = 0.0
            process_rd_total = 0.0
            process_wd_total = 0.0
            process_iops_total = 0.0
            process_network_io_total = 0.0

            process_cpu_usage = []
            process_mem_usage = []
            process_rd_usage = []
            process_wd_usage = []
            process_iops_usage = []
            process_network_io_usage = []
            pidstat_process_time = []
            bio_process_time = []
            btcp_process_time = []

            pidstat_result = os.path.join(dirname, "pidstat_" + self.target_processes[index] + ".json")
            bio_result = os.path.join(dirname, "bio_" + self.target_processes[index] + ".json")
            btcp_result = os.path.join(dirname, "btcp_" + self.target_processes[index] + ".json")

            if PFUtil.is_file_empty(pidstat_result) or (not os.path.exists(pidstat_result)):
                continue
            else:
                with open(pidstat_result, 'r') as f:
                    json_lines = json.load(f)
                    start_flag = True
                    start_time_object = None
                    for json_line in json_lines:
                        if start_flag == True:
                            start_time_object = datetime.strptime(json_line['Time'], time_format)
                            start_flag = False
                        time_object = datetime.strptime(json_line['Time'], time_format)
                        time_zeroed = (time_object - start_time_object).total_seconds()
                        pidstat_process_time.append(time_zeroed)

                        process_cpu_total += float(json_line['CPU'])
                        process_mem_total += float(json_line['RSS'])
                        process_rd_total += float(json_line['Disk_rd'])
                        process_wd_total += float(json_line['Disk_wr'])

                        process_cpu_usage.append(float(json_line['CPU']))
                        process_mem_usage.append(float(json_line['RSS']))
                        process_rd_usage.append(float(json_line['Disk_rd']))
                        process_wd_usage.append(float(json_line['Disk_wr']))

            if PFUtil.is_file_empty(bio_result) or (not os.path.exists(bio_result)):
                pass
            else:
                with open(bio_result, 'r') as f:
                    json_lines = json.load(f)
                    start_flag = True
                    start_time_object = None
                    for json_line in json_lines:
                        if start_flag == True:
                            start_time_object = datetime.strptime(json_line['Time'], time_format)
                            start_flag = False
                        time_object = datetime.strptime(json_line['Time'], time_format)
                        time_zeroed = (time_object - start_time_object).total_seconds()
                        bio_process_time.append(time_zeroed)

                        process_iops_total += float(json_line['I/O'])
                        process_iops_usage.append(float(json_line['I/O']))

            if PFUtil.is_file_empty(btcp_result) or (not os.path.exists(btcp_result)):
                pass
            else:
                with open(btcp_result, 'r') as f:
                    json_lines = json.load(f)
                    start_flag = True
                    start_time_object = None
                    for json_line in json_lines:
                        if start_flag == True:
                            start_time_object = datetime.strptime(json_line['Time'], time_format)
                            start_flag = False
                        time_object = datetime.strptime(json_line['Time'], time_format)
                        time_zeroed = (time_object - start_time_object).total_seconds()
                        btcp_process_time.append(time_zeroed)

                        process_network_io_total += (float(json_line['TX_KB'])+float(json_line['RX_KB']))
                        process_network_io_usage.append(float(json_line['TX_KB'])+float(json_line['RX_KB']))

            # 将当前进程的性能数据放入列表中
            processes_pf_list.append(
                [pidstat_process_time, bio_process_time, btcp_process_time,
                 process_cpu_usage, process_mem_usage, process_rd_usage, process_wd_usage,
                 process_iops_usage, process_network_io_usage])

            # 因采样时间不同，这里要做修改
            process_average_cpu = 0
            process_average_mem = 0
            process_average_rd = 0
            process_average_wd = 0
            process_average_iops = 0
            process_average_network_io = 0

            if process_cpu_total:
                # tmp_len_pidstat = int(pidstat_process_time[-1] + 1)
                # if tmp_len_pidstat > len_pidstat:
                #     len_pidstat = tmp_len_pidstat
                process_average_cpu = process_cpu_total / len_pidstat
                func_average_cpu += process_average_cpu
            if process_mem_total:
                process_average_mem = process_mem_total / len_pidstat
                func_average_mem += process_average_mem
            if process_rd_total:
                process_average_rd = process_rd_total / len_pidstat
                func_average_rd += process_average_rd
            if process_wd_total:
                process_average_wd = process_wd_total / len_pidstat
                func_average_wd += process_average_wd
            if process_iops_total:
                # tmp_len_bio = int(bio_process_time[-1] / 10 + 1)
                # if tmp_len_bio > len_bio:
                #     len_bio = tmp_len_bio
                process_average_iops = process_iops_total / len_bio
                func_average_iops += process_average_iops
            if process_network_io_total:
                # tmp_len_btcp = int(btcp_process_time[-1] / 10 + 1)
                # if tmp_len_btcp > len_btcp:
                #     len_btcp = tmp_len_btcp
                process_average_network_io = process_network_io_total / len_btcp
                func_average_network_io += process_average_network_io

            row = "| {} | {:.2f}% | {:.2f}MB | {:.2f}KB/s | {:.2f}KB/s | {:.2f} | {:.2f} \n" \
                .format(self.target_processes[index], process_average_cpu, process_average_mem, process_average_rd,
                        process_average_wd, process_average_iops, process_average_network_io)
            result_f.write(row)

        total_row = "| {} | {:.2f}% | {:.2f}MB | {:.2f}KB/s | {:.2f}KB/s | {:.2f} | {:.2f} \n". \
            format("全部进程", func_average_cpu, func_average_mem, func_average_rd, func_average_wd, func_average_iops,
                   func_average_network_io)
        result_f.write(total_row)

        # 写入最大值
        result_f.write("\n")
        header = "| 进程名 | vcpu最高占用率 | RSS最大值 | 读数据最高速率 | 写数据最高速率 | IOPS最大值 | network_io最大值 \n" \
                 "| --- | --- | --- | --- | --- | --- | --- |\n"
        result_f.write(header)

        func_cpu_data = {wid_pidstat*x: 0 for x in range(len_pidstat)}
        func_mem_data = {wid_pidstat*x: 0 for x in range(len_pidstat)}
        func_rd_data = {wid_pidstat*x: 0 for x in range(len_pidstat)}
        func_wd_data = {wid_pidstat*x: 0 for x in range(len_pidstat)}

        func_iops_data = {wid_bio*x: 0 for x in range(len_bio)}
        func_network_io_data = {wid_btcp*x: 0 for x in range(len_btcp)}

        for index in range(len(processes_pf_list)):
            process_cpu_data = {wid_pidstat*x: 0 for x in range(len_pidstat)}
            process_mem_data = {wid_pidstat*x: 0 for x in range(len_pidstat)}
            process_rd_data = {wid_pidstat*x: 0 for x in range(len_pidstat)}
            process_wd_data = {wid_pidstat*x: 0 for x in range(len_pidstat)}

            process_iops_data = {wid_bio*x: 0 for x in range(len_bio)}
            process_network_io_data = {wid_btcp*x: 0 for x in range(len_btcp)}

            for time, cpu, mem, rd, wd in zip(processes_pf_list[index][0], processes_pf_list[index][3],
                                              processes_pf_list[index][4], processes_pf_list[index][5],
                                              processes_pf_list[index][6]):
                time = int(time / wid_pidstat) * wid_pidstat
                func_cpu_data[time] += cpu
                func_mem_data[time] += mem
                func_rd_data[time] += rd
                func_wd_data[time] += wd

                process_cpu_data[time] += cpu
                process_mem_data[time] += mem
                process_rd_data[time] += rd
                process_wd_data[time] += wd

            for time, iops in zip(processes_pf_list[index][1], processes_pf_list[index][7]):
                time = int(time / wid_bio) * wid_bio
                func_iops_data[time] += iops
                process_iops_data[time] += iops

            for time, network_io in zip(processes_pf_list[index][2], processes_pf_list[index][8]):
                time = int(time / wid_btcp) * wid_btcp
                print(time)
                func_network_io_data[time] += network_io
                process_network_io_data[time] += network_io

            # if len(processes_pf_list[index][3]):
            axs[0, 0].plot(list(process_cpu_data.keys()), list(process_cpu_data.values()),
                           label=self.target_processes[index])
            axs[0, 1].plot(list(process_mem_data.keys()), list(process_mem_data.values()),
                           label=self.target_processes[index])
            axs[2, 0].plot(list(process_rd_data.keys()), list(process_rd_data.values()),
                           label=self.target_processes[index])
            axs[2, 1].plot(list(process_wd_data.keys()), list(process_wd_data.values()),
                           label=self.target_processes[index])

            # if len(processes_pf_list[index][7]):
            axs[4, 0].plot(list(process_iops_data.keys()), list(process_iops_data.values()),
                           label=self.target_processes[index])
            # if len(processes_pf_list[index][8]):
            axs[4, 1].plot(list(process_network_io_data.keys()), list(process_network_io_data.values()),
                           label=self.target_processes[index])

            row = "| {} | {:.2f}% | {:.2f}MB | {:.2f}KB/s | {:.2f}KB/s | {:.2f} | {:.2f} \n" \
                .format(self.target_processes[index], max(process_cpu_data.values(), default=0),
                        max(process_mem_data.values(), default=0),
                        max(process_rd_data.values(), default=0),
                        max(process_wd_data.values(), default=0),
                        max(process_iops_data.values(), default=0),
                        max(process_network_io_data.values(), default=0))
            result_f.write(row)

        total_row = "| {} | {:.2f}% | {:.2f}MB | {:.2f}KB/s | {:.2f}KB/s | {:.2f} | {:.2f} \n". \
            format("全部进程", max(func_cpu_data.values(), default=0), max(func_mem_data.values(), default=0),
                   max(func_rd_data.values(), default=0), max(func_wd_data.values(), default=0),
                   max(func_iops_data.values(), default=0),
                   max(func_network_io_data.values(), default=0))
        result_f.write(total_row)

        # 绘制总资源消耗的曲线
        axs[1, 0].plot(list(func_cpu_data.keys()), list(func_cpu_data.values()),
                       label='total')
        axs[1, 1].plot(list(func_mem_data.keys()), list(func_mem_data.values()),
                       label='total')
        axs[3, 0].plot(list(func_rd_data.keys()), list(func_rd_data.values()),
                       label='total')
        axs[3, 1].plot(list(func_wd_data.keys()), list(func_wd_data.values()),
                       label='total')
        axs[5, 0].plot(list(func_iops_data.keys()), list(func_iops_data.values()),
                       label='total')
        axs[5, 1].plot(list(func_network_io_data.keys()), list(func_network_io_data.values()),
                       label='total')

        # 设置子图标题、轴标签和图例
        for i in range(6):  # 6行
            for j in range(2):  # 2列
                axs[i, j].set_xlabel('time (seconds)')

        axs[0, 0].set_ylabel('vcpu (%)')
        axs[1, 0].set_ylabel('vcpu (%)')
        axs[0, 1].set_ylabel('RSS (MB)')
        axs[1, 1].set_ylabel('RSS (MB)')
        axs[2, 0].set_ylabel('rd (KB/s)')
        axs[3, 0].set_ylabel('rd (KB/s)')
        axs[2, 1].set_ylabel('wd (KB/s)')
        axs[3, 1].set_ylabel('wd (KB/s)')
        axs[4, 0].set_ylabel('iops')
        axs[5, 0].set_ylabel('iops')
        axs[4, 1].set_ylabel('network_io')
        axs[5, 1].set_ylabel('network_io')

        axs[0, 0].set_title('process CPU usage')
        axs[0, 1].set_title('process MEM usage')
        axs[1, 0].set_title('total CPU usage')
        axs[1, 1].set_title('total MEM usage')
        axs[2, 0].set_title('process RD usage')
        axs[2, 1].set_title('process WD usage')
        axs[3, 0].set_title('total RD usage')
        axs[3, 1].set_title('total WD usage')
        axs[4, 0].set_title('process iops usage')
        axs[4, 1].set_title('process network_io usage')
        axs[5, 0].set_title('total iops usage')
        axs[5, 1].set_title('total network_io usage')

        for i in range(6):  # 6行
            for j in range(2):  # 2列
                axs[i, j].legend()

        plt.tight_layout()
        fig_path = os.path.join(self.dir, f'{test_function}.png')
        # 保存图片
        plt.savefig(fig_path, dpi=300)

        result_f.write(f"### {self.translation[test_function]}性能数据图：" + '\n\n')
        alt_text = "fig"
        result_f.write(f"![{alt_text}]({fig_path})\n")
        result_f.close()

    @staticmethod
    def turn_database_to_table(database, query):
        def query_db(database, query):
            connection = sqlite3.connect(database)
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]
            connection.close()
            return column_names, results

        def format_table(column_names, data):
            markdown_table = "| ID | " + " | ".join(column_names) + " |\n"
            markdown_table += "| --- | " + " | ".join(["---"] * len(column_names)) + " |\n"

            for index, row in enumerate(data, start=1):
                formatted_row = [str(item).replace('\n', ' ').replace('|', '\\|') for item in row]
                markdown_table += f"| {index} | " + " | ".join(formatted_row) + " |\n"

            return markdown_table

        column_names, data = query_db(database, query)
        markdown_table = format_table(column_names, data)
        return len(data), markdown_table

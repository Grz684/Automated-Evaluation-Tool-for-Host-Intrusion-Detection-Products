import os
import json
import sqlite3
import time
from datetime import datetime

from matplotlib import pyplot as plt


class PFUtil:
    def __init__(self, test_functions, dir, target_processes, translation):
        self.test_functions = test_functions
        self.dir = dir
        self.target_processes = target_processes
        self.translation = translation

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

    def display_test_data(self, function_id):
        test_function = self.test_functions[function_id]
        file_path = os.path.join(self.dir, f'{test_function}_result.md')
        if os.path.exists(file_path):
            os.remove(file_path)
        dirname = os.path.join(self.dir, test_function)

        with open(os.path.join(dirname, 'time'), mode='r', encoding='utf-8') as time_f:
            test_time = int(time_f.readline().strip())
            start_time = time_f.readline().strip()
            time_format = '%H:%M:%S'
            start_time_object = datetime.strptime(start_time, time_format)

        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f"### {self.translation[test_function]}性能数据：" + '\n\n')
            f.write("在仅开启 {} 功能的情况下，各进程组件性能测试结果如下（测试时间{}s）：".format(test_function,
                                                                                               test_time) + '\n\n')
        # print("在仅开启 {} 功能的情况下，各进程组件性能测试结果如下（测试时间{}s）：".format(test_function, test_time))

        func_average_cpu = 0.0
        func_average_mem = 0.0
        func_average_rd = 0.0
        func_average_wd = 0.0
        fig, axs = plt.subplots(2, 2, figsize=(20, 8))
        processes_pf_list = []

        with open(file_path, 'a', encoding='utf-8') as result_f:
            header = "| 进程名 | vcpu平均占用率 | 驻留物理内存平均大小（RSS） | 读数据平均速率 | 写数据平均速率 \n| --- | --- | --- | --- | --- |\n"
            result_f.write(header)

            for index in range(len(self.target_processes)):

                process_cpu_total = 0.0
                process_mem_total = 0.0
                process_rd_total = 0.0
                process_wd_total = 0.0
                process_cpu_usage = []
                process_mem_usage = []
                process_rd_usage = []
                process_wd_usage = []
                process_time = []

                file_name = os.path.join(dirname, self.target_processes[index])
                if PFUtil.is_file_empty(file_name):
                    continue
                f = open(file_name, mode='r', encoding='utf-8')
                line = f.readline().strip()

                while line:
                    json_line = json.loads(line)

                    time_object = datetime.strptime(json_line['time'], time_format)
                    time_zeroed = (time_object - start_time_object).total_seconds()
                    process_time.append(time_zeroed)

                    process_cpu_total += float(json_line['cpu'])
                    process_mem_total += float(json_line['RSS']) / 1024
                    process_rd_total += float(json_line['kB_rd'])
                    process_wd_total += float(json_line['kB_wr'])
                    process_cpu_usage.append(float(json_line['cpu']))
                    process_mem_usage.append(float(json_line['RSS']) / 1024)
                    process_rd_usage.append(json_line['kB_rd'])
                    process_wd_usage.append(json_line['kB_wr'])

                    line = f.readline().strip()

                f.close()

                # 将当前进程的性能数据放入列表中
                processes_pf_list.append(
                    zip(process_time, process_cpu_usage, process_mem_usage, process_rd_usage, process_wd_usage))

                process_average_cpu = process_cpu_total / test_time
                process_average_mem = process_mem_total / test_time
                process_average_rd = process_rd_total / test_time
                process_average_wd = process_wd_total / test_time

                func_average_cpu += process_average_cpu
                func_average_mem += process_average_mem
                func_average_rd += process_average_rd
                func_average_wd += process_average_wd

                row = "| {} | {:.2f}% | {:.2f}MB | {:.2f}KB/s | {:.2f}KB/s \n".format(self.target_processes[index],
                                                                                      process_average_cpu,
                                                                                      process_average_mem,
                                                                                      process_average_rd,
                                                                                      process_average_wd)
                result_f.write(row)

                # with open(file_path, 'a', encoding='utf-8') as f:
                #     f.write("进程{}:\naverage_cpu: {:.2f} %, average_mem: {:.2f} %"
                #             .format(self.target_processes[index], process_average_cpu, process_average_mem) + '\n\n')
                # print("进程{}:\naverage_cpu: {:.2f} %, average_mem: {:.2f} %"
                #       .format(self.target_processes[index], process_average_cpu, process_average_mem))

        # 绘制单个进程消耗的曲线
        func_cpu_data = {x: 0 for x in range(test_time + 1)}
        func_mem_data = {x: 0 for x in range(test_time + 1)}
        for index in range(len(processes_pf_list)):
            process_cpu_data = {x: 0 for x in range(test_time + 1)}
            process_mem_data = {x: 0 for x in range(test_time + 1)}
            for time, cpu, mem, rd, wd in processes_pf_list[index]:
                func_cpu_data[time] += cpu
                func_mem_data[time] += mem
                process_cpu_data[time] += cpu
                process_mem_data[time] += mem

            axs[0, 0].plot(list(process_cpu_data.keys()), list(process_cpu_data.values()),
                           label=self.target_processes[index])
            axs[0, 1].plot(list(process_mem_data.keys()), list(process_mem_data.values()),
                           label=self.target_processes[index])

        # 绘制总资源消耗的曲线
        axs[1, 0].plot(list(func_cpu_data.keys()), list(func_cpu_data.values()),
                       label='total')
        axs[1, 1].plot(list(func_mem_data.keys()), list(func_mem_data.values()),
                       label='total')

        # 设置子图标题、轴标签和图例
        axs[0, 0].set_xlabel('time (seconds)')
        axs[0, 1].set_xlabel('time (seconds)')
        axs[0, 0].set_ylabel('vcpu (%)')
        axs[0, 1].set_ylabel('RSS (MB)')
        axs[0, 0].set_title('process CPU usage')
        axs[0, 1].set_title('process MEM usage')
        axs[0, 0].legend()
        axs[0, 1].legend()

        axs[1, 0].set_xlabel('time (seconds)')
        axs[1, 0].set_ylabel('vcpu (%)')
        axs[1, 1].set_xlabel('time (seconds)')
        axs[1, 1].set_ylabel('RSS (MB)')
        axs[1, 0].set_title('total CPU usage')
        axs[1, 1].set_title('total MEM usage')

        plt.tight_layout()
        fig_path = os.path.join(self.dir, f'{test_function}.png')
        # 保存图片
        plt.savefig(fig_path, dpi=300)
        with open(file_path, 'a', encoding='utf-8') as f:
            row = "| {} | {:.2f}% | {:.2f}MB | {:.2f}KB/s | {:.2f}KB/s \n".format("全部进程", func_average_cpu,
                                                         func_average_mem, func_average_rd, func_average_wd)
            f.write(row)
            # f.write("总资源占用:\naverage_cpu: {:.2f} %, average_mem: {:.2f} %"
            #         .format(func_average_cpu, func_average_mem) + '\n\n')
            f.write(f"### {self.translation[test_function]}性能数据图：" + '\n\n')
            alt_text = "vul_scan_fig"
            f.write(f"![{alt_text}]({fig_path})\n")

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

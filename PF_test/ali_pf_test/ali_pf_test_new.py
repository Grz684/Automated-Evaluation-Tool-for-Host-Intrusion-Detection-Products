import time
import threading
from Remote.ssh_client import SSHConnection
from Ali.ali_api import AliAPI
from Ali.baseline import BaselineInfo
from typing import List
from tabulate import tabulate
import json
import os
import re

current_dir = os.getcwd()

# 登录信息
ssh_hostname = "10.10.21.172"
ssh_username = "root"
ssh_password = "123456"

# 阿里云ak
accessKeyId = "LTAI5tHTkkKKy7MfiBfxVm2P"
accessKeySecret = "zmpDfZSWsTKXZQhxRHxTkCHvgfQDAK"

# 基线信息
baseline_names = ['阿里云标准-Docker安全基线检查',
                  '阿里云标准-Kubernetes-Master安全基线检查',
                  '阿里云标准-Kubernetes-Node安全基线检查',
                  ]

# 目标进程id
# AliDetect 0
# AliYunDunUpdate 1
# AliYunDun 2
# AliYunDunMonitor 3
# AliSecGuard 4
# AliHips 5
# AliNet 6
# AliSecureCheckAdvanced 7 开启基线检测会启动该进程

# 测试功能
target_processes = ["AliDetect", "AliYunDunUpdate", "AliYunDun", "AliYunDunMonitor", "AliSecureCheckAdvanced"]
test_functions = ["nothing_open", "baseline_scan"]


def ali_normal_test():
    """
    阿里性能测试，负责测试系统负载和agent大小
    :return:
    """
    ssh_test = SSHConnection(ssh_hostname, ssh_username, ssh_password)
    # 测试系统负载
    uptime_output = ssh_test.exec_command("uptime")[0]
    pattern = r"load average: ([0-9]+\.[0-9]+), ([0-9]+\.[0-9]+), ([0-9]+\.[0-9]+)"
    match = re.search(pattern, uptime_output)
    if match:
        load_1 = float(match.group(1))
        load_5 = float(match.group(2))
        load_15 = float(match.group(3))
        print(f"Current system load averages:\n - 1 minute: \t{load_1:.2f}\n - 5 minutes: \t{load_5:.2f}\n "
              f"- 15 minutes: \t{load_15:.2f}")
    else:
        print("Failed to parse uptime output.")

    # 测试agent大小
    agent_output = ssh_test.exec_command("du -h --max-depth=0 /usr/local/aegis/")[0]
    agent_size = re.findall(r'^\S+', agent_output)[0]
    print(f"Ali Cloud Agent Size:\t{agent_size}")

    ssh_test.close()


def ali_pidstat_test(function_id, test_time=30):
    """
    阿里云性能测试，使用pidstat测试vcpu，mem，disk读写速率
    :param function_id: 测试的功能序号
    :param test_time: 测试时间
    :return:
    """
    test_function = test_functions[function_id]
    ssh_check = SSHConnection(ssh_hostname, ssh_username, ssh_password)

    # 检测对应进程是否启动
    check_start(test_function, ssh_check, 1)

    # 测试cpu，内存，读写
    ssh_pidstat = SSHConnection(ssh_hostname, ssh_username, ssh_password)
    # 执行pidstat命令，并将输出重定向到文件中
    pidstat_command = "pidstat -urd -l -h 1 10000 | grep ae[g]is | awk '{printf \"{" \
                      "\\\"cpu\\\":\\\"%s\\\"," \
                      "\\\"VSZ\\\":\\\"%s\\\", \\\"RSS\\\":\\\"%s\\\"," \
                      "\\\"kB_rd\\\":\\\"%s\\\", \\\"kB_wr\\\":\\\"%s\\\"," \
                      "\\\"command\\\":\\\"%s\\\"," \
                      "\\\"time\\\":\\\"%s\\\"}\\n\",$8,$12,$13,$15,$16,$19,$1}' 1> /tmp/test.txt " \
                      "2>/dev/null"
    # tmux后台运行
    print("-" * 50)
    print("Executing pidstat performance test for Ali......")
    print("-" * 50)
    session_name = f'ali-pidstat={function_id}'
    ssh_pidstat.create_tmux_session(session_name)
    ssh_pidstat.attach_to_tmux_session(session_name)
    ssh_pidstat.exec_command(pidstat_command, False)
    ssh_pidstat.close()

    # 未开启功能，休眠test_time
    # if function_id == 0:
    #     time.sleep(test_time)
    # else:
    #     # 检测对应进程是否结束
    #     check_end(test_function, ssh_check, 1)

    # 休眠测试时间
    time.sleep(test_time)

    # 结束检测任务
    ssh_end = SSHConnection(ssh_hostname, ssh_username, ssh_password)
    ssh_end.exec_command("killall pidstat")
    ssh_end.kill_tmux_session(session_name)
    ssh_end.close()

    # 获取检测结果
    time.sleep(5)
    test_result = ssh_check.exec_command("cat /tmp/test.txt")[0].strip()
    ssh_check.exec_command("rm /tmp/test.txt", False)

    # 记录数据
    os.makedirs("ali", exist_ok=True)
    basename = os.path.join(current_dir, 'Ali', 'ali')
    file_name = basename + "/init_" + test_function + ".txt"
    f = open(file_name, mode='w', encoding='utf-8')
    f.write(test_result)
    ssh_check.close()
    f.close()


def ali_bcc_test(function_id, test_time=30):
    """
    阿里性能测试，使用bcc测试iops,network io
    :param function_id: 测试的功能序号
    :param test_time: 测试的时间
    :return:
    """
    # 测试前准备
    test_function = test_functions[function_id]
    ssh_check = SSHConnection(ssh_hostname, ssh_username, ssh_password)
    ssh_bcc = SSHConnection(ssh_hostname, ssh_username, ssh_password)
    # 检测对应进程是否启动
    check_start(test_function, ssh_check, 1)
    # 获取正在运行的进程名
    # process_names = get_running_process(ssh_bio)
    # 常态['AliDetect', 'AliYunDunUpdate', 'AliYunDun', 'AliYunDunMonitor']

    # 开始测试
    print("-" * 50)
    print("Executing bcc performance test for Ali......")
    print("-" * 50)
    bcc_command = "sh /home/ubuntu/test/sh/bcc-AliAll.sh"
    # tmux后台运行
    session_name = f'ali-bcc={function_id}'
    ssh_bcc.create_tmux_session(session_name)
    ssh_bcc.exec_command(f'tmux send-keys -t {session_name} "{bcc_command}" Enter')
    ssh_bcc.close()

    # 休眠test_time
    time.sleep(test_time)

    # 执行biotop命令，并将输出重定向到文件中
    # print("-" * 50)
    # print("Executing biotop performance test......")
    # print("-" * 50)
    # bio_procs = ['AliYunDunMonitor']
    # for bio_proc in bio_procs:
    #     # 只有AliYunDunMonitor有io，而且不常见
    #     bio_command = "sh /home/ubuntu/test/sh/bio-{}.sh".format(bio_proc)
    #     session_name = f'ali-bio-{function_id}-{bio_proc}'
    #     ssh_bio.create_tmux_session(session_name)
    #     ssh_bio.exec_command(f'tmux send-keys -t {session_name} "{bio_command}" Enter')
    # ssh_bio.close()
    #
    # # 执行tcptop命令，并将输出重定向到文件中
    # print("-" * 50)
    # print("Executing tcptop performance test......")
    # print("-" * 50)
    # ssh_btcp = SSHConnection(ssh_hostname, ssh_username, ssh_password)
    # tcp_procs = ['AliYunDun']
    # for tcp_proc in tcp_procs:
    #     # 目前只发现AliYunDun有tcp，且很少见
    #     btcp_command = "sh /home/ubuntu/test/sh/btcp-{}.sh".format(tcp_proc)
    #     # print(btcp_command)
    #     session_name = f'ali-btcp={function_id}-{tcp_proc}'
    #     ssh_btcp.create_tmux_session(session_name)
    #     ssh_btcp.exec_command(f'tmux send-keys -t {session_name} "{btcp_command}" Enter')
    # ssh_btcp.close()

    # if function_id == 0:
    #     time.sleep(test_time)
    # else:
    #     # 检测对应进程是否结束
    #     check_end(test_function, ssh_check, 1)

    # 获取数据
    bio_procs = ['AliYunDunMonitor']
    for bio_proc in bio_procs:
        time.sleep(5)
        test_bio_result = ssh_check.exec_command(f"cat /tmp/bio-{bio_proc}.txt")[0].strip()
        ssh_check.exec_command(f"rm /tmp/bio-{bio_proc}.txt", False)
        basename = os.path.join(current_dir, 'Ali', 'ali')
        os.makedirs("ali", exist_ok=True)
        file_name = basename + "/init_bio_{}_{}.txt".format(test_function, bio_proc)
        with open(file_name, 'w', encoding='utf-8') as f:
            if test_bio_result:
                f.write(test_bio_result)
                f.close()

    tcp_procs = ['AliYunDun']
    for tcp_proc in tcp_procs:
        time.sleep(5)
        test_btcp_result = ssh_check.exec_command(f"cat /tmp/btcp-{tcp_proc}.txt")[0].strip()
        ssh_check.exec_command(f"rm /tmp/btcp-{tcp_proc}.txt", False)
        basename = os.path.join(current_dir, 'Ali', 'ali')
        os.makedirs("ali", exist_ok=True)
        file_name = basename + "/init_btcp_{}_{}.txt".format(test_function, tcp_proc)
        with open(file_name, 'w', encoding='utf-8') as f:
            if test_btcp_result:
                f.write(test_btcp_result)
                f.close()

    # 结束检测任务
    ssh_check.close()
    ssh_end = SSHConnection(ssh_hostname, ssh_username, ssh_password)
    ssh_end.close()


def get_running_process(ssh: SSHConnection) -> List[str]:
    """
    获取正在运行的进程
    :param ssh: ssh会话
    :return:
    """
    check_command = "ps -ef | grep ae[g]is | awk '{printf \"\\\"%s\\\"\\n\",$8}'"
    process_paths = ssh.exec_command(check_command)[0].replace('"', '').strip().split("\n")
    # print(process_paths)
    running_processes = []
    for process_path in process_paths:
        path = process_path.split("/")
        running_processes.append(path[-1])
    # print(running_processes)
    return running_processes


def check_start(test_function, ssh, check_time):
    """
    循环检测对应进程是否启动
    :param test_function: 测试的功能
    :param ssh: ssh会话
    :param check_time: 检测间隔(s)
    :return:
    """
    while True:
        start_flag = check_status(test_function, ssh)
        if start_flag:
            break
        time.sleep(check_time)


def check_end(test_function, ssh, check_time):
    """
    循环检测对应进程是否结束
    :param test_function: 测试的功能
    :param ssh: ssh会话
    :param check_time: 检测间隔(s)
    :return:
    """
    while True:
        end_flag = not check_status(test_function, ssh)
        if end_flag:
            break
        time.sleep(check_time)


def check_status(test_function, ssh):
    """
    检查功能是否开启
    :param test_function:测试的功能
    :param ssh:ssh会话
    :return: False/True
    """
    running_processes = get_running_process(ssh)
    target_flag = False
    # 常态
    if test_function == test_functions[0]:
        target_flag = True
    # 基线检查
    if test_function == test_functions[1] and target_processes[4] in running_processes:
        target_flag = True

    return target_flag


def handle_pidstat_data(function_id):
    """
    处理测试数据
    :param function_id: 测试功能序号
    :return:
    """
    test_function = test_functions[function_id]
    basename = os.path.join(current_dir, 'Ali', 'ali')
    init_file_name = os.path.join(basename, 'init_{}'.format(test_function)) + ".txt"

    dirname = basename + '\\' + test_function
    os.makedirs(dirname, exist_ok=True)

    result_files = dict()
    output_data = {process: [] for process in target_processes}
    for process in target_processes:
        output_filename = os.path.join(dirname, f"pidstat_{process}.json")
        f = open(output_filename, mode='w', encoding='utf-8')
        result_files[process] = f

    with open(init_file_name, mode='r', encoding='utf-8') as init_file:
        for line in init_file:
            json_line = json.loads(line)
            command = json_line['command'].split('/')[-1]
            if command in result_files.keys():
                time_info = time.strptime(json_line['time'])
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
    for process in target_processes:
        json.dump(output_data[process], result_files[process], indent=4)
        result_files[process].write('\n')

    # 关闭文件句柄
    for process in target_processes:
        result_files[process].close()


def handle_bio_data(function_id):
    process_names = ['AliYunDunMonitor']
    test_function = test_functions[function_id]
    basename = os.path.join(current_dir, 'Ali', 'ali')
    for process_name in process_names:
        filename = basename + "/init_bio_{}_{}.txt".format(test_function, process_name)

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
        output_dir = os.path.join(basename, test_function)
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "bio_{}.json".format(process_name))

        # 将数据写入 JSON 文件
        with open(output_file, "w") as outfile:
            json.dump(output_data, outfile, indent=4)


def handle_btcp_data(function_id):
    process_names = ['AliYunDun']
    test_function = test_functions[function_id]
    basename = os.path.join(current_dir, 'Ali', 'ali')
    for process_name in process_names:
        filename = basename + "/init_btcp_{}_{}.txt".format(test_function, process_name)

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
        output_dir = os.path.join(basename, test_function)
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "btcp_{}.json".format(process_name))

        # 将数据写入 JSON 文件
        with open(output_file, "w") as outfile:
            json.dump(output_data, outfile, indent=4)


def run_ali_pf_test(indicator: str, check_type=' '):
    # 常驻状态
    ali_api = AliAPI(accessKeyId, accessKeySecret)
    baseline_info = BaselineInfo(accessKeyId, accessKeySecret)
    check_id = 0
    if check_type:
        check_id = int(check_type)
    if indicator == 'load':
        ali_normal_test()
    elif indicator == 'cpu':
        if check_id == 0:
            ali_pidstat_test(check_id, 100)
            handle_pidstat_data(check_id)
        elif check_id == 1:
            strategy_id = 40137696
            # ali_api.exec_strategy(strategy_id)
            # for baseline_name in baseline_names:
            #     baseline_info.print_baseline_summary(baseline_name)
            # ali_pidstat_test(check_id)
            handle_pidstat_data(check_id)
            # display_pidstat_data(check_id)
    elif indicator == 'io':
        if check_id == 0:
            # ali_bcc_test(0, 300)
            # add_time(check_id)
            handle_bio_data(check_id)
            handle_btcp_data(check_id)
            # display_btcp_data(check_id)
            # display_bio_data(check_id)
        elif check_id == 1:
            strategy_id = 40137696
            # ali_api.exec_strategy(strategy_id)
            # for baseline_name in baseline_names:
            #     baseline_info.print_baseline_summary(baseline_name)
            # ali_bcc_test(check_id)
            # handle_btcp_data(check_id)
            # handle_bio_data(check_id)
            # display_btcp_data(check_id)
            # display_bio_data(check_id)
    elif indicator == 'all':
        if check_id == 0:
            # 性能监控
            thread_pid = threading.Thread(target=ali_pidstat_test, args=(check_id, 300))
            thread_bcc = threading.Thread(target=ali_bcc_test, args=(check_id, 300))
            thread_pid.start()
            thread_bcc.start()
            thread_pid.join()
            thread_bcc.join()
            # 处理数据
            handle_pidstat_data(check_id)
            handle_bio_data(check_id)
            handle_btcp_data(check_id)
        elif check_id == 1:
            # 调用API执行测试
            strategy_id = 40137696
            ali_api.exec_strategy(strategy_id)
            # for baseline_name in baseline_names:
            #     baseline_info.print_baseline_summary(baseline_name)
            # 性能监控
            thread_pid = threading.Thread(target=ali_pidstat_test, args=(check_id, 300))
            thread_bcc = threading.Thread(target=ali_bcc_test, args=(check_id, 300))
            thread_pid.start()
            thread_bcc.start()
            thread_pid.join()
            thread_bcc.join()
            # 处理数据
            handle_pidstat_data(check_id)
            handle_bio_data(check_id)
            handle_btcp_data(check_id)
    else:
        print(f'indicator {indicator} not found!')


if __name__ == "__main__":
    run_ali_pf_test('all', '0')

import glob
import os
import re
import subprocess
import time

import yaml

from ssh import SSH
import configparser

with open("../config.yaml", "r") as f:
    config = yaml.safe_load(f)
agent = config["attackinfo"]
ssh_hostname = str(agent["ssh_hostname"])
ssh_username = str(agent["ssh_username"])
ssh_password = str(agent["ssh_password"])
root_username = str(agent['root_username'])
root_password = str(agent['root_password'])
attack_pattern = str(agent['attack_pattern'])
attack_target = str(agent['attack_target'])
assist_hostname = str(agent["assist_hostname"])
assist_username = str(agent["assist_username"])
assist_password = str(agent["assist_password"])
variables = {
    "test": "ccc",
    "host_name": ssh_hostname,
    "password": ssh_password,
    "user": ssh_username,
    "root_password": root_password,
    "assist_user": assist_username,
    "assist_hostname": assist_hostname,
    "assist_password": assist_password
}

def read_first_line(file_path):
    with open(file_path, 'r', encoding='UTF-8') as file:
        first_line = file.readline().strip()
    return first_line


def read_commands_from_file(file_path):
    with open(file_path, 'r', encoding='UTF-8') as file:
        file.readline()
        lines = file.readlines()

    commands_dict = {}
    current_section = None
    combined_command = []

    for line in lines:
        if line.startswith('#'):
            if current_section:
                commands_dict[current_section] = ' ; '.join(combined_command)
                combined_command = []
            current_section = line.strip()
        else:
            # 预定义参数渲染
            command = line.strip()
            for match in re.findall(r'%(\w+)%', command):
                if match in variables:
                    command = command.replace(f'%{match}%', variables[match])
            combined_command.append(command)

    if current_section and combined_command:
        commands_dict[current_section] = ' ; '.join(combined_command)

    return commands_dict


def prepare(command_file, client):
    if command_file == os.path.join("Attack", "defense-evasion", "T1480.001"):
        script_path = os.path.join("attack_file", "T1480.001.py")
        input_file_path = os.path.join("attack_file", "meterpreter_reverse_tcp.elf")
        output_file_path = os.path.join("attack_file", "test_T1480_enc")
        command = ["python", script_path, "encrypt", input_file_path, output_file_path, ssh_hostname]
        subprocess.run(command, text=True)

        local_file_1 = output_file_path
        remote_file_1 = "/tmp/test_T1480_enc"
        local_file_2 = os.path.join("attack_file", "T1480.001.py")
        remote_file_2 = "/tmp/T1480.001.py"
        # 创建SFTP会话
        sftp = client.open_sftp()
        # 将本地文件传输到远程主机
        sftp.put(local_file_1, remote_file_1)
        sftp.put(local_file_2, remote_file_2)
        # 关闭SFTP会话
        sftp.close()
    elif command_file == os.path.join("Attack", "discovery", "T1040"):
        local_file = os.path.join("attack_file", "linux_pcapdemo.c")
        remote_file = "/tmp/linux_pcapdemo.c"
        # 创建SFTP会话
        sftp = client.open_sftp()
        # 将本地文件传输到远程主机
        sftp.put(local_file, remote_file)
        # 关闭SFTP会话
        sftp.close()
    elif command_file == os.path.join("Attack", "credential-access", "T1003.007"):
        local_file = os.path.join("attack_file", "mimipenguin_2.0-release.tar.gz")
        remote_file = "/tmp/mimipenguin.tar.gz"
        # 创建SFTP会话
        sftp = client.open_sftp()
        # 将本地文件传输到远程主机
        sftp.put(local_file, remote_file)
        # 关闭SFTP会话
        sftp.close()
    elif command_file == os.path.join("Attack", "credential-access", "T1110.004"):
        local_file = os.path.join("attack_file", "credstuffuserpass.txt")
        remote_file = "/tmp/credstuffuserpass.txt"
        # 创建SFTP会话
        sftp = client.open_sftp()
        # 将本地文件传输到远程主机
        sftp.put(local_file, remote_file)
        # 关闭SFTP会话
        sftp.close()
    elif command_file == os.path.join("Attack", "credential-access", "T1552.004"):
        local_file = os.path.join("attack_file", "id_rsa")
        remote_file = "/tmp/id_rsa"
        # 创建SFTP会话
        sftp = client.open_sftp()
        # 将本地文件传输到远程主机
        sftp.put(local_file, remote_file)
        # 关闭SFTP会话
        sftp.close()
    elif command_file == os.path.join("Attack", "credential-access", "T1555"):
        local_file = os.path.join("attack_file", "LaZagne.zip")
        remote_file = "/tmp/LaZagne.zip"
        # 创建SFTP会话
        sftp = client.open_sftp()
        # 将本地文件传输到远程主机
        sftp.put(local_file, remote_file)
        # 关闭SFTP会话
        sftp.close()
    elif command_file == os.path.join("Attack", "credential-access", "T1556.003"):
        local_file = os.path.join("attack_file", "pam_evil.c")
        remote_file = "/tmp/pam_evil.c"
        # 创建SFTP会话
        sftp = client.open_sftp()
        # 将本地文件传输到远程主机
        sftp.put(local_file, remote_file)
        # 关闭SFTP会话
        sftp.close()
    elif command_file == os.path.join("Attack", "persistence", "T1098.004"):
        local_file = os.path.join("attack_file", "id_rsa.pub")
        remote_file = "/tmp/id_rsa.pub"
        # 创建SFTP会话
        sftp = client.open_sftp()
        # 将本地文件传输到远程主机
        sftp.put(local_file, remote_file)
        # 关闭SFTP会话
        sftp.close()
    elif command_file == os.path.join("Attack", "persistence", "T1543.002"):
        local_file = os.path.join("attack_file", "T1543.002")
        remote_file = "/tmp/T1543.002"
        # 创建SFTP会话
        sftp = client.open_sftp()
        # 将本地文件传输到远程主机
        sftp.put(local_file, remote_file)
        # 关闭SFTP会话
        sftp.close()
    elif command_file == os.path.join("Attack", "persistence", "T1547.006"):
        local_file = os.path.join("attack_file", "Diamorphine-master.zip")
        remote_file = "/tmp/Diamorphine-master.zip"
        # 创建SFTP会话
        sftp = client.open_sftp()
        # 将本地文件传输到远程主机
        sftp.put(local_file, remote_file)
        # 关闭SFTP会话
        sftp.close()
    elif command_file == os.path.join("Attack", "defense-evasion", "T1014"):
        local_file = os.path.join("attack_file", "Diamorphine-master.zip")
        remote_file = "/tmp/Diamorphine-master.zip"
        # 创建SFTP会话
        sftp = client.open_sftp()
        # 将本地文件传输到远程主机
        sftp.put(local_file, remote_file)
        # 关闭SFTP会话
        sftp.close()
    elif command_file == os.path.join("Attack", "defense-evasion", "T1027.001"):
        local_file = os.path.join("attack_file", "malware_test")
        remote_file = "/tmp/malware_test"
        # 创建SFTP会话
        sftp = client.open_sftp()
        # 将本地文件传输到远程主机
        sftp.put(local_file, remote_file)
        # 关闭SFTP会话
        sftp.close()
    elif command_file == os.path.join("Attack", "defense-evasion-try", "T1027.002"):
        local_file1 = os.path.join("attack_file", "malware_test")
        remote_file1 = "/tmp/malware_test"
        local_file2 = os.path.join("attack_file", "upx.py")
        remote_file2 = "/tmp/upx.py"
        # 创建SFTP会话
        sftp = client.open_sftp()
        # 将本地文件传输到远程主机
        sftp.put(local_file1, remote_file1)
        sftp.put(local_file2, remote_file2)
        # 关闭SFTP会话
        sftp.close()
    elif command_file == os.path.join("Attack", "defense-evasion", "T1222.002"):
        local_file = os.path.join("attack_file", "malware_test")
        remote_file = "/tmp/malware_test"
        # 创建SFTP会话
        sftp = client.open_sftp()
        # 将本地文件传输到远程主机
        sftp.put(local_file, remote_file)
        # 关闭SFTP会话
        sftp.close()
    elif command_file == os.path.join("Attack", "defense-evasion", "T1553.004"):
        local_file = os.path.join("attack_file", "rootCA.crt")
        remote_file = "/tmp/rootCA.crt"
        # 创建SFTP会话
        sftp = client.open_sftp()
        # 将本地文件传输到远程主机
        sftp.put(local_file, remote_file)
        # 关闭SFTP会话
        sftp.close()
    elif command_file == os.path.join("Attack", "defense-evasion", "T1564.001"):
        local_file = os.path.join("attack_file", "malware_test")
        remote_file = "/tmp/malware_test"
        # 创建SFTP会话
        sftp = client.open_sftp()
        # 将本地文件传输到远程主机
        sftp.put(local_file, remote_file)
        # 关闭SFTP会话
        sftp.close()
    elif command_file == os.path.join("Attack", "defense-evasion-try", "T1055"):
        local_file = os.path.join("attack_file", "linux-process-injection.zip")
        remote_file = "/tmp/linux-process-injection.zip"
        # 创建SFTP会话
        sftp = client.open_sftp()
        # 将本地文件传输到远程主机
        sftp.put(local_file, remote_file)
        # 关闭SFTP会话
        sftp.close()
    elif command_file == os.path.join("Attack", "defense-evasion-try", "T1205.001"):
        local_file = os.path.join("attack_file", "knock-knock.c")
        remote_file = "/tmp/knock-knock.c"
        # 创建SFTP会话
        sftp = client.open_sftp()
        # 将本地文件传输到远程主机
        sftp.put(local_file, remote_file)
        # 关闭SFTP会话
        sftp.close()
    elif command_file == os.path.join("Attack", "defense-evasion-try", "T1548.001"):
        local_file = os.path.join("attack_file", "cap.c")
        remote_file = "/tmp/cap.c"
        # 创建SFTP会话
        sftp = client.open_sftp()
        # 将本地文件传输到远程主机
        sftp.put(local_file, remote_file)
        # 关闭SFTP会话
        sftp.close()
    elif command_file == os.path.join("Attack", "defense-evasion-try", "T1574.006"):
        local_file_1 = os.path.join("attack_file", "myhook.c")
        remote_file_1 = "/tmp/myhook.c"
        local_file_2 = os.path.join("attack_file", "target_program.c")
        remote_file_2 = "/tmp/target_program.c"
        # 创建SFTP会话
        sftp = client.open_sftp()
        # 将本地文件传输到远程主机
        sftp.put(local_file_1, remote_file_1)
        sftp.put(local_file_2, remote_file_2)
        # 关闭SFTP会话
        sftp.close()
    elif command_file == os.path.join("Attack", "defense-evasion-try", "T1620"):
        local_file_1 = os.path.join("attack_file", "ezuri.zip")
        remote_file_1 = "/tmp/ezuri.zip"
        local_file_2 = os.path.join("attack_file", "meterpreter_reverse_tcp.elf")
        remote_file_2 = "/tmp/meterpreter_reverse_tcp.elf"
        # 创建SFTP会话
        sftp = client.open_sftp()
        # 将本地文件传输到远程主机
        sftp.put(local_file_1, remote_file_1)
        sftp.put(local_file_2, remote_file_2)
        # 关闭SFTP会话
        sftp.close()

def exec_attack(command_file):
    first_line = read_first_line(command_file)
    need_wait = 0

    print(f"权限需求标记: {first_line}")
    if "Elevation Required" in first_line:
        ssh = SSH(ssh_hostname, root_username, root_password)
        client = ssh.connect()
    else:
        ssh = SSH(ssh_hostname, ssh_username, ssh_password)
        client = ssh.connect()
    if "Waiting Required" in first_line:
        need_wait = 1

    prepare(command_file, client)
    commands_dict = read_commands_from_file(command_file)

    for key, commands in commands_dict.items():
        print("当前阶段：" + key)
        if key != "#check":
            print("执行命令：" + commands + "\n")
        else:
            print("执行命令：" + commands)
        if key == "#check" and need_wait == 1:
            time.sleep(60)

        stdin, stdout, stderr = client.exec_command(commands)

        if key != "#nowait":
            # Wait for the current command to complete before proceeding to the next command
            exit_status = stdout.channel.recv_exit_status()

            if exit_status == 0:
                output = stdout.read().decode('utf-8')
                if key == "#check":
                    if output:
                        if re.search("No such file or directory", output):
                            print(command_file + ": 攻击失败")
                            print("攻击失败情况：")
                        else:
                            print(command_file + ": 攻击成功")
                            print("攻击成功证据：")
                    else:
                        print(command_file + ": 攻击失败")
                        print("攻击失败情况：")
                print(output)
            else:
                error_output = stderr.read().decode('utf-8')
                print(f"命令执行报错: {error_output}")

    ssh.close()


if __name__ == '__main__':
    if attack_pattern == "0":
        folder_path = 'Attack'
        print("开始测试全部技术：")
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for file_name in filenames:
                file_path = os.path.join(dirpath, file_name)
                print(print(f"开始测试技术{file_path}....."))
                exec_attack(file_path)

    elif attack_pattern == "1":
        folder_path = os.path.join("Attack", attack_target)
        print(f"开始测试{attack_target}战术下的全部技术：")
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                print(f"开始测试技术{file_path}.....")
                exec_attack(file_path)

    elif attack_pattern == "2":
        my_string = attack_target
        my_list = my_string.split(",")
        for file_name_to_find in my_list:
            folder_path = 'Attack'

            pattern = f"{folder_path}/**/{file_name_to_find}"
            matching_file = glob.glob(pattern, recursive=True)
            print(f"开始测试技术{matching_file[0]}.....")
            exec_attack(matching_file[0])

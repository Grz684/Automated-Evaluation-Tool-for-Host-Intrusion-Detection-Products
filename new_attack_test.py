import glob
import os
import re
import time

from ssh import SSH
import configparser

cf = configparser.ConfigParser()
cf.read("config.conf", encoding='utf-8')
ssh_hostname = cf['attackinfo']['ssh_hostname']
ssh_username = cf['attackinfo']['ssh_username']
ssh_password = cf['attackinfo']['ssh_password']
root_username = cf['attackinfo']['root_username']
root_password = cf['attackinfo']['root_password']
attack_pattern = cf['attackinfo']['attack_pattern']
attack_target = cf['attackinfo']['attack_target']


def read_first_line(file_path):
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()
    return first_line


def read_commands_from_file(file_path):
    with open(file_path, 'r') as file:
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
            combined_command.append(line.strip())

    if current_section and combined_command:
        commands_dict[current_section] = ' ; '.join(combined_command)

    return commands_dict


def exec_attack(command_file):
    first_line = read_first_line(command_file)
    need_wait = 0

    print(f"需求标记: {first_line}")
    if "Elevation Required" in first_line:
        ssh = SSH(ssh_hostname, root_username, root_password)
        client = ssh.connect()
    else:
        ssh = SSH(ssh_hostname, ssh_username, ssh_password)
        client = ssh.connect()
    if "Waiting Required" in first_line:
        need_wait = 1

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
        folder_path = 'Attack\\' + attack_target
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

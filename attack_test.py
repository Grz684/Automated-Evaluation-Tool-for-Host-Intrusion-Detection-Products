import glob
import time
from ssh import SSH
import json
import os
import re
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


def exec_attack(command_file):
    f = open(command_file, encoding='utf-8')
    line1 = f.readline().split(";")
    need_wait = 0
    if "Elevation Required" in line1:
        ssh = SSH(ssh_hostname, root_username, root_password)
    else:
        ssh = SSH(ssh_hostname, ssh_username, ssh_password)
    if "Waiting Required" in line1:
        need_wait = 1
    f.close()

    f = open(command_file, encoding='utf-8')
    f.readline()
    pre_status = 0
    current_status = 0
    std = []
    while True:
        line = f.readline()
        if line:
            # 判断状态
            if line == "#pre\n":
                print("pre")
                current_status = 1
                continue
            elif line == "#command\n":
                print("command")
                current_status = 2
                continue
            elif line == "#check\n":
                print("check")
                if need_wait == 1:
                    time.sleep(60)
                current_status = 3
                continue
            elif line == "#cleanup\n":
                print("cleanup")
                current_status = 4
                continue

            # 根据状态执行命令
            if pre_status != current_status:
                if std:
                    std[0].channel.shutdown_write()
                    res = std[1].read()
                    print(res)
                    if pre_status == 3:
                        if res.decode().strip():
                            if re.search("No such file or directory", res.decode().strip()):
                                print(command_file + ": attack fail")
                            else:
                                print(command_file + ": attack success")
                                print("攻击成功证据：")
                        else:
                            print(command_file + ": attack fail")
                        print(res.decode().strip() + "\n")
                    std[0].close()
                    std[1].close()
                    std[2].close()
                std = ssh.get_std()
                pre_status = current_status

            std[0].write(line)
            time.sleep(1)

        else:
            break

    ssh.close()
    f.close()


# directory = "Attack/collection"
# files = os.listdir("Attack/collection")
# for file in files:
#     command_file = directory + "/" + file
#     exec_attack(command_file)
#     time.sleep(30)
if __name__ == '__main__':
    if attack_pattern == "0":
        folder_path = 'Attack'
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for file_name in filenames:
                file_path = os.path.join(dirpath, file_name)
                print(file_path)
                exec_attack(file_path)

    elif attack_pattern == "1":
        folder_path = 'Attack\\' + attack_target

        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                print(file_path)
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

import paramiko


class SSH:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.client = self.connect()

    def connect(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.hostname, username=self.username, password=self.password)
        return client

    def exec_command(self, command):
        stdin, stdout, stderr = self.client.exec_command('bash')
        stdin.write(command)
        stdin.channel.shutdown_write()
        res = stdout.read()

        stdin.close()
        stdout.close()
        stderr.close()

        return res

    def exec_command_without_stdout(self, command):
        stdin, stdout, stderr = self.client.exec_command('bash')
        stdin.write(command)
        stdin.channel.shutdown_write()

        stdin.close()
        stdout.close()
        stderr.close()

    def get_std(self):
        stdin, stdout, stderr = self.client.exec_command('bash')
        return [stdin, stdout, stderr]

    def exec_command_infile(self, command_file, row_num):
        # row_num为目标命令所在行数（1~）
        # 获取命令
        f = open(command_file, encoding='utf-8')
        for i in range(row_num - 1):
            line = f.readline()
        command = f.readline()
        f.close()

        stdin, stdout, stderr = self.client.exec_command('bash')
        stdin.write(command)
        stdin.channel.shutdown_write()
        res = stdout.read()

        # Because they are file objects, they need to be closed
        stdin.close()
        stdout.close()
        stderr.close()

        return res

    def exec_command_without_stdout_infile(self, command_file, row_num):
        # row_num为目标命令所在行数（1~）
        # 获取命令
        f = open(command_file, encoding='utf-8')
        for i in range(row_num - 1):
            line = f.readline()
        command = f.readline()
        f.close()

        stdin, stdout, stderr = self.client.exec_command('bash')
        stdin.write(command)
        stdin.channel.shutdown_write()

        # Because they are file objects, they need to be closed
        stdin.close()
        stdout.close()
        stderr.close()

    def close(self):
        # Close the client itself
        self.client.close()

    def exec_command_file(self, command_file):
        # 获取命令
        commands = []
        f = open(command_file, encoding='utf-8')
        inputCommand = ""
        while True:
            line = f.readline()
            if line:
                commands.append(line)
            else:
                break
        f.close()

        if len(commands) != 0:
            for command in commands:
                inputCommand = inputCommand + command

        # 输入输出操作
        stdin, stdout, stderr = self.client.exec_command('bash')

        stdin.write(inputCommand)
        stdin.channel.shutdown_write()

        # print(f'STDOUT: {stdout.read().decode("utf8")}')
        # print(f'STDERR: {stderr.read().decode("utf8")}')
        # print(f'Return code: {stdout.channel.recv_exit_status()}')
        # print("")

        res = stdout.read()

        # Because they are file objects, they need to be closed
        stdin.close()
        stdout.close()
        stderr.close()

        return res

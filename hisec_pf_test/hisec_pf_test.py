import json

ali_target_processes = ["hisec_agent"]
ali_test_functions = ["nothing_open"]


def display_test_data(function_id):
    test_function = ali_test_functions[function_id]
    dirname = "huawei/" + test_function

    test_time = 1000

    print("在仅开启 {} 功能的情况下，各进程组件性能测试结果如下（测试时间{}s）：".format(test_function, test_time))

    func_average_cpu = 0.0
    func_average_mem = 0.0
    func_average_disk_read = 0.0
    func_average_disk_write = 0.0

    for index in range(len(ali_target_processes)):
        total_cpu = 0.0
        total_mem = 0.0
        total_disk_read = 0.0
        total_disk_write = 0.0

        file_name = dirname + "/" + ali_target_processes[index]
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
            .format(ali_target_processes[index], average_cpu, average_mem, average_disk_rd, average_disk_wr))

    print(
        "总资源占用:\naverage_cpu: {:.2f} %, average_mem: {:.2f} %, average_disk_rd: {:.2f} kb/s, average_disk_write: {:.2f} kb/s"
        .format(func_average_cpu, func_average_mem, func_average_disk_read, func_average_disk_write))


for i in range(len(ali_test_functions)):
    display_test_data(i)
    print("\n")

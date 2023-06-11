### 基线扫描性能数据：

在仅开启 baseline_scan 功能的情况下，各进程组件性能测试结果如下（测试时间300s）：

| 进程名 | vcpu平均占用率 | RSS平均大小 | 读数据平均速率 | 写数据平均速率 | IOPS平均值 | network_io平均值 
| --- | --- | --- | --- | --- | --- | --- |
| wsssr_defence_service | 3.21% | 0.08MB | 46.63KB/s | 2.36KB/s | 1.70 | 25.30 
| wsssr_defence_daemon | 0.08% | 0.00MB | 0.00KB/s | 0.04KB/s | 0.00 | 0.50 
| lbaselinescan | 0.35% | 0.00MB | 32.81KB/s | 0.32KB/s | 0.00 | 0.00 
| icsfilesec | 0.00% | 0.00MB | 0.00KB/s | 0.00KB/s | 0.00 | 0.00 
| 全部进程 | 3.63% | 0.08MB | 79.44KB/s | 2.72KB/s | 1.70 | 25.80 

| 进程名 | vcpu最高占用率 | RSS最大值 | 读数据最高速率 | 写数据最高速率 | IOPS最大值 | network_io最大值 
| --- | --- | --- | --- | --- | --- | --- |
| wsssr_defence_service | 9.00% | 0.08MB | 4670.67KB/s | 68.00KB/s | 18.00 | 222.00 
| wsssr_defence_daemon | 1.00% | 0.01MB | 0.00KB/s | 2.67KB/s | 0.00 | 6.00 
| lbaselinescan | 22.26% | 0.02MB | 2520.93KB/s | 17.28KB/s | 0.00 | 0.00 
| icsfilesec | 0.00% | 0.00MB | 0.00KB/s | 0.00KB/s | 0.00 | 0.00 
| 全部进程 | 23.92% | 0.11MB | 4670.67KB/s | 68.00KB/s | 18.00 | 222.00 
### 基线扫描性能数据图：

![fig](E:\Project\Python_project\graduation_project\PF_test\yunsuo_pf_test\yunsuo\baseline_scan.png)

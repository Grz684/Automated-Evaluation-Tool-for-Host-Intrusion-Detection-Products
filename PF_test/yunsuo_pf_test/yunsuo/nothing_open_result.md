### 无功能开启性能数据：

在仅开启 nothing_open 功能的情况下，各进程组件性能测试结果如下（测试时间300s）：

| 进程名 | vcpu平均占用率 | RSS平均大小 | 读数据平均速率 | 写数据平均速率 | IOPS平均值 | network_io平均值 
| --- | --- | --- | --- | --- | --- | --- |
| wsssr_defence_service | 1.28% | 0.06MB | 40.02KB/s | 1.65KB/s | 5.33 | 19.03 
| wsssr_defence_daemon | 0.08% | 0.00MB | 0.00KB/s | 0.05KB/s | 0.03 | 0.73 
| lbaselinescan | 0.00% | 0.00MB | 0.00KB/s | 0.00KB/s | 0.00 | 0.00 
| icsfilesec | 0.00% | 0.00MB | 0.00KB/s | 0.00KB/s | 0.00 | 0.00 
| 全部进程 | 1.36% | 0.07MB | 40.02KB/s | 1.70KB/s | 5.37 | 19.77 

| 进程名 | vcpu最高占用率 | RSS最大值 | 读数据最高速率 | 写数据最高速率 | IOPS最大值 | network_io最大值 
| --- | --- | --- | --- | --- | --- | --- |
| wsssr_defence_service | 7.33% | 0.13MB | 1786.67KB/s | 72.00KB/s | 30.00 | 222.00 
| wsssr_defence_daemon | 2.00% | 0.01MB | 0.00KB/s | 4.00KB/s | 1.00 | 9.00 
| lbaselinescan | 0.00% | 0.00MB | 0.00KB/s | 0.00KB/s | 0.00 | 0.00 
| icsfilesec | 0.00% | 0.00MB | 0.00KB/s | 0.00KB/s | 0.00 | 0.00 
| 全部进程 | 9.33% | 0.13MB | 1786.67KB/s | 72.00KB/s | 30.00 | 222.00 
### 无功能开启性能数据图：

![fig](E:\Project\Python_project\graduation_project\PF_test\yunsuo_pf_test\yunsuo\nothing_open.png)

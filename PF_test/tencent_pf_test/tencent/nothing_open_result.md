### 无功能开启性能数据：

在仅开启 nothing_open 功能的情况下，各进程组件性能测试结果如下（测试时间300s）：

| 进程名 | vcpu平均占用率 | RSS平均大小 | 读数据平均速率 | 写数据平均速率 | IOPS平均值 | network_io平均值 
| --- | --- | --- | --- | --- | --- | --- |
| YDService | 2.14% | 0.05MB | 0.54KB/s | 2.24KB/s | 2.63 | 0.33 
| YDLive | 0.04% | 0.00MB | 0.00KB/s | 0.00KB/s | 0.00 | 0.00 
| YDPython | 0.00% | 0.00MB | 0.00KB/s | 0.00KB/s | 0.00 | 0.00 
| YDUtils | 0.00% | 0.00MB | 0.00KB/s | 0.00KB/s | 0.00 | 0.00 
| 全部进程 | 2.18% | 0.05MB | 0.54KB/s | 2.24KB/s | 2.63 | 0.33 

| 进程名 | vcpu最高占用率 | RSS最大值 | 读数据最高速率 | 写数据最高速率 | IOPS最大值 | network_io最大值 
| --- | --- | --- | --- | --- | --- | --- |
| YDService | 4.00% | 0.06MB | 42.38KB/s | 9.33KB/s | 3.00 | 4.00 
| YDLive | 0.33% | 0.01MB | 0.00KB/s | 0.00KB/s | 0.00 | 0.00 
| YDPython | 0.00% | 0.00MB | 0.00KB/s | 0.00KB/s | 0.00 | 0.00 
| YDUtils | 0.00% | 0.00MB | 0.00KB/s | 0.00KB/s | 0.00 | 0.00 
| 全部进程 | 4.00% | 0.07MB | 42.38KB/s | 9.33KB/s | 3.00 | 4.00 
### 无功能开启性能数据图：

![fig](E:\Project\Python_project\graduation_project\PF_test\tencent_pf_test\tencent\nothing_open.png)

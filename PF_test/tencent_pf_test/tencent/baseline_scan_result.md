### 基线扫描性能数据：

在仅开启 baseline_scan 功能的情况下，各进程组件性能测试结果如下（测试时间300s）：

| 进程名 | vcpu平均占用率 | RSS平均大小 | 读数据平均速率 | 写数据平均速率 | IOPS平均值 | network_io平均值 
| --- | --- | --- | --- | --- | --- | --- |
| YDService | 2.23% | 0.06MB | 7.34KB/s | 14.27KB/s | 2.63 | 0.93 
| YDLive | 0.06% | 0.00MB | 1.64KB/s | 0.01KB/s | 0.03 | 0.10 
| YDPython | 0.73% | 0.01MB | 4.78KB/s | 0.13KB/s | 0.27 | 0.00 
| YDUtils | 0.00% | 0.00MB | 0.00KB/s | 0.00KB/s | 0.00 | 0.00 
| 全部进程 | 3.02% | 0.07MB | 13.76KB/s | 14.41KB/s | 2.93 | 1.03 

| 进程名 | vcpu最高占用率 | RSS最大值 | 读数据最高速率 | 写数据最高速率 | IOPS最大值 | network_io最大值 
| --- | --- | --- | --- | --- | --- | --- |
| YDService | 4.67% | 0.06MB | 734.67KB/s | 825.33KB/s | 3.00 | 12.00 
| YDLive | 0.67% | 0.01MB | 164.00KB/s | 1.33KB/s | 1.00 | 3.00 
| YDPython | 8.61% | 0.03MB | 111.26KB/s | 2.67KB/s | 6.00 | 0.00 
| YDUtils | 0.00% | 0.00MB | 0.00KB/s | 0.00KB/s | 0.00 | 0.00 
| 全部进程 | 11.26% | 0.09MB | 734.67KB/s | 825.33KB/s | 9.00 | 12.00 
### 基线扫描性能数据图：

![fig](E:\Project\Python_project\graduation_project\PF_test\tencent_pf_test\tencent\baseline_scan.png)

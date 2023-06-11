### 基线扫描性能数据：

在仅开启 baseline_scan 功能的情况下，各进程组件性能测试结果如下（测试时间300s）：

| 进程名 | vcpu平均占用率 | RSS平均大小 | 读数据平均速率 | 写数据平均速率 | IOPS平均值 | network_io平均值 
| --- | --- | --- | --- | --- | --- | --- |
| hostwatch | 0.03% | 0.00MB | 0.00KB/s | 0.03KB/s | 0.03 | 0.10 
| hostguard | 1.83% | 0.07MB | 13.61KB/s | 1.83KB/s | 0.37 | 6.77 
| python | 0.06% | 0.00MB | 0.00KB/s | 0.27KB/s | 0.00 | 0.00 
| 全部进程 | 1.92% | 0.07MB | 13.61KB/s | 2.12KB/s | 0.40 | 6.87 

| 进程名 | vcpu最高占用率 | RSS最大值 | 读数据最高速率 | 写数据最高速率 | IOPS最大值 | network_io最大值 
| --- | --- | --- | --- | --- | --- | --- |
| hostwatch | 0.33% | 0.01MB | 0.00KB/s | 2.67KB/s | 1.00 | 3.00 
| hostguard | 4.67% | 0.07MB | 1134.67KB/s | 153.33KB/s | 1.00 | 157.00 
| python | 1.00% | 0.02MB | 0.00KB/s | 2.67KB/s | 0.00 | 0.00 
| 全部进程 | 5.34% | 0.10MB | 1134.67KB/s | 153.33KB/s | 1.00 | 157.00 
### 基线扫描性能数据图：

![fig](E:\Project\Python_project\graduation_project\PF_test\hss_pf_test\hss\baseline_scan.png)

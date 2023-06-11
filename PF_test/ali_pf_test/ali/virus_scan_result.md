### 病毒扫描性能数据：

在仅开启 virus_scan 功能的情况下，各进程组件性能测试结果如下（测试时间300s）：

| 进程名 | vcpu平均占用率 | RSS平均大小 | 读数据平均速率 | 写数据平均速率 | IOPS平均值 | network_io平均值 
| --- | --- | --- | --- | --- | --- | --- |
| AliDetect | 1.79% | 0.02MB | 0.07KB/s | 0.37KB/s | 0.17 | 1.50 
| AliYunDunUpdate | 0.13% | 0.00MB | 0.00KB/s | 0.00KB/s | 0.00 | 0.00 
| AliYunDun | 1.01% | 0.01MB | 0.00KB/s | 0.03KB/s | 0.00 | 33.60 
| AliYunDunMonitor | 3.09% | 0.04MB | 0.08KB/s | 0.03KB/s | 0.10 | 4.30 
| AliSecureCheckAdvanced | 1.74% | 0.02MB | 103.01KB/s | 0.82KB/s | 0.60 | 1.27 
| 全部进程 | 7.76% | 0.09MB | 103.15KB/s | 1.24KB/s | 0.87 | 40.67 

| 进程名 | vcpu最高占用率 | RSS最大值 | 读数据最高速率 | 写数据最高速率 | IOPS最大值 | network_io最大值 
| --- | --- | --- | --- | --- | --- | --- |
| AliDetect | 8.33% | 0.02MB | 6.67KB/s | 2.67KB/s | 5.00 | 45.00 
| AliYunDunUpdate | 1.00% | 0.00MB | 0.00KB/s | 0.00KB/s | 0.00 | 0.00 
| AliYunDun | 1.67% | 0.01MB | 0.00KB/s | 2.67KB/s | 0.00 | 120.00 
| AliYunDunMonitor | 4.67% | 0.04MB | 8.00KB/s | 1.33KB/s | 3.00 | 129.00 
| AliSecureCheckAdvanced | 9.00% | 0.04MB | 1025.33KB/s | 69.33KB/s | 14.00 | 38.00 
| 全部进程 | 13.67% | 0.11MB | 1025.33KB/s | 69.33KB/s | 14.00 | 154.00 
### 病毒扫描性能数据图：

![fig](E:\Project\Python_project\graduation_project\PF_test\ali_pf_test\ali\virus_scan.png)

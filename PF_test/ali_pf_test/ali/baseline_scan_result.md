### 基线扫描性能数据：

在仅开启 baseline_scan 功能的情况下，各进程组件性能测试结果如下（测试时间300s）：

| 进程名 | vcpu平均占用率 | RSS平均大小 | 读数据平均速率 | 写数据平均速率 | IOPS平均值 | network_io平均值 
| --- | --- | --- | --- | --- | --- | --- |
| AliDetect | 1.80% | 0.02MB | 0.07KB/s | 0.33KB/s | 0.00 | 1.50 
| AliYunDunUpdate | 0.13% | 0.00MB | 0.00KB/s | 0.00KB/s | 0.00 | 0.00 
| AliYunDun | 0.81% | 0.01MB | 0.00KB/s | 0.01KB/s | 0.00 | 7.37 
| AliYunDunMonitor | 3.35% | 0.03MB | 0.07KB/s | 0.03KB/s | 0.03 | 0.00 
| AliSecureCheckAdvanced | 0.19% | 0.00MB | 0.52KB/s | 0.38KB/s | 0.33 | 0.43 
| 全部进程 | 6.27% | 0.06MB | 0.65KB/s | 0.74KB/s | 0.37 | 9.30 

| 进程名 | vcpu最高占用率 | RSS最大值 | 读数据最高速率 | 写数据最高速率 | IOPS最大值 | network_io最大值 
| --- | --- | --- | --- | --- | --- | --- |
| AliDetect | 8.33% | 0.02MB | 6.67KB/s | 4.00KB/s | 0.00 | 45.00 
| AliYunDunUpdate | 0.67% | 0.00MB | 0.00KB/s | 0.00KB/s | 0.00 | 0.00 
| AliYunDun | 1.67% | 0.01MB | 0.00KB/s | 1.33KB/s | 0.00 | 152.00 
| AliYunDunMonitor | 8.00% | 0.03MB | 5.33KB/s | 1.33KB/s | 1.00 | 0.00 
| AliSecureCheckAdvanced | 6.00% | 0.02MB | 30.67KB/s | 36.00KB/s | 6.00 | 13.00 
| 全部进程 | 17.67% | 0.08MB | 32.00KB/s | 37.33KB/s | 6.00 | 152.00 
### 基线扫描性能数据图：

![fig](E:\Project\Python_project\graduation_project\PF_test\ali_pf_test\ali\baseline_scan.png)

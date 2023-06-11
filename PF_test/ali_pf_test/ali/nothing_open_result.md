### 无功能开启性能数据：

在仅开启 nothing_open 功能的情况下，各进程组件性能测试结果如下（测试时间300s）：

| 进程名 | vcpu平均占用率 | RSS平均大小 | 读数据平均速率 | 写数据平均速率 | IOPS平均值 | network_io平均值 
| --- | --- | --- | --- | --- | --- | --- |
| AliDetect | 1.61% | 0.02MB | 0.00KB/s | 0.37KB/s | 0.00 | 0.00 
| AliYunDunUpdate | 0.13% | 0.00MB | 0.00KB/s | 0.00KB/s | 0.00 | 0.00 
| AliYunDun | 0.74% | 0.01MB | 0.00KB/s | 0.00KB/s | 0.00 | 0.50 
| AliYunDunMonitor | 3.13% | 0.03MB | 0.00KB/s | 2.63KB/s | 0.00 | 0.00 
| AliSecureCheckAdvanced | 0.00% | 0.00MB | 0.00KB/s | 0.00KB/s | 0.00 | 0.00 
| 全部进程 | 5.61% | 0.06MB | 0.00KB/s | 2.99KB/s | 0.00 | 0.50 

| 进程名 | vcpu最高占用率 | RSS最大值 | 读数据最高速率 | 写数据最高速率 | IOPS最大值 | network_io最大值 
| --- | --- | --- | --- | --- | --- | --- |
| AliDetect | 4.33% | 0.02MB | 0.00KB/s | 4.00KB/s | 0.00 | 0.00 
| AliYunDunUpdate | 0.67% | 0.00MB | 0.00KB/s | 0.00KB/s | 0.00 | 0.00 
| AliYunDun | 1.00% | 0.01MB | 0.00KB/s | 0.00KB/s | 0.00 | 5.00 
| AliYunDunMonitor | 6.00% | 0.03MB | 0.00KB/s | 265.33KB/s | 0.00 | 0.00 
| AliSecureCheckAdvanced | 0.00% | 0.00MB | 0.00KB/s | 0.00KB/s | 0.00 | 0.00 
| 全部进程 | 8.33% | 0.06MB | 0.00KB/s | 265.33KB/s | 0.00 | 5.00 
### 无功能开启性能数据图：

![fig](E:\Project\Python_project\graduation_project\PF_test\ali_pf_test\ali\nothing_open.png)

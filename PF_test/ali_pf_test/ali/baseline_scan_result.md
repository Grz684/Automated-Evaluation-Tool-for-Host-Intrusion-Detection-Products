### 基线扫描性能数据：

在仅开启 baseline_scan 功能的情况下，各进程组件性能测试结果如下（测试时间19s）：

| 进程名 | vcpu平均占用率 | 驻留物理内存平均大小（RSS） | 读数据平均速率 | 写数据平均速率 
| --- | --- | --- | --- | --- |
| AliYunDunUpdate | 0.16% | 1.02MB | 0.00KB/s | 0.00KB/s 
| AliYunDun | 1.16% | 11.94MB | 0.00KB/s | 0.00KB/s 
| AliYunDunMonitor | 8.10% | 30.18MB | 0.00KB/s | 0.00KB/s 
| AliSecGuard | 0.05% | 0.35MB | 0.00KB/s | 0.00KB/s 
| AliHips | 0.26% | 5.84MB | 0.00KB/s | 0.21KB/s 
| AliNet | 0.11% | 1.08MB | 0.00KB/s | 0.00KB/s 
| AliSecureCheckAdvanced | 2.37% | 15.23MB | 0.00KB/s | 5.68KB/s 
| 全部进程 | 12.21% | 65.65MB | 0.00KB/s | 5.89KB/s 
### 基线扫描性能数据图：

![vul_scan_fig](E:\Project\Python_project\graduation_project\PF_test\ali_pf_test\ali\baseline_scan.png)

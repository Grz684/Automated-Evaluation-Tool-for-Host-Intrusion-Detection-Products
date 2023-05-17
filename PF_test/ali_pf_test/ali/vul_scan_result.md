### 漏洞扫描性能数据：

在仅开启 vul_scan 功能的情况下，各进程组件性能测试结果如下（测试时间67s）：

| 进程名 | vcpu平均占用率 | 驻留物理内存平均大小（RSS） | 读数据平均速率 | 写数据平均速率 
| --- | --- | --- | --- | --- |
| AliYunDunUpdate | 0.13% | 0.87MB | 0.00KB/s | 0.00KB/s 
| AliYunDun | 1.06% | 11.71MB | 0.00KB/s | 0.06KB/s 
| AliYunDunMonitor | 4.92% | 29.10MB | 0.00KB/s | 0.18KB/s 
| AliSecGuard | 0.09% | 0.60MB | 0.00KB/s | 0.00KB/s 
| AliHips | 0.25% | 5.52MB | 0.00KB/s | 0.30KB/s 
| AliNet | 0.13% | 1.38MB | 0.00KB/s | 0.00KB/s 
| AliSecureCheckAdvanced | 2.13% | 22.44MB | 0.00KB/s | 25.19KB/s 
| 全部进程 | 8.73% | 71.62MB | 0.00KB/s | 25.73KB/s 
### 漏洞扫描性能数据图：

![vul_scan_fig](E:\Project\Python_project\graduation_project\PF_test\ali_pf_test\ali\vul_scan.png)

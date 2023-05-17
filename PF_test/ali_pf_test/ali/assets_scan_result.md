### 资产扫描性能数据：

在仅开启 assets_scan 功能的情况下，各进程组件性能测试结果如下（测试时间78s）：

| 进程名 | vcpu平均占用率 | 驻留物理内存平均大小（RSS） | 读数据平均速率 | 写数据平均速率 
| --- | --- | --- | --- | --- |
| AliYunDunUpdate | 0.14% | 0.91MB | 0.00KB/s | 0.00KB/s 
| AliYunDun | 1.04% | 12.64MB | 0.00KB/s | 0.26KB/s 
| AliYunDunMonitor | 5.11% | 29.04MB | 0.00KB/s | 0.10KB/s 
| AliSecGuard | 0.08% | 0.52MB | 0.00KB/s | 0.00KB/s 
| AliHips | 0.27% | 5.45MB | 0.00KB/s | 0.26KB/s 
| AliNet | 0.12% | 1.19MB | 0.00KB/s | 0.00KB/s 
| AliSecureCheckAdvanced | 4.69% | 27.39MB | 0.00KB/s | 22.77KB/s 
| 全部进程 | 11.45% | 77.14MB | 0.00KB/s | 23.38KB/s 
### 资产扫描性能数据图：

![vul_scan_fig](E:\Project\Python_project\graduation_project\PF_test\ali_pf_test\ali\assets_scan.png)

### 资产扫描性能数据：

在仅开启 assets_scan 功能的情况下，各进程组件性能测试结果如下（测试时间20s）：

| 进程名 | vcpu平均占用率 | RSS平均大小 | 读数据平均速率 | 写数据平均速率 | IOPS平均值 | network_io平均值 
| --- | --- | --- | --- | --- | --- | --- |
| wsssr_defence_service | 1.25% | 45.20MB | 0.00KB/s | 1.60KB/s | 1.25 | 2.30 
| wsssr_defence_daemon | 0.05% | 0.50MB | 0.00KB/s | 0.00KB/s | 0.05 | 0.03 
| 全部进程 | 1.30% | 45.70MB | 0.00KB/s | 1.60KB/s | 1.30 | 2.33 
| 进程名 | vcpu最高占用率 | RSS最大值 | 读数据最高速率 | 写数据最高速率 | IOPS最大值 | network_io最大值 
| --- | --- | --- | --- | --- | --- | --- |
| wsssr_defence_service | 4.00% | 82.18MB | 0.00KB/s | 32.00KB/s | 4.00 | 4.19 
| wsssr_defence_daemon | 1.00% | 3.35MB | 0.00KB/s | 0.00KB/s | 1.00 | 0.17 
| 全部进程 | 4.00% | 85.53MB | 0.00KB/s | 32.00KB/s | 4.00 | 4.36 
### 资产扫描性能数据图：

![fig](E:\Project\Python_project\graduation_project\PF_test\hisec_pf_test\hisec\assets_scan.png)

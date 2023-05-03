### 资产扫描性能数据：

在仅开启 assets_scan 功能的情况下，各进程组件性能测试结果如下（测试时间163s）：

| 进程名 | vcpu平均占用率 | 驻留物理内存平均大小（RSS） | 读数据平均速率 | 写数据平均速率 
| --- | --- | --- | --- | --- |
| wsssr_defence_service | 4.19% | 89.32MB | 75.43KB/s | 6.06KB/s 
| wsssr_defence_daemon | 0.07% | 0.57MB | 0.00KB/s | 0.05KB/s 
| lbaselinescan | 4.10% | 4.64MB | 71.24KB/s | 5.10KB/s 
| 全部进程 | 8.36% | 94.53MB | 146.67KB/s | 11.21KB/s 
### 资产扫描性能数据图：

![vul_scan_fig](E:\Project\Python_project\graduation_project\PF_test\yunsuo_pf_test\yunsuo\assets_scan.png)
### 资产扫描结果：

共扫描到1348项资产，资产分类情况为：

资产收集-PROCESS: 219

资产收集-NETLINK: 7

资产收集-USER: 34

资产收集-INSTALLPACKAGE: 695

资产收集-AUTORUNSERV: 60

资产收集-CRON: 10

资产收集-SYSMODULE: 84

资产收集-SYSTEM: 1

资产收集-REGAUTOSTART: 0

资产收集-SERVICE: 3

资产收集-第三方jar: 0

资产收集-SOFTAPP: 11

资产收集-WBEFRAME: 0

资产收集-JAR: 0

资产收集-CERT: 0

资产收集-DATABASE: 0

资产收集-WEB: 0

资产收集-WEBSERVER: 0

资产收集-PORT: 4

资产收集-服务器: 1

资产收集-进程资产: 219

资产收集-web
应用资产: 0

主机发现扫描: 0


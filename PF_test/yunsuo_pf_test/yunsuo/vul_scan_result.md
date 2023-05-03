### 漏洞扫描性能数据：

在仅开启 vul_scan 功能的情况下，各进程组件性能测试结果如下（测试时间318s）：

| 进程名 | vcpu平均占用率 | 驻留物理内存平均大小（RSS） | 读数据平均速率 | 写数据平均速率 
| --- | --- | --- | --- | --- |
| wsssr_defence_service | 2.61% | 67.27MB | 396.69KB/s | 1.71KB/s 
| wsssr_defence_daemon | 0.09% | 0.53MB | 0.00KB/s | 0.04KB/s 
| lbaselinescan | 3.18% | 6.48MB | 390.09KB/s | 0.96KB/s 
| 全部进程 | 5.88% | 74.29MB | 786.79KB/s | 2.70KB/s 
### 漏洞扫描性能数据图：

![vul_scan_fig](E:\Project\Python_project\graduation_project\PF_test\yunsuo_pf_test\yunsuo\vul_scan.png)
### 漏洞扫描结果：

共扫描到10个漏洞，漏洞cve编号分别为：

CVE-2022-25636 (Linux kernel内核本地权限提升漏洞(CVE-2022-25636))

CVE-2022-27666 (Linux kernel内核本地权限提升漏洞(CVE-2022-27666))

CVE-2021-3493 (Linux kernel 本地提权漏洞（CVE-2021-3493）)

CVE-2021-22555 (Linux kernel netfilter本地提权漏洞(CVE-2021-22555))

CVE-2019-19241 (Linux kernel提权漏洞(CVE-2019-19241))

CVE-2021-33909 (Linux kernel seq_file本地提权漏洞(CVE-2021-33909))

CVE-2022-25258,CVE-2022-25265,CVE-2022-25375 (Linux kernel多个安全漏洞(CVE-2022-25265、CVE-2022-25258、CVE-2022-25375))

CVE-2022-0778 (OpenSSL拒绝服务漏洞(CVE-2022-0778))

CVE-2022-34918 (Linux Kernel 权限提升漏洞(CVE-2022-34918))

CVE-2022-2639 (Linux Kernel 权限提升漏洞(CVE-2022-2639))


### 漏洞扫描性能数据：

在仅开启 vul_scan 功能的情况下，各进程组件性能测试结果如下（测试时间394s）：

| 进程名 | vcpu平均占用率 | 驻留物理内存平均大小（RSS） | 读数据平均速率 | 写数据平均速率 
| --- | --- | --- | --- | --- |
| YDService | 2.50% | 70.17MB | 30.32KB/s | 16.35KB/s 
| YDLive | 0.05% | 0.56MB | 0.00KB/s | 0.00KB/s 
| YDPython | 4.42% | 32.34MB | 28.22KB/s | 3.14KB/s 
| 全部进程 | 6.96% | 103.06MB | 58.55KB/s | 19.49KB/s 
### 漏洞扫描性能数据图：

![vul_scan_fig](E:\Project\Python_project\graduation_project\PF_test\tencent_pf_test\tencent\vul_scan.png)
### 漏洞扫描结果：

共扫描到45个漏洞，漏洞cve编号分别为：

CVE-2023-1264 (Vim 代码问题漏洞(CVE-2023-1264))

CVE-2023-1175 (Vim 安全漏洞(CVE-2023-1175))

CVE-2023-1170 (Vim 安全漏洞(CVE-2023-1170))

CVE-2023-24329 (Python urllib.parse 安全特性绕过漏洞（CVE-2023-24329）)

CVE-2022-45141 (Samba 安全漏洞(CVE-2022-45141))

CVE-2022-38090 (Intel(R) Processors 信息泄露漏洞（CVE-2022-38090）)

CVE-2022-33972 (3rd Generation Intel(R) Xeon(R) Scalable Processors 信息泄露漏洞（CVE-2022-33972）)

CVE-2022-33196 (Intel Software Guard Extensions 权限提升漏洞（CVE-2022-33196）)

CVE-2022-21216 (Intel(R) Atom® and Intel® Xeon® Scalable Processors 权限提升漏洞（CVE-2022-21216）)

CVE-2023-23916 (curl 拒绝服务漏洞(CVE-2023-23916))

CVE-2023-0286 (OpenSSL拒绝服务漏洞（CVE-2023-0286）)

CVE-2023-0215 (OpenSSL 拒绝服务漏洞（CVE-2023-0215）)

CVE-2022-4450 (OpenSSL拒绝服务漏洞（CVE-2022-4450）)

CVE-2022-4304 (OpenSSL 安全漏洞（CVE-2022-4304）)

CVE-2022-37434 (zlib 安全漏洞 (CVE-2022-37434))

CVE-2022-32221 (curl 安全漏洞（CVE-2022-32221）)

CVE-2022-41903 (Git 代码执行漏洞（CVE-2022-41903）)

CVE-2022-23521 (Git 代码执行漏洞（CVE-2022-23521）)

CVE-2022-1292 (OpenSSL 操作系统命令注入漏洞 (CVE-2022-1292))

CVE-2021-3711 (OpenSSL 缓冲区错误漏洞（CVE-2021-3711）)

CVE-2022-2526 (Systemd 释放后重用漏洞（CVE-2022-2526）)

CVE-2021-22901 (Haxx curl 资源管理错误漏洞 (CVE-2021-22901))

CVE-2022-1271 (GNU Gzip 输入验证错误漏洞（CVE-2022-1271）)

CVE-2022-41973 (device-mapper-multipath 安全漏洞（CVE-2022-41973）)

CVE-2022-41974 (device-mapper-multipath 安全漏洞（CVE-2022-41974）)

CVE-2022-40284 (NTFS-3G 缓冲区溢出漏洞(CVE-2022-40284))

CVE-2021-44731 (Snapd 竞争条件问题漏洞（CVE-2021-44731）)

CVE-2022-40304 (libxml2 安全漏洞（CVE-2022-40304）)

CVE-2022-3328 (snapd 本地权限提升漏洞（CVE-2022-3328）)

CVE-2022-24903 (RSyslog 缓冲区溢出漏洞（CVE-2022-24903）)

CVE-2022-40303 (libxml2 拒绝服务漏洞（CVE-2022-40303）)

CVE-2022-29187 (Github Git 安全漏洞（CVE-2022-29187）)

CVE-2023-22809 (Sudo 安全特性绕过漏洞（CVE-2023-22809）)

CVE-2022-47016 (tmux 代码问题漏洞（CVE-2022-47016）)

CVE-2021-3712 (OpenSSL 缓冲区错误漏洞 (CVE-2021-3712))

CVE-2022-0778 (OpenSSL BN_mod_sqrt 拒绝服务漏洞 (CVE-2022-0778))

CVE-2022-1473 (OpenSSL 安全漏洞 (CVE-2022-1473))

CVE-2022-2068 (OpenSSL 安全漏洞 (CVE-2022-2068))

CVE-2022-2097 (OpenSSL 加密问题漏洞 (CVE-2022-2097))

CVE-2021-22876 (HAXX libcurl 信息泄露漏洞 (CVE-2021-22876))

CVE-2022-27776 (curl 信息泄露漏洞（CVE-2022-27776）)

CVE-2022-27774 (curl 信息泄露漏洞（CVE-2022-27774）)

CVE-2021-22898 (HAXX libcurl 安全漏洞 (CVE-2021-22898))

CVE-2022-25636 (linux 内核本地权限提升漏洞（CVE-2022-25636）)

CVE-2021-4034 (Linux polkit本地权限提升漏洞（CVE-2021-4034）)


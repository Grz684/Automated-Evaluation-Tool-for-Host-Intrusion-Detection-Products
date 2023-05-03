### 基线扫描性能数据：

在仅开启 baseline_scan 功能的情况下，各进程组件性能测试结果如下（测试时间349s）：

| 进程名 | vcpu平均占用率 | 驻留物理内存平均大小（RSS） | 读数据平均速率 | 写数据平均速率 
| --- | --- | --- | --- | --- |
| YDService | 2.57% | 70.63MB | 2.20KB/s | 5.71KB/s 
| YDLive | 0.05% | 0.54MB | 0.00KB/s | 0.00KB/s 
| YDPython | 0.97% | 11.58MB | 2.12KB/s | 0.77KB/s 
| 全部进程 | 3.58% | 82.74MB | 4.32KB/s | 6.48KB/s 
### 基线扫描性能数据图：

![vul_scan_fig](E:\Project\Python_project\graduation_project\PF_test\tencent_pf_test\tencent\baseline_scan.png)
### 基线检测结果

共检测CIS基线151项，基线检测结果为：

| ID | item_name | is_passed_check |
| --- | --- | --- |
| 1 | 确保ssh的tcp转发功能是关闭的 | no |
| 2 | 确保配置/etc/group的权限 | yes |
| 3 | 确保已配置/etc/shadow的权限 | yes |
| 4 | 确保禁用freevxfs文件系统的挂载 | no |
| 5 | 确保/home存在单独的分区 | no |
| 6 | 禁用自动挂载 | yes |
| 7 | 确保SSH访问受到限制 | no |
| 8 | 确保在/etc/issue.net上配置了权限 | yes |
| 9 | 确保收集了未成功的未经授权的文件访问尝试 | no |
| 10 | 确保SSH LoginGraceTime设置为一分钟或更短 | no |
| 11 | 确保密码哈希算法为SHA-512 | yes |
| 12 | 确保/var/log存在单独的分区 | no |
| 13 | 确保未启用rsync服务 | no |
| 14 | 禁用IPv6 | no |
| 15 | 确保仅使用强密码 | yes |
| 16 | 确保已配置GDM登录横幅 | yes |
| 17 | 确保未安装X Window系统 | yes |
| 18 | 确保未安装LDAP客户端 | yes |
| 19 | 确保禁用了数据包重定向发送 | no |
| 20 | 确保在/var/tmp分区上设置了noexec选项 | yes |
| 21 | 确保收集了会话启动信息 | no |
| 22 | 确保sudo命令使用pty | no |
| 23 | 确保已配置SSH空闲超时间隔 | no |
| 24 | 确保默认用户shell超时为900秒或更短 | no |
| 25 | 确保不存在world-writable文件 | no |
| 26 | 确保/var存在单独的分区 | yes |
| 27 | 确保已配置/etc/issue的权限 | yes |
| 28 | 确保未安装rsh客户端 | yes |
| 29 | 确保收集了修改日期和时间信息的事件 | no |
| 30 | 确保对su命令的访问受到限制 | no |
| 31 | 确保禁用jffs2文件系统的挂载 | no |
| 32 | 确保未启用NFS | yes |
| 33 | 确保不接受IPv6路由器通告 | no |
| 34 | 确保审核日志不会自动删除 | no |
| 35 | 确保收集了登录和注销事件 | no |
| 36 | 确保限制密码重用 | no |
| 37 | 确保已禁用cramfs文件系统的挂载 | no |
| 38 | 确保在/tmp分区上设置nodev选项 | yes |
| 39 | 确保已配置/etc/motd的权限 | yes |
| 40 |  确保未启用DHCP服务器 | yes |
| 41 | 确保禁用hfsplus文件系统的挂载 | no |
| 42 | 确保配置了bootloader配置的权限 | no |
| 43 | 确保将日记记录配置为压缩大日志文件 | no |
| 44 | 确保在引导加载程序配置中启用了AppArmor | no |
| 45 | 确保/var/tmp存在单独的分区 | no |
| 46 | 确保已安装AIDE | no |
| 47 | 确保SSH PermitUserEnvironment已禁用 | yes |
| 48 | 确保配置/etc/shadow-的权限 | yes |
| 49 | 确保成功收集文件系统挂载 | no |
| 50 | 确保配置/etc/crontab上的权限 | no |
| 51 | 确保已配置SSH警告标语 | no |
| 52 | 确保禁用prelink | no |
| 53 | 确保未启用FTP服务 | no |
| 54 | 确保未启用HTTP代理服务 | yes |
| 55 | 确保收集了修改系统的强制访问控制的事件 | no |
| 56 | 确保sudo日志文件存在 | no |
| 57 | 确保密码字段不为空 | yes |
| 58 | 确保禁用hfs文件系统的挂载 | no |
| 59 | 确保audit_backlog_limit已配置 | no |
| 60 | 确保收集了修改系统网络环境的事件 | no |
| 61 | 确保仅使用强大的密钥交换算法 | yes |
| 62 | 确保在/etc/group-上配置了权限 | yes |
| 63 | 确保在/tmp分区上设置了noexec选项 | yes |
| 64 | 禁用USB存储 | no |
| 65 | 确保定期检查文件系统完整性 | no |
| 66 | 确保已安装auditd | no |
| 67 | 确保启用了地址空间布局随机化（ASLR） | yes |
| 68 | 确保不接受源路由数据包 | no |
| 69 | 确保启用了cron守护程序 | yes |
| 70 | 确保收集了任意访问控制权限修改事件 | no |
| 71 | 确保在审核日志已满时禁用系统 | no |
| 72 | 确保将日记记录配置为将日志文件写入永久磁盘 | no |
| 73 | 确保已配置/etc/cron.daily的权限 | no |
| 74 | 确保已安装sudo | yes |
| 75 | 确保在所有可写目录上设置了粘性位 | no |
| 76 | 确保未安装NIS客户端 | yes |
| 77 | 确保启用了TCP SYN Cookies | no |
| 78 | 确保启用对在auditd之前启动的进程的审计 | no |
| 79 | 确保启用了SSH IgnoreRhosts | yes |
| 80 | 确保配置/etc/passwd的权限 | yes |
| 81 | 确保未安装IMAP POP3服务器 | yes |
| 82 | 确保未安装RPC客户端 | yes |
| 83 | 确保禁用RDS | no |
| 84 | 确保未启用Samba | no |
| 85 | 确保禁用DCCP | no |
| 86 | 确保在 /dev/shm 分区上设置 nodev 选项 | yes |
| 87 | 确保在 /dev/shm 分区上设置了 nosuid 选项 | yes |
| 88 | 确保已配置ntp | no |
| 89 | 确保未启用DNS服务 | yes |
| 90 | 确保已启用SSH PAM | yes |
| 91 | 确保禁用IP转发 | yes |
| 92 | 确保已配置审核日志存储大小 | yes |
| 93 | 确保已配置/etc/cron.weekly的权限 | no |
| 94 | 确保已配置失败密码尝试的锁定 | no |
| 95 | 确保在/home分区上设置nodev选项 | yes |
| 96 | 确保正在使用时间同步 | yes |
| 97 | 确保禁用SSH X11转发 | no |
| 98 | 确保已配置SSH MaxStartups | no |
| 99 | 确保已配置/tmp | no |
| 100 | 确保将rsyslog配置为将日志发送到远程日志主机 | no |
| 101 | 确保已安装AppArmor | yes |
| 102 | 确保不接受ICMP重定向 | no |
| 103 | 确保系统管理范围（sudoers）更改的收集 | no |
| 104 | 确保配置/etc/ssh/sshd_config的权限 | no |
| 105 | 确保配置/etc/cron.d上的权限 | no |
| 106 | 确保已配置/etc/gshadow的权限 | yes |
| 107 | 确保不存在任何无主文件或目录 | no |
| 108 | 确保在/tmp分区上设置了nosuid选项 | yes |
| 109 | 确保在/var/tmp分区上设置nodev选项 | yes |
| 110 | 确保未安装telnet客户端 | no |
| 111 | 确保收集了修改用户/组信息的事件 | no |
| 112 | 确保已配置rsyslog默认文件权限 | yes |
| 113 | 确保未启用CUPS | yes |
| 114 | 确保未启用HTTP服务 | yes |
| 115 | 确保未安装talk客户端 | yes |
| 116 | 确保在/var/tmp分区上设置nosuid选项 | yes |
| 117 | 确保/var/log/audit存在单独的分区 | no |
| 118 | 确保未启用LDAP服务器 | yes |
| 119 | 确保已安装rsyslog | yes |
| 120 | 确保仅使用强大的MAC算法 | no |
| 121 | 确保已配置密码创建要求 | no |
| 122 | 确保已配置两次密码更改之间的最短日期 | no |
| 123 | 确保禁止挂载udf文件系统 | no |
| 124 | 确保核心转储受到限制 | no |
| 125 | 确保收集到用户的文件删除事件 | no |
| 126 | 确保审核配置是不变的 | no |
| 127 | 确保SSH MaxAuthTries设置为4或更低 | no |
| 128 | 确保禁用SSH root登录 | no |
| 129 | 确保已禁用SSH空密码登录 | yes |
| 130 | 确保配置/etc/passwd-的权限 | yes |
| 131 | 确保未安装Avahi Server | yes |
| 132 | 确保未启用NIS服务器 | yes |
| 133 | 确保记录了可疑数据包 | no |
| 134 | 确保配置/etc/cron.monthly的权限 | no |
| 135 | 确保不存在未分组的文件或目录 | no |
| 136 | 确保已启用auditd服务 | yes |
| 137 | 确保SSH LogLevel适用 | yes |
| 138 | 确保已禁用SSH基于主机的身份验证 | yes |
| 139 | 确保启用了反向路径过滤 | no |
| 140 | 确保rsyslog服务已启用 | yes |
| 141 | 确保将日记记录配置为将日志发送到rsyslog | no |
| 142 | 确保默认用户umask限制为027或更高 | no |
| 143 | 确保配置/etc/gshadow-的权限 | yes |
| 144 | 确保配置了/dev/shm自动挂载 | yes |
| 145 | 确保不接受secure ICMP重定向 | no |
| 146 | 确保配置/etc/cron.hourly的权限 | no |
| 147 | 确保root是唯一的UID 0帐户 | yes |
| 148 | 确保在 /dev/shm 分区上设置了 noexec 选项 | no |
| 149 | 确保未启用SNMP服务 | yes |
| 150 | 确保禁用TIPC | no |
| 151 | 确保SSH MaxSessions设置为10或更小 | yes |

### 基线扫描性能数据：

在仅开启 baseline_scan 功能的情况下，各进程组件性能测试结果如下（测试时间134s）：

| 进程名 | vcpu平均占用率 | 驻留物理内存平均大小（RSS） | 读数据平均速率 | 写数据平均速率 
| --- | --- | --- | --- | --- |
| wsssr_defence_service | 4.70% | 101.92MB | 0.00KB/s | 2.59KB/s 
| wsssr_defence_daemon | 0.06% | 0.43MB | 0.00KB/s | 0.03KB/s 
| lbaselinescan | 0.94% | 0.55MB | 0.00KB/s | 1.49KB/s 
| 全部进程 | 5.70% | 102.90MB | 0.00KB/s | 4.11KB/s 
### 基线扫描性能数据图：

![vul_scan_fig](E:\Project\Python_project\graduation_project\PF_test\yunsuo_pf_test\yunsuo\baseline_scan.png)
### 基线检测结果

共检测CIS基线204项，基线检测结果为：

| ID | cn_desc | is_passed_check |
| --- | --- | --- |
| 1 | 确保禁止挂载cramfs文件系统 | yes |
| 2 | 确保禁止挂载squashfs文件系统 | yes |
| 3 | 确保禁止挂载udf文件系统 | yes |
| 4 | 确保禁止挂载FAT文件系统 | yes |
| 5 | 确保/tmp存在独立的分区 | no |
| 6 | 确保/tmp分区设置了nodev属性 | no |
| 7 | 确保/tmp分区设置了nosuid属性 | no |
| 8 | 确保/tmp分区设置了noexec属性 | no |
| 9 | 确保/var存在独立的分区 | yes |
| 10 | 确保/var/tmp存在独立的分区 | no |
| 11 | 确保/var/tmp分区设置了nodev属性 | no |
| 12 | 确保/var/tmp分区设置了nosuid属性 | no |
| 13 | 确保/var/tmp分区设置了noexec属性 | no |
| 14 | 确保/var/log存在独立的分区 | no |
| 15 | 确保/var/log/audit存在独立的分区 | no |
| 16 | 确保/home存在独立的分区 | no |
| 17 | 确保/home分区设置了nodev属性 | no |
| 18 | 确保/dev/shm分区设置了nodev属性 | yes |
| 19 | 确保/dev/shm分区设置了nosuid属性 | yes |
| 20 | 确保/dev/shm分区设置了noexec属性 | no |
| 21 | 关闭自动挂载功能 | None |
| 22 | 确保全局gpgcheck已被激活 | no |
| 23 | 确保AIDE程序已安装 | no |
| 24 | 确保开启定期检查文件系统完整性的功能 | no |
| 25 | 确保正确配置bootloader相关文件的权限 | yes |
| 26 | 确保引导程序密码已设置 | no |
| 27 | 确保单用户模式需要身份验证 | no |
| 28 | 限制生成核心转储文件 | no |
| 29 | 确认启用地址空间布局随机化(ASLR) | yes |
| 30 | 确认禁用prelink | yes |
| 31 | 确保在引导加载程序配置中未禁用SELinux | yes |
| 32 | 确保SELinux的状态为Enforcing | no |
| 33 | 确保配置了SELinux的策略 | yes |
| 34 | 确保未安装SETroubleshoot软件包 | yes |
| 35 | 确保未安装MCS Translation Service (mcstrans)软件包 | yes |
| 36 | 确保安装SELinux软件包 | no |
| 37 | 确保安装了更新或安全补丁 | yes |
| 38 | 确保已禁用xinetd服务 | None |
| 39 | 如果启用ntp服务, 确保ntp被正确配置 | yes |
| 40 | 如果启用chrony服务, 确保chrony被正确配置 | yes |
| 41 | 确保X Window System相关软件包未安装 | yes |
| 42 | 确保Avahi服务已禁用 | yes |
| 43 | 确保CUPS服务已禁用 | None |
| 44 | 确保DHCP服务已禁用 | None |
| 45 | 确保LDAP服务已禁用 | None |
| 46 | 确保NFS和RPC服务已禁用 | None |
| 47 | 确保DNS服务已禁用 | None |
| 48 | 确保FTP服务已禁用 | None |
| 49 | 确保HTTP服务已禁用 | None |
| 50 | 确保IMAP和POP3服务已禁用 | None |
| 51 | 确保SAMBA服务已禁用 | None |
| 52 | 确保HTTP Proxy服务已禁用 | None |
| 53 | 确保SNMP服务已禁用 | None |
| 54 | 确保邮件传输代理配置为仅本地模式 | no |
| 55 | 确保NIS服务已禁用 | None |
| 56 | 确保rsh (rsh,rlogin,rexec) 服务已禁用 | yes |
| 57 | 确保telnet服务已禁用 | None |
| 58 | 确保tftp服务已禁用 | yes |
| 59 | 确保rsync服务已禁用 | None |
| 60 | 确保NIS客户端未安装 | no |
| 61 | 确保rsh客户端未安装 | no |
| 62 | 确保talk客户端未安装 | no |
| 63 | 确保telnet客户端未安装 | no |
| 64 | 确保LDAP客户端未安装 | no |
| 65 | 确保IP转发已禁用 | yes |
| 66 | 确保数据包重定向发送已禁用 | no |
| 67 | 确保不接受源路由数据包 | no |
| 68 | 确保不接受ICMP重定向 | no |
| 69 | 确保不接受安全的ICMP重定向 | no |
| 70 | 确保记录可疑数据包 | no |
| 71 | 确保ICMP广播请求被忽略 | yes |
| 72 | 确保虚假ICMP响应被忽略 | yes |
| 73 | 确保启用反向路径过滤 | no |
| 74 | 确保开启tcp syn cookies | yes |
| 75 | 确保安装iptables软件包 | yes |
| 76 | 确保默认防火墙策略为拒绝 | no |
| 77 | 确保环回流量被正确配置 | no |
| 78 | 确保所有开放的端口都有对应的防火墙规则 | no |
| 79 | 确保审计日志存储大小已配置 | no |
| 80 | 确保审计日志已满时禁用系统 | no |
| 81 | 确保审核日志不会自动删除 | no |
| 82 | 确保auditd服务已启用 | yes |
| 83 | 确保audit对之前启动的进程也审计 | yes |
| 84 | 确保收集修改日期和时间信息的事件 | no |
| 85 | 确保收集修改user/group信息的事件 | no |
| 86 | 确保收集修改系统网络环境的事件 | no |
| 87 | 收集修改系统强制访问控制的事件 | no |
| 88 | 确保收集登录和注销事件 | no |
| 89 | 确保收集会话启动信息 | no |
| 90 | 确保收集自主访问控制权限修改事件 | no |
| 91 | 确保收集未成功和未经授权的文件访问尝试 | no |
| 92 | 确保收集使用特权命令 | no |
| 93 | 确保收集成功的文件系统安装 | no |
| 94 | 确保收集用户的文件删除事件 | no |
| 95 | 确保收集对系统管理范围（sudoers）的更改 | no |
| 96 | 确保收集系统管理员操作（sudolog） | no |
| 97 | 确保收集内核模块的加载和卸载 | no |
| 98 | 确保审计配置不可变 | no |
| 99 | 确保rsyslog服务已启用 | None |
| 100 | 确保配置了rsyslog默认文件权限 | no |
| 101 | 确保将rsyslog配置为将日志发送到远程日志主机 | no |
| 102 | 确保安装了rsyslog或syslog-ng服务 | yes |
| 103 | 确保所有的log文件都配置了正确的权限 | no |
| 104 | 确保开启cron守护进程 | None |
| 105 | 确保正确配置/etc/crontab文件的权限 | no |
| 106 | 确保正确配置/etc/cron.hourly文件的权限 | no |
| 107 | 确保正确配置/etc/cron.daily文件的权限 | no |
| 108 | 确保正确配置/etc/cron.weekly文件的权限 | no |
| 109 | 确保正确配置/etc/cron.monthly文件的权限 | no |
| 110 | 确保正确配置/etc/cron.d文件的权限 | no |
| 111 | 确保at或cron仅限授权用户使用 | no |
| 112 | 确保正确配置/etc/ssh/sshd_config文件的权限 | no |
| 113 | 确保ssh的日志等级设置为INFO | yes |
| 114 | 确保关闭SSH X11 forwarding | no |
| 115 | 确保SSH MaxAuthTries设置为4或更低 | no |
| 116 | 确保已启用SSH IgnoreRhosts | yes |
| 117 | 确保已禁用SSH HostbasedAuthentication | yes |
| 118 | 确保已禁用ssh root登陆 | no |
| 119 | 确保已禁用SSH PermitEmptyPasswords | yes |
| 120 | 确保禁止用户向ssh守护程序提供环境选项 | yes |
| 121 | 确保仅使用经过批准的MAC算法 | no |
| 122 | 确保配置SSH空闲超时间隔 | yes |
| 123 | 确保SSH LoginGraceTime设置为一分钟或更短 | no |
| 124 | 确保SSH访问受限 | no |
| 125 | 确保配置了SSH警告标题 | no |
| 126 | 确保配置了创建密码时应遵循的规则 | no |
| 127 | 确保配置了尝试登陆失败N次后锁定账户 | no |
| 128 | 确保限制了密码重用次数 | no |
| 129 | 确保密码使用SHA-512加密 | no |
| 130 | 确保密码到期时间为365天或更短 | no |
| 131 | 确保修改密码间隔最短天数为7或更多 | no |
| 132 | 确保密码到期警告天数为7或更多 | yes |
| 133 | 确保非活动密码锁定为30天或更短时间 | no |
| 134 | 确保所有用户的密码更改日期都是过去的 | yes |
| 135 | 确保系统帐户不能登录 | no |
| 136 | 确保root帐户的默认组为GID 0 | yes |
| 137 | 确保默认用户umask为027或更高限制 | yes |
| 138 | 确保默认用户shell超时为900秒或更短 | no |
| 139 | 确保限制对su命令的访问 | no |
| 140 | 确保正确配置/etc/passwd文件的权限 | yes |
| 141 | 确保正确配置/etc/shadow文件的权限 | no |
| 142 | 确保正确配置/etc/group文件的权限 | yes |
| 143 | 确保正确配置/etc/gshadow文件的权限 | no |
| 144 | 确保正确配置/etc/passwd-文件的权限 | yes |
| 145 | 确保正确配置/etc/shadow-文件的权限 | no |
| 146 | 确保正确配置/etc/group-文件的权限 | yes |
| 147 | 确保正确配置/etc/gshadow-文件的权限 | no |
| 148 | 确保不存在全局可写文件 | yes |
| 149 | 确保密码字段不为空 | yes |
| 150 | 确保root是唯一的UID 0帐户 | yes |
| 151 | 确保所有用户都拥有自己的家目录 | no |
| 152 | 确保iptables-services包没有安装 | no |
| 153 | 确保nftables没有安装、停止和屏蔽 | no |
| 154 | 确保firewalld服务启用并运行 | no |
| 155 | 确保设置了默认区域 | no |
| 156 | 确保auditd服务启用并运行 | no |
| 157 | 确保audit_backlog_limit足够 | no |
| 158 | 确保远程rsyslog消息只在指定的日志主机上被接受 | no |
| 159 | 确保将journald配置为发送日志到rsyslog | no |
| 160 | 确保将journald配置为压缩大型日志文件 | yes |
| 161 | 确保日志被配置为写日志文件到持久磁盘 | no |
| 162 | 确保配置了SSH私有主机密钥文件的权限 | no |
| 163 | 确保配置了SSH公共主机密钥文件的权限 | yes |
| 164 | 确保SSH只使用强密码 | yes |
| 165 | 确保只使用强密钥交换算法 | yes |
| 166 | 确保启用了SSH PAM | yes |
| 167 | 确保禁用SSH allowtcpforward | no |
| 168 | 确保配置了SSH maxstartup | no |
| 169 | 确保SSH最大会话数受到限制 | yes |
| 170 | 确保修改密码间隔最短天数为1 | no |
| 171 | 确保/etc/passwd中的帐户使用隐藏密码 | yes |
| 172 | 确保root路径的完整性 | yes |
| 173 | 确保用户的主目录权限限制在750或更高 | no |
| 174 | 确保用户拥有自己的主目录 | yes |
| 175 | 确保没有用户拥有.forward文件 | no |
| 176 | 确保没有用户拥有.netrc文件 | yes |
| 177 | 确保用户的.netrc文件不能被组或全局访问 | yes |
| 178 | 确保没有用户拥有.rhosts文件 | yes |
| 179 | 确保/etc/passwd中的所有组都存在于/etc/group中 | yes |
| 180 | 确保不存在重复的uid | yes |
| 181 | 确保不存在重复的gid | yes |
| 182 | 确保不存在重复的用户名 | yes |
| 183 | 确保没有重复的组名存在 | yes |
| 184 | 确保shadow组为空 | yes |
| 185 | 确保配置了package manager存储库 | no |
| 186 | 确保已配置/dev/shm | yes |
| 187 | 确保在可移动媒体分区上设置noexec选项 | no |
| 188 | 确保在可移动媒体分区上设置nodev选项 | no |
| 189 | 确保在可移动媒体分区上设置nosuid选项 | no |
| 190 | 确保时间同步 | no |
| 191 | 确保iptables被刷新 | yes |
| 192 | 确保防火墙表存在 | no |
| 193 | 确保基链存在 | no |
| 194 | 确保配置了环回流量 | no |
| 195 | 确保配置出站和已建立的连接 | no |
| 196 | 确保默认拒绝防火墙策略 | no |
| 197 | 确保iptables规则被保存 | no |
| 198 | 确保iptables已启用并正在运行 | no |
| 199 | 确保IPv6默认拒绝防火墙策略 | no |
| 200 | 确保配置了IPv6环回流量 | no |
| 201 | 确保配置了IPv6出站和已建立的连接 | no |
| 202 | 确保所有开放端口都有IPv6防火墙规则 | no |
| 203 | 确保ip6tables规则被保存 | no |
| 204 | 确保ip6tables已启用并正在运行 | no |

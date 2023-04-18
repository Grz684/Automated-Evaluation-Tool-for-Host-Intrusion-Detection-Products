# -*- coding: utf-8 -*-

import sqlite3
import time
import requests
import json


def find_best_matches(cn_desc_list, check_item_list, similarity_func, similarity_threshold=0.5):
    matches_from_cn_desc = {}
    matches_from_check_item = {}

    for i, cn_desc in enumerate(cn_desc_list):
        best_match_index = -1
        best_match_score = -1

        for j, check_item in enumerate(check_item_list):
            similarity = similarity_func(cn_desc, check_item)

            if similarity > best_match_score:
                best_match_score = similarity
                best_match_index = j

        if best_match_score >= similarity_threshold:
            matches_from_cn_desc[i] = (best_match_index, best_match_score)

    for j, check_item in enumerate(check_item_list):
        best_match_index = -1
        best_match_score = -1

        for i, cn_desc in enumerate(cn_desc_list):
            similarity = similarity_func(cn_desc, check_item)

            if similarity > best_match_score:
                best_match_score = similarity
                best_match_index = i

        if best_match_score >= similarity_threshold:
            matches_from_check_item[j] = (best_match_index, best_match_score)

    matched_pairs = []

    for i, (j, score_from_cn_desc) in matches_from_cn_desc.items():
        if j in matches_from_check_item and matches_from_check_item[j] == (i, score_from_cn_desc):
            matched_pairs.append((cn_desc_list[i], check_item_list[j]))

    return matched_pairs


def simnet_check_by_baidu(text1, text2):
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v2/simnet?charset=&access_token=" + get_access_token()

    payload = json.dumps({
        "text_1": text1,
        "text_2": text2
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    jsonData = json.loads(response.text)
    print(jsonData)

    return jsonData['score']


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": "uL0P7on65vGyw8Za8DLQesly",
              "client_secret": "s0QPmxh0GYK5hc7APIzZmj5NMMo9jKdF"}
    return str(requests.post(url, params=params).json().get("access_token"))


if __name__ == '__main__':
    yunsuo_vs_ali_baseline_items_list = [('确保禁止挂载cramfs文件系统', '确保cramfs文件系统挂载禁用'), ('确保禁止挂载udf文件系统', '确保udf文件系统挂载禁用'), ('确保/tmp存在独立的分区', '确保/tmp目录独立分区存在'), ('确保/tmp分区设置了nodev属性', '确保/tmp分区设置了nodev选项'), ('确保/tmp分区设置了nosuid属性', '确保/tmp分区设置了nosuid选项'), ('确保/tmp分区设置了noexec属性', '确保/tmp分区设置了noexec选项'), ('确保/dev/shm分区设置了nodev属性', '确保/dev/shm分区设置了nodev选项'), ('确保/dev/shm分区设置了nosuid属性', '确保/dev/shm分区设置了nosuid选项'), ('确保/dev/shm分区设置了noexec属性', '确保/dev/shm分区设置了noexec选项'), ('关闭自动挂载功能', '确保自动挂载禁用'), ('确保AIDE程序已安装', '确保AIDE安装'), ('确保开启定期检查文件系统完整性的功能', '确保定期检查文件系统完整性'), ('确保正确配置bootloader相关文件的权限', '确保bootloader配置文件权限已配置'), ('确保引导程序密码已设置', '确保只使用了已核准的密码'), ('确保单用户模式需要身份验证', '确保单用户模式需要验证'), ('限制生成核心转储文件', '确保core dumps 受限制'), ('确认启用地址空间布局随机化(ASLR)', '开启地址空间布局随机化'), ('确认禁用prelink', '确保prelink被禁用'), ('确保SELinux的状态为Enforcing', '确保SELinux状态为enforcing'), ('确保配置了SELinux的策略', '确保SELinux策略设置'), ('确保安装SELinux软件包', '确保已安装SELinux'), ('确保已禁用xinetd服务', '确保xinetd服务未启用'), ('如果启用ntp服务, 确保ntp被正确配置', '确保TCP Wrappers已安装'), ('确保X Window System相关软件包未安装', '确保X Window系统未安装'), ('确保Avahi服务已禁用', '确保Avahi服务器未启用'), ('确保CUPS服务已禁用', '确保CUPS未启用'), ('确保DHCP服务已禁用', '确保DHCP服务器未启用'), ('确保NFS和RPC服务已禁用', '确保NFS和RPC未启用'), ('确保DNS服务已禁用', '确保DNS服务器未启用'), ('确保FTP服务已禁用', '确保FTP服务器未启用'), ('确保HTTP服务已禁用', '确保HTTP服务器未启用'), ('确保IMAP和POP3服务已禁用', '确保IMAP和POP3服务器未启用'), ('确保SAMBA服务已禁用', '确保Samba未启用'), ('确保SNMP服务已禁用', '确保SNMP服务器未启用'), ('确保邮件传输代理配置为仅本地模式', '确保邮件传输代理配置为仅限本地模式'), ('确保NIS服务已禁用', '确保NIS服务未启用'), ('确保telnet服务已禁用', '确保telnet服务未启用'), ('确保tftp服务已禁用', '确保tftp服务未启用'), ('确保rsync服务已禁用', '确保rsync服务未启用'), ('确保NIS客户端未安装', '确保NIS客户端未安装'), ('确保rsh客户端未安装', '确保rsh客户端未安装'), ('确保talk客户端未安装', '确保talk客户端未安装'), ('确保telnet客户端未安装', '确保telnet客户端未安装'), ('确保LDAP客户端未安装', '确保LDAP客户端未安装'), ('确保IP转发已禁用', '确保IP转发禁用(仅限主机)'), ('确保数据包重定向发送已禁用', '确保数据包重定向发送功能已禁用（仅限主机）'), ('确保不接受源路由数据包', '确保数据包不被源路由接受'), ('确保不接受ICMP重定向', '确保ICMP重定向不被接受'), ('确保不接受安全的ICMP重定向', '确保安全的ICMP重定向不被接受'), ('确保记录可疑数据包', '确保可疑数据包被记录'), ('确保ICMP广播请求被忽略', '确保广播ICMP请求被忽略'), ('确保虚假ICMP响应被忽略', '确保伪造的ICMP响应被忽略'), ('确保启用反向路径过滤', '确保反向路径过滤被启用'), ('确保开启tcp syn cookies', '确保 TCP SYN Cookie启用'), ('确保环回流量被正确配置', '确保本地回环规则已正确配置'), ('确保所有开放的端口都有对应的防火墙规则', '确保所有打开的端口都存在防火墙规则'), ('确保审计日志存储大小已配置', '确保审核日志存储大小已配置'), ('确保auditd服务已启用', '确保审核服务已启用'), ('确保audit对之前启动的进程也审计', '确保启用对auditd之前启动的进程的审计'), ('确保收集修改日期和时间信息的事件', '确保收集修改日期和时间信息的事件'), ('确保收集修改user/group信息的事件', '确保收集修改用户/组信息的事件'), ('收集修改系统强制访问控制的事件', '确保收集修改系统强制访问控制的事件'), ('确保收集登录和注销事件', '确保收集登录和注销事件'), ('确保收集会话启动信息', '确保收集会话启动信息'), ('确保rsyslog服务已启用', '确保rsyslog服务已启用'), ('确保配置了rsyslog默认文件权限', '确保rsyslog默认文件权限已配置'), ('确保将rsyslog配置为将日志发送到远程日志主机', '确保rsyslog配置为将日志发送到远程日志主机'), ('确保所有的log文件都配置了正确的权限', '确保所有日志文件权限已正确配置'), ('确保开启cron守护进程', '确保cron守护进程已启用'), ('确保正确配置/etc/crontab文件的权限', '确保/etc/crontab文件权限已正确配置'), ('确保正确配置/etc/cron.hourly文件的权限', '确保/etc/cron.hourly 文件权限已正确配置'), ('确保正确配置/etc/cron.daily文件的权限', '确保/etc/cron.daily文件权限已正确配置'), ('确保正确配置/etc/cron.weekly文件的权限', '确保/etc/cron.weekly 文件权限已正确配置'), ('确保正确配置/etc/cron.monthly文件的权限', '确保/etc/cron.monthly文件权限已正确配置'), ('确保正确配置/etc/cron.d文件的权限', '确保/etc/cron.d文件权限已正确配置'), ('确保at或cron仅限授权用户使用', '确保at/cron仅限于授权用户'), ('确保正确配置/etc/ssh/sshd_config文件的权限', '确保配置了文件/etc/ssh/sshd-config的权限'), ('确保ssh的日志等级设置为INFO', '确保SSH LogLevel设置为INFO'), ('确保关闭SSH X11 forwarding', '确保 SSH X11 被禁用'), ('确保SSH MaxAuthTries设置为4或更低', '确保SSH MaxAuthTries设置为3到6之间'), ('确保已启用SSH IgnoreRhosts', '确保SSH的IgnoreRhosts已启用'), ('确保已禁用SSH HostbasedAuthentication', '确保SSH的HostbasedAuthentication被禁用'), ('确保禁止用户向ssh守护程序提供环境选项', '确保SSH的PermitUserEnvironment被禁用'), ('确保仅使用经过批准的MAC算法', '确保只使用了已批准的MAC算法'), ('确保SSH LoginGraceTime设置为一分钟或更短', '确保SSH LoginGraceTime设置为小于60秒'), ('确保SSH访问受限', '确保ssh访问受到限制'), ('确保配置了SSH警告标题', '确保SSH警告通知已设置'), ('确保限制了密码重用次数', '检查密码重用是否受限制'), ('确保密码使用SHA-512加密', '确保密码散列算法为SHA-512'), ('确保密码到期警告天数为7或更多', '确保密码到期警告天数为7或更多'), ('确保非活动密码锁定为30天或更短时间', '确保不活跃的密码锁定小于等于30天'), ('确保所有用户的密码更改日期都是过去的', '确保所有用户的上次密码更改日期都在过去'), ('确保系统帐户不能登录', '確保系统帐户为non-login'), ('确保root帐户的默认组为GID 0', '确保root用户默认组的GID为0'), ('确保默认用户umask为027或更高限制', '确保默认用户umask为027或更严格'), ('确保限制对su命令的访问', '确保su命令的访问受限制'), ('确保正确配置/etc/shadow文件的权限', '确保 /etc/shadow 权限配置'), ('确保正确配置/etc/group文件的权限', '确保 /etc/group  权限配置'), ('确保正确配置/etc/passwd-文件的权限', '确保 /etc/passwd 权限配置'), ('确保正确配置/etc/gshadow-文件的权限', '确保 /etc/gshadow 权限配置'), ('确保不存在全局可写文件', '确保不存在无主文件或目录'), ('确保root是唯一的UID 0帐户', '确保root是唯一的UID为0的帐户'), ('确保所有用户都拥有自己的家目录', '确保用户拥有自己的home目录'), ('确保日志被配置为写日志文件到持久磁盘', '确保日志已配置'), ('确保配置了SSH私有主机密钥文件的权限', '确保配置了ssh私钥文件的权限'), ('确保配置了SSH公共主机密钥文件的权限', '确保配置了ssh公密钥文件的权限'), ('确保SSH只使用强密码', '禁止SSH空密码用户登录'), ('确保修改密码间隔最短天数为1', '设置密码修改最小间隔时间'), ('确保用户的主目录权限限制在750或更高', '确保用户home目录权限设置为750或者更严格'), ('确保没有用户拥有.forward文件', '确保没有用户有.forward文件'), ('确保没有用户拥有.netrc文件', '确保没有用户有.netrc文件'), ('确保用户的.netrc文件不能被组或全局访问', "确保用户'.netrc'文件不可全局或组访问"), ('确保没有用户拥有.rhosts文件', '确保没有用户有.rhosts文件'), ('确保/etc/passwd中的所有组都存在于/etc/group中', '确保/etc/passwd 中的所有组在 /etc/group存在'), ('确保不存在重复的gid', '确保重复GID不存在'), ('确保不存在重复的用户名', '确保重复用户名不存在'), ('确保配置了package manager存储库', '确保已配置包管理器存储库'), ('确保时间同步', '确保使用了时间同步'), ('确保防火墙表存在', '确保防火墙已安装'), ('确保配置出站和已建立的连接', '确保出站和已建立的连接配置规则'), ('确保配置了IPv6环回流量', '确保不接受IPv6重定向'), ('确保配置了IPv6出站和已建立的连接', '确保不接受IPv6路由器通告')]
    print(len(yunsuo_vs_ali_baseline_items_list))
    for item in yunsuo_vs_ali_baseline_items_list:
        print(item)
    # # 连接第一个数据库并读取cn_desc列
    # db1 = sqlite3.connect('yunsuo_pf_test/yunsuo_cis_baseline_scan_items.db')
    # cursor1 = db1.cursor()
    # cursor1.execute('SELECT cn_desc FROM items')
    # cn_desc_data = cursor1.fetchall()
    #
    # # 连接阿里cis数据库并读取check_item列
    # db2 = sqlite3.connect('ali_pf_test/ali_cis_baseline_scan_items.db')
    # cursor2 = db2.cursor()
    # cursor2.execute('SELECT check_item FROM items')
    # check_item_data = cursor2.fetchall()
    #
    # # 处理结果
    # cn_desc_list = [row[0] for row in cn_desc_data]
    # check_item_list = [row[0] for row in check_item_data]
    #
    # # 关闭数据库连接
    # cursor1.close()
    # db1.close()
    # cursor2.close()
    # db2.close()
    #
    # print("yunsuo 列：", cn_desc_list)
    # print("ali 列：", check_item_list)
    # text1 = "确保SSH LoginGraceTime设置为一分钟或更短"
    # text2 = "确保SSH LoginGraceTime设置为小于60秒"
    #
    # simnet_check_by_baidu(text1, text2)

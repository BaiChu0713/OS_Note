# 针对目标[192.168.17.131]的信息收集报告

侦察日期： [2025/11/25]
报告作者： [白初]
目标说明： [搜集目标靶机相关信息]

## 执行摘要

目的:深化学习侦查阶段的被动/主动搜集

## 信息收集详情

### 被动收集

#### whois

![](/Photos/D7_1.png)
```
#
# ARIN WHOIS data and services are subject to the Terms of Use
# available at https://www.arin.net/resources/registry/whois/tou/
#
# Copyright 1997-2025, American Registry for Internet Numbers, Ltd.

NetRange:       192.168.0.0 - 192.168.255.255
CIDR:           192.168.0.0/16
NetName:        PRIVATE-ADDRESS-CBLK-RFC1918
NetHandle:      NET-192-168-0-0-1
Parent:         NET192 (NET-192-0-0-0-0)
NetType:        IANA Special Use
OriginAS:       
Organization:   Internet Assigned Numbers Authority (IANA)
RegDate:        1993-03-15
Updated:        2013-06-06
Comment:        These addresses are in use by millions of devices
Comment:        and are only intended for private LANs; they
Comment:        are not routable on the public Internet.
Comment:        See RFC 1918 (https://tools.ietf.org/html/rfc1918).
Ref:            https://rdap.arin.net/registry/ip/192.168.0.0
```

结论：RFC 1918 私有地址，不属于任何公网组织


#### nslookup
![](/Photos/D7_3.png)

NXDOMAIN

内网的 DNS（192.168.17.2）里没有给 192.168.17.131 做反向解析记录，所以返回 ‘找不到’

#### dig

![](/Photos/D7_2.png)


| 段落 | 关键信息 | 本例结论 |
| ---- | -------- | -------- |
| **HEADER** | `status: NXDOMAIN` | 无 PTR 记录 |
| **flags** | `qr rd ra` **无 aa** | 缓存/转发回答 |
| **QUERY/ANSWER** | 1 / 0 | 问了 1 条，答 0 条 |
| **AUTHORITY** | `168.192.in-addr.arpa. SOA` | 空区，负缓存依据 |
| **EDNS** | `udp: 1232` + COOKIE | 扩展协商，无业务数据 |
| **Query time** | 7 ms | 局域网延迟 |
| **SERVER** | 192.168.17.2#53 | 内网 DNS 给出否定应答 |

> 一句话：**192.168.17.131 在内网 DNS 里没起名字，所以返回 NXDOMAIN。**


| 工具 / 数据库 | 工作层级 | 查询内容 | 返回数据示例 | 典型用途 | 对 192.168.x.x 的意义 |
|---|---|---|---|---|---|
| **whois** | **IP 分配记录**<br>（RIR 数据库）| 网段归属、注册组织、联系人、ASN | NetRange / CIDR / Org / Address / Phone | 被动踩点：确认目标 IP 是否属于云厂商、企业专线、还是 IDC | 仅得到模板“RFC1918 Private Use”，**无法定位到个人或企业** |
| **dig -x** | **DNS 反向解析**<br>（in-addr.arpa 区）| IP → 域名（PTR 记录） | 131.17.168.192.in-addr.arpa. PTR srv131.corp.com. | 发现机器名、内网命名规律、VPN 池、邮件服务器 | 若内网未建反向区 → **NXDOMAIN**；若自建 DNS → 可泄漏主机名、职能、域森林名 |
| **nslookup** | **同上**<br>（DNS 反向，但工具不同） | 同 dig -x | 同上 | 快速验证，Windows 默认自带；脚本友好性弱 | 与 dig 结果一致，只是**输出更简洁**，无权威/TTL 等细节 |

> 一句话差异：  
> - **whois** 告诉你“这段 IP 分给谁”——**公网才有效**；  
> - **dig/nslookup** 告诉你“这台机器管自己叫什么”——**依赖本地反向区**，私有地址也能用，但需内部 DNS 配合。

### 主动侦察

#### ping

![](/Photos/D7_4.png)

结论:能ping通，主机存活

#### masscan

![](/Photos/D7_6.png)

简单扫了1000个常用的端口缩小侦察范围

#### scan
![](/Photos/D7_5.png)

扫描版本号以及开放端口，获取更详细的信息

#### 主动侦察tip
| 维度 | 工具 | 一句话作用 | 典型用法示例 |
| ---- | ---- | ---------- | ------------ |
| **主机存活** | `ping` / `fping` / `hping3` | ICMP/TCP/UDP/ARP 探活 | `fping -ag 192.168.17.0/24` |
| **端口扫描** | `nmap` / `masscan` / `unicornscan` | 端口开放、OS、服务指纹 | `nmap -sV -O -T4 192.168.17.131` |
| **漏洞扫描** | `nmap --script vuln` / `nikto` / `openvas` | 已知 CVE、配置缺陷 | `nikto -h http://192.168.17.131` |
| **Web 目录** | `dirb` / `gobuster` / `feroxbuster` | 暴力目录/文件 | `gobuster dir -u http://target -w /usr/share/wordlists/dirb/common.txt` |
| **DNS 爆破** | `dnsrecon` / `dnsenum` / `fierce` | 子域、域传送、反向 | `dnsrecon -d example.com -D sub.txt -t brt` |
| **SSL/TLS** | `sslscan` / `testssl.sh` / `sslyze` | 协议、套件、证书 | `sslscan 192.168.17.131:443` |
| **SNMP** | `onesixtyone` / `snmp-check` | 社区串、系统信息 | `onesixtyone -c public 192.168.17.131` |
| **SMB/NetBIOS** | `enum4linux-ng` / `smbclient` / `rpcclient` | 共享、用户、组、策略 | `enum4linux-ng -A 192.168.17.131` |
| **LDAP** | `ldapsearch` / `windapsearch` | 用户/组/计算机枚举 | `ldapsearch -x -H ldap://192.168.17.131 -s base namingcontexts` |
| **FTP/TFTP** | `ftp` / `tftp` / `nmap --script ftp-*` | 匿名登录、目录遍历 | `nmap --script ftp-anon,ftp-bounce -p 21 192.168.17.131` |
| **SSH** | `ssh-audit` / `nmap --script ssh-*` | 算法、密钥、banner | `ssh-audit 192.168.17.131` |
| **SMTP** | `smtp-user-enum` / `swaks` | 用户枚举、中继测试 | `smtp-user-enum -M VRFY -U users.txt -t 192.168.17.131` |
| **VoIP** | `svmap` / `svwar`（SIPVicious） | SIP 服务器/分机枚举 | `svmap 192.168.17.0/24` |
| **数据库** | `sqlmap` / `tnscmd10g`（Oracle） / `msf` 模块 | SQL 注入、监听器探活 | `sqlmap -u "http://target/page.php?id=1"` |
| **抓包/注入** | `tcpdump` / `wireshark` / `hping3` / `scapy` | 手工发包、畸形包、重放 | `hping3 -S -p 80 --flood 192.168.17.131` |
| **漏洞利用** | `metasploit` (`msfconsole`) | 一体化 Exploit/Post | `msf> use exploit/multi/http/apache_struts*` |
| **Web  fuzz** | `wfuzz` / `ffuf` / `burpsuite` | 参数、值、Header 爆破 | `ffuf -w params.txt -u http://target/FUZZ` |
| **API/GraphQL** | `gqlmap` / `arjun` | 端点、查询、注入 | `gqlmap -u http://target/graphql` |
| **密码喷洒** | `hydra` / `medusa` / `ncrack` | 多协议弱口令 | `hydra -l admin -P pass.txt ssh://192.168.17.131` |
| **AD 综合** | `bloodhound-python` / `enum4linux-ng` / `netexec` | 域拓扑、攻击路径 | `bloodhound-python -d corp.com -u user -p pass -c all` |

使用节奏建议：
1. 先 ping/fping 扫存活 →
2. masscan 快速全端口 →
3. nmap -sV -sC 细扫 →
4. 按服务选专用工具（nikto、sslscan、enum4linux-ng…）→
5. msf/sqlmap 验证利用。

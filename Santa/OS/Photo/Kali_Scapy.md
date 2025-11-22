# Scapy 网络探测实验总结

## 1. 基础数据包创建函数

### `IP()` 函数
```
IP(dst="192.168.1.1", src="192.168.1.100", ttl=64, proto=6)
```

**参数说明：**
- `dst`：目标IP地址（Destination）
- `src`：源IP地址（Source），不指定则使用本机IP
- `ttl`：生存时间（Time To Live），每经过一个路由器减1，为0时丢弃
- `proto`：上层协议类型（6=TCP, 17=UDP, 1=ICMP）
- `id`：数据包标识符
- `flags`：IP标志位（DF=不分片, MF=更多分片）

### `TCP()` 函数
```
TCP(dport=80, sport=12345, flags="S", seq=1000, window=8192)
```

**参数说明：**
- `dport`：目标端口（Destination Port）
- `sport`：源端口（Source Port），不指定则随机生成
- `flags`：TCP控制标志
  - `S` = SYN（同步，建立连接）
  - `A` = ACK（确认）
  - `F` = FIN（结束连接）
  - `R` = RST（重置连接）
  - `P` = PSH（推送数据）
  - `U` = URG（紧急指针）
- `seq`：序列号
- `ack`：确认号
- `window`：窗口大小

### `UDP()` 函数

```
UDP(dport=53, sport=12345)
```

**参数说明：**
- `dport`：目标端口
- `sport`：源端口
- `chksum`：校验和（可选）

### `ICMP()` 函数

```
ICMP(type=8, code=0)  # type=8 是 Echo Request (ping请求)
```
**参数说明：**
- `type`：ICMP类型
  - `8` = Echo Request（ping请求）
  - `0` = Echo Reply（ping回复）
  - `3` = Destination Unreachable（目标不可达）
- `code`：子类型代码

---

## 2. 发送函数参数详解

### `sr1()` - 发送并接收第一个回复
```
sr1(pkt, timeout=2, verbose=1, iface="eth0", filter="icmp")
```
**参数说明：**
- `pkt`：要发送的数据包
- `timeout`：等待回复的超时时间（秒）
- `verbose`：显示详细程度（0=安静，1=默认，2=更详细）
- `iface`：指定网络接口
- `filter`：BPF过滤器，只捕获匹配的回复包

### `sr()` - 发送并接收所有回复
```
answers, unanswers = sr(pkt, timeout=1, multi=True, retry=2)
```
**参数说明：**
- `multi`：是否允许多个回复（对于广播包）
- `retry`：重试次数
- 返回两个列表：`answers`（有回复的），`unanswers`（无回复的）

### `send()` / `sendp()` - 只发送不接收
```
send(pkt, count=10, inter=0.1, iface="eth0")
sendp(pkt)  # 第二层发送
```
**参数说明：**
- `count`：发送次数
- `inter`：发送间隔（秒）
- `iface`：指定网络接口

---

## 3. 扫描函数参数详解

### `srp()` - 第二层发送接收
```
ans, unans = srp(pkt, timeout=2, iface="eth0", verbose=0)
```

**参数说明：**
- 专门用于以太网帧级别的发送接收
- 常用于ARP扫描等第二层操作

### ARP扫描参数
```
Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.1.0/24", hwdst="ff:ff:ff:ff:ff:ff")
```
**Ether参数：**
- `dst`：目标MAC地址，`ff:ff:ff:ff:ff:ff`是广播地址

**ARP参数：**
- `pdst`：目标IP或IP范围
- `psrc`：源IP地址
- `hwdst`：目标MAC地址，广播时用全F
- `op`：操作类型（1=请求，2=回复）

---

## 4. 嗅探函数参数详解

### `sniff()` - 数据包捕获
```
sniff(count=100, timeout=30, iface="eth0", filter="tcp port 80", prn=callback_func, store=True)
```
**参数说明：**
- `count`：捕获数据包的数量
- `timeout`：捕获超时时间
- `iface`：网络接口
- `filter`：BPF过滤表达式
- `prn`：回调函数，对每个捕获的包执行
- `store`：是否在内存中存储数据包

### BPF过滤器常用语法：
```
"host 192.168.1.1"           # 指定主机
"net 192.168.1.0/24"         # 指定网络
"port 80"                    # 指定端口
"tcp" / "udp" / "icmp"       # 指定协议
"src host 192.168.1.1"       # 源主机
"dst port 53"                # 目标端口
"tcp and port 80"            # 组合条件
```

---

## 5. 显示和分析函数参数

### `summary()` - 摘要显示
```
packets.summary(lfilter=lambda pkt: pkt.haslayer(TCP),
                prn=lambda pkt: pkt.sprintf("{IP:%IP.src% -> %IP.dst%}"))
```
**参数说明：**
- `lfilter`：过滤函数，只显示匹配的数据包
- `prn`：自定义显示格式函数

### `show()` - 详细显示
```
pkt.show()           # 显示所有层
pkt[TCP].show()      # 只显示TCP层
```

### `sprintf()` - 格式化输出
```
pkt.sprintf("%IP.src% > %IP.dst% %TCP.sport%")
```
**常用格式符：**
- `%IP.src%`：源IP
- `%IP.dst%`：目标IP  
- `%TCP.sport%`：TCP源端口
- `%TCP.dport%`：TCP目标端口
- `%ICMP.type%`：ICMP类型

---

## 6. 文件操作函数

### `rdpcap()` - 读取PCAP文件
```
packets = rdpcap("file.pcap", count=100)
```
**参数说明：**
- 文件名或文件对象
- `count`：最多读取的数据包数量

### `wrpcap()` - 写入PCAP文件
```
wrpcap("output.pcap", packets, append=False)
```
**参数说明：**
- `append`：是否追加到现有文件

---

## 7. 实用示例：理解每个参数

```
# 完整的TCP SYN扫描示例
answers, unanswers = sr(
    IP(dst="192.168.1.1", ttl=64)/      # 目标IP，TTL=64
    TCP(                                # TCP层
        dport=(1,100),                  # 扫描端口1-100
        sport=12345,                    # 源端口
        flags="S",                      # SYN标志
        window=1024                     # 窗口大小
    ),
    timeout=1,                          # 1秒超时
    verbose=0,                          # 不显示详细信息
    retry=1                             # 重试1次
)
```

**这个扫描的过程：**
1. 创建IP包：目标=192.168.1.1，TTL=64
2. 创建TCP包：扫描端口1-100，设置SYN标志
3. 发送并等待1秒
4. 如果有端口回复SYN-ACK，说明端口开放
5. 如果没有回复，说明端口关闭或被过滤

---

## 重要参数总结表

| 函数 | 关键参数 | 作用 | 默认值 |
|------|----------|------|--------|
| `sr1()` | `timeout`, `verbose` | 控制等待时间和输出 | 2秒, 1 |
| `sniff()` | `count`, `filter`, `prn` | 控制捕获条件和处理 | 无限制 |
| `IP()` | `dst`, `ttl`, `proto` | 设置目标、生存时间、协议 | 必需, 64, 自动 |
| `TCP()` | `dport`, `flags` | 设置端口和标志位 | 随机, "S" |



## 实验概述
使用Scapy工具构造ARP和TCP数据包，通过分析应答包来推测目标系统的存活状态和端口开放情况。

## 实验环境
- 工具：Scapy
- 模式：交互式命令行界面

## ARP扫描

### 1. 启动Scapy
```
scapy
```
成功启动后显示 `>>>` 提示符。

### 2. 构造ARP请求包
```
ARP().display  # 显示ARP数据包模板
```

### 3. 配置ARP参数
根据实际情况设置本机MAC地址等参数，使用`ifconfig`命令查看网络信息。

### 4. 发送ARP请求
```
sr1(arp_request)  # 发送ARP请求并接收响应
```
- `sr1()`函数只能接收一个响应包
- 返回信息包含源MAC地址、源IP地址、目标MAC地址、目标IP地址等

### 5. ARP扫描局域网主机
**方法一：使用srp函数**
```
ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.1.0/24"), timeout=2)
print(ans.nsummary())  # 查看扫描结果
```

**方法二：使用内置arpping方法**
```
arping("192.168.1.0/24")
```

## TCP端口扫描

### 1. TCP SYN扫描
```
res, unres = sr(IP(dst="192.168.1.3")/TCP(flags="S", dport=(1,1024)))
```

**扫描原理：**
- 向每个端口发送TCP SYN包
- 通过响应判断端口状态：
  - 收到SYN-ACK包：端口开放
  - 收到TCP RST复位包：端口关闭
  - 收到ICMP错误：端口不可达

### 2. 查看扫描结果
```
res.summary(lfilter=lambda s,r: r.sprintf("%TCP.flags%")=="SA",
           prn=lambda s,r: r.sprintf("%TCP.sport% is open"))
```

### 3. 绕过防火墙的扫描

某些防火墙会丢弃没有TCP时间戳的包，需要添加选项：

```
res, unres = sr(IP(dst="192.168.1.3")/TCP(flags="S",
               options=[("Timestamp",(0,0))], dport=(1,1024)))
```

## 注意事项

1. **执行时间**：TCP端口扫描执行时间较长，需要耐心等待
2. **手动终止**：扫描过程中可能需要按 `Ctrl+C` 来结束程序
3. **结果查看**：使用 `res[1]` 查看详细扫描内容
4. **参数配置**：根据实际网络环境调整IP地址范围和超时时间

## 总结
Scapy提供了灵活的数据包构造和发送能力，能够有效进行网络主机发现和端口扫描，是网络探测和安全性测试的重要工具。

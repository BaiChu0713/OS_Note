# cmd命令合集


## 常用命令格式

`命令 [参数]`




## 文件目录操作

### cd
1. `cd /d`  切换到任意位置
2. `cd/? `帮助文件
3. `cd dir `当前目录所有文件
4. `cd ..`上一级文件
5. `cd /`返回到根目录

### dir


1. `dir`列出当前目录中的所有文件和子目录。
2. `mkdir x `创建新目录
3. `rmdir x `删除（空目录）
4. `rmdir /s x`

### copy/move
`copy a addr`

`move a addr`

### del ren
`del a`

`ren old_name new_name `

## 系统信息获取命令

`systeminfo` 查看系统消息
`whoami`
`hostname`

### task
1. ` tasklist` 查看进程列表
2. `taskkill /IM [进程名] /F `结束进程


## 网络配置命令

`ipconfig `查看计算机的 IP 地址、子网掩码和默认网关

`ipconfig /release;ipconfig /renew` 释放和更新 DHCP 分配的 IP 地址

`netstat   [选项] `显示当前所有的网络连接和监听端口

`tracert [IP 地址或域名] `追踪到另一端的路由

### ping

`ping   [选项]  [主机名称或IP地址]`

验证与远程计算机的连接，检查网络是否能够连通和分析网络速度，默认响应4下结束

## 磁盘和文件系统操作命令

`wmic logicaldisk get size,freespace,caption`  显示每个逻辑磁盘的总大小和可用空间

`format` [驱动器:] /FS:[文件系统]  将 D 盘格式化为 NTFS 文件系统

`chkdsk `[驱动器:]  检查 C 盘的错误

`diskpart` 进入 DiskPart 工具后，输入 list disk 查看所有磁盘信息

## 批处理文件

批处理文件是一个包含多个 CMD 命令的文本文件，可以方便地执行一系列命令

```
@echo off
echo Hello, World!
pause
```

## 环境变量

`set`  查看环境变量

`set [变量名]=[值] ` 设置环境变量

`set [变量名]=`  删除环境变量

## CMD 技巧

### 使用管道

管道符 | 可以将一个命令的输出作为另一个命令的输入(经典注入式攻击)

`tasklist | find "chrome"`


### 重定向

重定向符 `>` 可以将命令的输出保存到文件

`dir > output.txt`

### 批量重命名文件

for 循环批量重命名文件。

`for %f in (*.txt) do ren "%f" "*.bak"`

### CMD 无法识别命令

可能是因为命令未正确输入或未安装相应的程序

### 权限不足

某些命令需要管理员权限，右键点击 CMD 图标，选择“以管理员身份运行”。

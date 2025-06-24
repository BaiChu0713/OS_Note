# 进程 软件管理

## 进程

刚考完计组，我不多说——5/7状态自行回忆



```
tasklist [/S system [/U username [/P [password]]]]
         [/M [module] | /SVC | /V] [/FI filter] [/FO format] [/NH]
```

## wmic

wmic （Windows Management Instrumentation Command-line）是一个强大的命令行工具，它允许用户通过WMI（Windows Management Instrumentation）查询本地和远程系统的信息。

wmic 在Windows环境下用于管理硬件和操作系统的各个方面，提供了一个命令行界面来执行WMI查询。它是管理员在故障排查和系统监控方面不可或缺的工具。

wmic 可以执行如下操作：

- 查询系统硬件和软件信息。
- 操作进程和服务。
- 访问注册表项。
- 启动、停止和管理服务。
- 进行性能监控。

wmic 命令的输出可以被格式化和重定向，这意味着可以将数据导入到电子表格或文本文件中，以便进一步分析或报告使用。

`wmic process list brief`了解进程的运行状况，比如内存占用、系统资源消耗等

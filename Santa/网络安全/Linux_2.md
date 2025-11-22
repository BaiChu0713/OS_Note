##  Linux Shell

 Shell 是一个强大的程序，它接收您输入的命令并将其传递给操作系统执行。

 如果用过图形用户界面 (GUI)，可能遇到过像“终端”或“控制台”这样的应用程序。

 这些程序只是为您打开一个 Shell 会话。

### 理解 Bash
在本课程中，我们将重点关注 Bash (Bourne Again Shell) 程序。

Bash 是大多数 Linux 发行版的默认 Shell，使其成为一项必学的基本工具。 虽然存在像 、 和 这样的其他 Shell，但掌握 Bash 为使用任何 Linux 系统打下了坚实的基础。kshzshtsch

###Shell 提示符
打开终端时，您会看到 Shell 提示符。
它的外观在不同发行版之间可能有所不同，但通常遵循以下格式：。`username@hostname:current_directory$`


- `echo hi`

  将提供的文本作为参数回显（或“复述”）到终端上

- `pwd`

  查找 current directory linux

- `cd`

  - . (当前目录)：表示您当前所在的目录。
  - .. (父目录)：将您向上移动一级到包含您当前目录的目录。
  - ~ (主目录)：指向您的个人主目录（如 ）的快捷方式。/home/pete
  - \- (前一个目录)：将您带回到您上一个所在的目录。

- `ls`

列出当前目录

|参数|作用|
|-|-|
|a|list all(include hidden)|
|l|long(详细信息)|
|r|反向排序|

- `touch`

更改文件时间戳、创建新的空文件

`touch tmp`

`touch -r A B`将一个文件(B)的时间戳设置为与另一个文件（参考文件A）的时间戳相匹配

`touch -d "2023-01-01 12:30:00" tmp.txt` 设置特定日期

- `file`

找出文件是什么类型

- `cat`

- `less`
以分页格式显示文本

|参数|作用|
|-|-|
|g|导航到开头|
|G|导航到结尾|
|q|quit|
|h|help|
|/|搜索，n下一个，N上一个|

- `history`
显示输入的历史记录

`history -c`

- `clear`

- `cp`

`cp A [DESTINATION]`

|参数|作用|
|-|-|
|*|匹配任何字符序列|
|?| 匹配任何单个字符|
|[]|匹配方括号中包含的任何一个字符|

如果涉及到目录需要加上-r

- `mv`

重命名文件或目录，以及将它们移动到不同的位置。

`mv oldfile newfile`

`mv old_directory_name new_directory_name`


mv 命令的另一个核心功能是将项目从一个位置移动到另一个位置。

将单个文件移动到另一个目录：
`mv file2 /home/pete/Documents`

也可以一次移动多个文件。 只需列出所有源文件，然后是目标目录：
`mv file_1 file_2 /somedirectory`

它允许您首先指定目标目录。 在移动许多文件时，这可能更清晰。
`mv -t /somedirectory file_1 file_2`

|参数|作用|
|-|-|
|-i (interactive)|在覆盖任何现有文件之前提示确认|
|-b (backup)|覆盖文件但想保留旧版本，此选项会创建目标文件的备份。 备份通常以波浪号后缀重命名。~|
|-v (verbose)|命令打印它正在执行的操作，显示正在移动或重命名的每个文件|


- `mkdir`

直接从终端或命令提示符中在 Linux 中创建目录

如果是嵌套目录的话加-p

- `rm`

|参数|作用|
|-|-|
|i|interface|
|r|递归的|
|f|force|

'rmdir'删除一个空目录

- `find`

>find [路径] [表达式]

|参数|作用|
|-|-|
|-type|确定find的类型，d是目录、f是文件|
|-name|`-name x`就是寻找名字为x的|

- `help`

|类型|作用|
|-|-|
|help echo||
|echo --help||

- `man`

>man ls

手册，q退出

- `whatis`

>whatis echo

- `alias`
为任何命令或命令序列定义一个自定义名称。

创建临时别名

`alias ll='ls -la'`

现在，您无需输入 ls -la，只需输入 ll 即可执行相同的命令。这是自定义 shell 的一种简单而强大的方法。

使别名永久化

临时别名在您关闭终端或重新启动系统后就会消失。要使 command alias in linux 永久化，您需要将其添加到 shell 的配置文件中。
对于 Bash shell，该文件通常是 ~/.bashrc。

在文本编辑器中打开文件：nano ~/.bashrc
将您的别名定义添加到文件中，就像您在命令行中输入的那样：
```
alias ll='ls -la'
alias update='sudo apt update && sudo apt upgrade'
```

保存文件并退出编辑器。
为了使更改生效，您必须关闭并重新打开终端，或者使用 source 命令告诉 shell 重新加载配置文件：

`source ~/.bashrc`
您的 Linux command alias 现在每次启动新的终端会话时都将可用。

移除别名
如果您不再需要别名，可以使用 unalias 命令将其删除。这将从当前会话中删除它。

`unalias ll`

- `exit`

`logout`

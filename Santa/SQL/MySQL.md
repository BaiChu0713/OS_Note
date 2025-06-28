# MySQL基本操作

## SQL基本语法

> SQL是一种结构化编程语言

基础SQL指令通常是以行为单位

SQL指令需要语句结束符，默认是英文分号：`;`、`\g`、`\G`

`\G`：主要用于查询数据，立体展示结果

SQL指令类似自然语言
编写的SQL中如果用到了关键字或者保留字，需要使用反引号` `` `来包裹，让系统忽略

SQL 基础操作类型：

1. 库操作——数据库相关操作

2. 表操作——数据表（字段）相关操作

3. 数据操作——数据相关操作


### 关于结构

`create 结构类型 结构名 结构描述;`

`show 结构类型（复数）;`

`show create 结构类型 结构名;`

### 数据表

 `insert into 表名 values`  新增数据

`select from 表名`  查看数据

`update 表名 set`  更新数据

`delete from 表名`  删除数据


## SQL库操作

### create

> 创建数据库

> `create database 数据库名字 [数据库选项];`

数据库的创建通常是一次性的

创建数据库的语法包含几个部分

关键字： create database

数据库名字： 自定义名字
数字、字母和下划线组成
不区分大小写

数据库选项：非必须的规定
- 字符集：`charset` /`character set` 字符集。非必须，默认继承`DBMS`
- 校对集：`collate` 校对集。非必须，依赖字符集


create后在磁盘指定存放处产生一个文件夹

eg:
```
create database db_1;

create database db_2 charset utf8MB4;

create database db_3 charset utf8MB4 collate utf8mb4_general_ci;
```


### show

>  查看数据库

> `show databases;`

> `show create database 数据库名字;`

通过客户端指令来查看已有数据库

数据库的查看是根据用户权限限定的

1. 查看数据库分为两种方式

  - 查看全部：`show databases;`

  - 查看具体创建指令：`show create database 数据库名字;`

2. 查看数据库的目的和应用

  开发人员确认数据库是否存在

  数据库管理员维护

eg:
```
show databases;

show create database db_1;
```

### use

> 使用数据库

> `use 数据库名字;`

指在进行具体SQL指令之前，让系统知道操作针对的是哪个数据库


目的：

  - 让系统知道后续SQL指令都是针对当前选择的数据库

  - 简化后续SQL指令的复杂度（如果不指定数据库，那么所有的SQL操作都必须强制指定数据库名字）

### alter

> 修改数据库

> `alter database 数据库名字 库选项 `

修改数据库的相关库选项

使用较少，通常是删除后新增

数据库名字不可修改（老版本可以）
  - 先新增
  - 后迁移
  - 最后删除

数据库修改分为两个部分（库选项）
  - 字符集
  - 校对集

eg.
```
alter database db_2 charset gbk;//修改数据库字符集

alter database db_3 charset gbk collate gbk_chinese_ci;//修改数据库校对集（必须同时改变字符集）
```

### drop

> 删除数据库

> `drop database db_1 `

将当前已有数据库删除



**数据库的删除不可逆**

- 删除会清空当前数据库内的所有数据表（表里数据一并删除）

- 删除数据库会将对应的文件夹从磁盘抹掉

一般不建议删除

数据库的操作通常是一次性的，即在进行业务代码开展之前将数据库维护好


## SQL表操作

## SQL数据操作

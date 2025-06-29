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

### create

> 创建数据表

- 表的创建需要**指定存储的数据库**

  - 先使用数据库：`use 数据库名字`

- 字段至少需要指定名字、类型

- 数据库表不限定字段数量

  - 每个字段间使用逗号,分隔
  - 最后一个字段不需要逗号


- 表可以指定表选项（都有默认值）

存储引擎：`engine [=] 具体存储引擎`

字符集：`[default] charset 具体字符集（继承数据库）`

校对集：`collate（继承数据库）`

eg.

1.指定数据库 创建简单数据表

```
create table db_2.t_1(
	name varchar(50)
);
```

2.创建数据表——多字段

使用数据库（进入数据库环境）
```
use db_2;
create table t_2(
    name varchar(50),
    age int,
    gender varchar(10)
);
```

3.创建数据表——含表选项
```
create table t_3(
	name varchar(50)
)engine Innodb charset utf8MB4;
```

数据表的创建与字段是同时存在的

创建数据表方式：
  1. 数据表前置顶数据库(数据库名.表名)
  2. 进入数据库环境

如果想创建一个与已有表一样的数据表，可使用`create table 表名 like 数据库名字.表名`

一张数据表用来存一组相关数据

**存储引擎**是指数据存储和管理的方式

#### 存储引擎类型
|类型|特性|
|-|-|
|InnoDB|默认存储引擎，支持事务处理和外键，数据统一管理|
|Mylsam|不支持事务和外键，数据、表结构、索引独立管理，MySQL5.6以后不再维护|

### show
>显示数据表

>`show tables;`

>`show tables from db_3;`

>`show tables like '%something';//_表示匹配一个字符（固定位置），%表示匹配N个字符`

>`show create table t_1;`

验证数据表是否存在
/
验证数据表的创建指令是否正确

- 显示所有数据表`show tables [from 指定数据库];`

- 显示部分s`how tables like 'pattern'; `

  - 匹配模式

    - `_`匹配单个字符
    - `%`匹配不限量字符（常用于模糊查询）

- 在显示数据的时候可以使用不同的语句结束符

  - `\g`与普通分号无区别
  - `\G`纵向显示列数据

### desc

> 查看数据表

> `desc 表名；`

> `describe 表名;`

> `show columns from 表名;`

指查看数据表中的具体结构

三种效果一样

### rename

> 更改数据表

> 修改表名r`ename table 表名 to 新表名`

> 修改表选项`alter table 表名`

 修改表名字和表选项

较少使用更改数据表，数据表应该在创建时就定义好

eg.

1.`rename table t_1 to t1;
`——要跨库修改的话，需要使用数据库名.表名

2.`alter table t1 charset utf8;`

### alter
>更改字段

> 指针对表创建好后，里面字段的增删改

字段操作还有位置处理

通常是在**表已经存在数据后**进行

#### 新增字段

> 给已有表追加一个字段

字段的新增必须同时存在字段类型

必须指定字段类型，追加默认实在所有字段以后

`alter table 表名 add [column] 字段名 字段类型 [字段属性] [字段位置]`


eg.
`alter table t_3 add age int;`增加字段age

`alter table t_3 add column nickname varchar(10);`增加字段nickname

#### 字段位置
> `alter table 表名 字段操作 字段位置;`


字段放到某个指定字段的位置

字段位置是配合字段操作的（新增、修改）

类型：`first`;`after 已存在的字段名`

eg.

`alter table t_3 add id int first; `增加int字段 且放到最前面

`alter table t_3 add card varchar(18) after name;`t_3表name字段后增加一个身份证字段card

#### 更改字段名
> 指对已经存在的字段名进行修改

>`alter table 表名 change 原字段名 新字段名 字段类型 [字段属性] [位置]
示例`

通常只是修改字段名字，但是也必须跟随类型

字段名修改change其实也可以修改字段类型、属性和位置，但是通常不使用（专人专事）

#### 修改字段
>修改字段的相关信息

> `alter table 表名 modify 字段名 字段类型 [字段属性] [位置]；`


- 字段类型修改
- 字段属性修改
- 字段位置修改

#### 删除字段
> `alter table 表名 drop 字段名;`

> 即将某个不要的字段从表中剔除

字段删除在删除字段名的同时会删除字段对应的数据，而且不可逆

***
以上是数据表的结构操作

 数据表结构的维护通常是一次性的，在业务开展前尽可能好的设计好数据表，而不要后期再进行其他维护

## SQL数据操作

### 新增数据
>将数据插入到数据表永久存储

数据以行（row）为存储单位，实际存储属于字段（field）存储数据

- 插入方式

  - 全字段插入`insert into 表名 values(字段列表顺序对应的所有值);`

      值列表必须与字段列表顺序一致

      值列表的每个数据类型必须与字段类型一致

  - 部分字段插入`insert into 表名 (字段列表) values(字段列表对应的值顺序列表);`

      字段列表可以顺序随意

      值列表必须与指定的字段列表顺序一致

      值列表元素的类型必须与字段列表的类型一致


eg.
```  
插入完整数据
  insert into t_3 values(1,'440111200011111101','Jim','Green');

根据字段插入数据
  insert into t_3 (id,sfz,name) values(2,'441000200011111211','Tom');
  ```


### 查看数据
>将表中已经存在的数据按照指定的要求显示出来

`select *|字段列表 from 表名;`

查到的数据显示出来是一张二维表

数据显示包含字段名和数据本身

- 数据查看的情况

  1. 查看全部：`select *` （*叫做通配符）
  2. 查看部分：`select 字段列表`（建议）

eg.
```
select * from t_3;

select name,sfz from t_3;

select * from t_3 where id = 1;
```

### 更新数据

更新某个已有字段的值

根据条件更新某些数据，而不是全部记录都更新

`update 表名 set 字段 = 新值[,字段 = 新值] [where条件筛选];`

eg.
```
update t_3 set sfz = '440100200010100001';

update t_3 set name = 'Lily',sfz = '440100200010100002' where id = 1;
```

通常是限定条件更新（一般不会更新全部）

### 删除数据

数据从已有数据表中清除（针对的是记录record）

是一种不可逆操作

`delete from 表名 [where条件];`

//where相当于 if


eg.
`delete from t_3 where id = 2;
`

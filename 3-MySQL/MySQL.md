# MySQL

## Overview

* 为server-side设计的, 使用最广泛的DB server
* 能承受高concurrency访问

<br>

## Setup

* Download MySQL from official website

  * After installation,  set a password for the `root` user

* `> ls /usr/local/mysql`

  * `data/`: 用来保存数据文件和log文件
  * `bin/`: 保存了MySQL常用的command工具和管理工具
  * `docs/` and `man/`: 保存了MySQL的help documentations

* Put `my.cnf` under `/etc` to set the encoding to UTF-8

* `System Preference` -> `MySQL` -> `Configuration`

  * Set the configuration file location to the above one

* Add the following to `.bashrc` and `.zshrc`:

  ```bash
  export PATH="/usr/local/mysql/bin:$PATH"
  ```

<br>

## Start/Stop MySQL Server

* `System Preference` -> `MySQL`
  * `Initialize Database`
  * `Start MySQL Server` / `Stop MySQL Server`

***

Note that `mysqld` is the command-line tool for operating MySQL server

***

<br>

## MySQL Command-Line Interface

```bash
> mysql -u root -p  # Establish a connection (open a client session), and enter MySQL interactive shell
```

***

**[Inside the interactive shell] Common commands**

```mysql
show variables;  -- Show all the system variables and status variables
```

```mysql
show databases;  -- Show all the databases on the MySQL server

create database if not exists test;  -- Create a database called "test" if it doesn't exist

use test;  -- Enter "test" database

show tables;  -- Show all the tables in "test" database

show views;  -- Show all the views in "test" database

source some_codes.sql;  -- Import (Execute) the SQL codes in "some_codes.sql"

describe some_table;  -- Show the structure (columns) of "some_table" table

drop database if exists test;  -- Delete a database called "test" if it exists
```

***

<br>

## Python Support

* `mysql-connector-python`
  * Official Python support by Oracle Inc.
  * Worst performance  = =
* `PyMySQL`

Open
# PostgreSQL

## Overview

* 为servide-side设计的, 使用普及度呈上升趋势
* 能承受高concurrency访问

<br>

## Setup

* Download PostgreSQL from `homebrew`

  `> brew install postgresql@9.6`

<br>

## Start/Stop PostgreSQL Server

<u>Note that `postgres` and `pg_ctl` are both command-line tools for operating PostgreSQL server</u>

*(相当于MySQL的`mysqld`)*

**Start PostgreSQL Server**

```bash
> postgres -D /usr/local/var/postgresql@9.6/
```

or

```bash
> pg_ctl -D /usr/local/var/postgresql@9.6/ start
```

Stop PostgreSQL server**

```bash
> pg_ctl -D /usr/local/var/postgresql@9.6/ stop
```

<br>

## PostgreSQL Command-Line Interface

```bash
> psql -l  # Show all the databases on the PostgreSQL server
```

```bash
> createdb test  # Create a database called "test"
> psql -l  # Now "test" database should show up
> psql test  # Connect to "test" database and enter the interactive shell
```

***

**[Inside the interactive shell] Common commands**

```
\l  -- Show all the databases on the PostgreSQL server

\dt  -- Show all the tables in "test" database

\d some_table  -- Show the structure (columns) of "some_table" table

\i some_codes.sql  - Import (Execute) the SQL codes in "some_codes.sql"

\c 
```

***

```bash
> dropdb test  # Delete a database called "test"
```

<br>

## Python Support

`psycopg2`
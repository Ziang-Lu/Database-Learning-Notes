# PostgreSQL

## Overview

* 为servide-side设计的, 使用普及度呈上升趋势
* 能承受高concurrency访问

<br>

## Setup

* Download and install PostgreSQL from `homebrew`

  `> brew install postgresql@9.6`

* Add the following to `.bashrc` and `.zshrc`:

  ```bash
  # Setting for icu4c
  export PATH="/usr/local/opt/icu4c/bin:$PATH"
  export PATH="/usr/local/opt/icu4c/sbin:$PATH"
  export LDFLAGS="-L/usr/local/opt/icu4c/lib"
  export CPPFLAGS="-I/usr/local/opt/icu4c/include"
  export PKG_CONFIG_PATH="/usr/local/opt/icu4c/lib/pkgconfig"
  
  # Setting for PostgreSQL
  export PATH="/usr/local/opt/postgresql@9.6/bin:$PATH"
  export LDFLAGS="-L/usr/local/opt/postgresql@9.6/lib"
  export CPPFLAGS="-I/usr/local/opt/postgresql@9.6/include"
  export PKG_CONFIG_PATH="/usr/local/opt/postgresql@9.6/lib/pkgconfig"
  ```

<br>

## Start/Stop PostgreSQL Server

<u>Note that `postgres` and `pg_ctl` are both command-line tools for operating PostgreSQL server</u>

*(相当于MySQL的`mysqld`)*

**Start PostgreSQL Server**   **(Daemon process)**

```bash
$ postgres -D /usr/local/var/postgresql@9.6/
```

or

```bash
$ pg_ctl -D /usr/local/var/postgresql@9.6/ start
```

**Stop PostgreSQL server**

```bash
$ pg_ctl -D /usr/local/var/postgresql@9.6/ stop
```

<br>

## PostgreSQL Command-Line Interface

```bash
$ createuser -s postgres  # Create a superuser "postgres" for later use
```

***

```bash
$ psql -l  # Show all the databases on the PostgreSQL server
```

```bash
$ createdb test  # Create a database called "test"
$ psql -l  # Now "test" database should show up
$ psql test  # Connect to "test" database and enter the interactive shell
```

***

**[Inside the interactive shell] Common commands**

```bash
\l  # Show all the databases on the PostgreSQL server

\dt  # Show all the tables in "test" database

\dv  # Show all the views in "test" database

\d some_table  # Show the structure (columns) of "some_table" table

\i some_codes.sql  # Import (Execute) the SQL codes in "some_codes.sql"

\x  # Toggle expanded output

\c db_name  # Change connection to another DB

\q  # Quit the interactive shell
```

***

```bash
$ dropdb test  # Delete a database called "test"
$ dropuser postgres  # Delete the previously created superuser "postgres"
```

<br>

## Python Support

`psycopg2`

(Check out `Online Forum App/` folder for a web application written with `Flask` and `PostgreSQL` DB)


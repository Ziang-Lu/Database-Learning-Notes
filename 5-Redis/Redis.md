# Redis

Key-value store

适用于要存储的data type相对简单, 但需要极高的retrieve和insert速度的嵌入式场景

## Overview

* 存储的data有结构, 用来存储`String`, `List` (linked-list), `Hash` (hash map), `Set` (hash set), `SortedSet` (tree set) 等data type
* => 常用作data structure server

<br>

## Setup

* Download

  `> cd /usr/local/`

  `> wget http://download.redis.io/releases/redis-5.0.3.tar.gz`

  `> tar xzf redis-5.0.3.tar.gz`

* Install

  `> redis-5.0.3`

  `> make`

  `> make test`

  `> make PREFIX=/usr/local/redis install`

  Add the following to `.bashrc` and `.zshrc`:

  ```bash
  export PATH="/usr/local/redis/bin:$PATH"
  ```

* Copy configuration file

  `> cd /usr/local/redis`

  `> scp ../redis-5.0.3/redis/redis.conf .`

<br>

## Start/Stop Redis Server

| Mode            | Start Redis server                                           | Stop Redis server      |
| --------------- | ------------------------------------------------------------ | ---------------------- |
| Non-daemon mode | `> redis-server /usr/local/redis/redis.conf`                 | `ctl-C`                |
| Daemon mode     | In `/usr/local/redis/redis.conf`, set the following:<br>`daemonize yes` | `kill -9 <daemon pid>` |

**打开Redis server默认会打开16个DB, 编号为0-15**

<br>

## Redis Command-Line Interface

```bash
> redis-cli  # 默认进入DB-0
```

***

**[Inside the interactive shell] Common commands**

```bash
select 2  # Use DB-2


# COMMANDS FOR KEYS IN GENERAL

keys *  # By using the wildcard "*", show all the keys in the current DB
keys o*  # ... show all the keys that start with an "o" in the current DB
keys ???  # By using the wildcard "?", show all the keys that are exactly 3 characters long in the current DB
keys on[aew]  # By using the wildcard "[]", show all the keys that start with "on" followed by any one character among "a"/"e"/"w" in the current DB

exists key  # Check whether "key" exists
type key  # Show the type of the value at "key"

move key 3  # Move "key" to DB-3

del key anotherkey  # Delete the specified keys

flushdb  # Delete all the keys in the current DB


# COMMANDS FOR STRING

# (1) Setting

set key "foo" nx  # Store the mapping "key" -> "foo", but only set when "key" doesn't already exist
set key "foo" xx  # ... but only set when "key" already exists => So this is equivalent to updating the string at "key"
mset key "foo" anotherkey "bar"  # Store multiple mappings "key" -> "foo" and "anotherkey" -> "bar"
msetnx key "foo" anotherkey "bar"  # ... but only set when all the specified keys don't already exist

# setrange
set key "hello"
setrange key 2 "xx"  # Update a range of the string at "key", starting from index-2 (starting from 0)
get key  # "hexxo"

append key "additional"  # Append "additional" to the end of the string at "key"

# setbit
set letter "A"  # "A" is stored as ASCII code 65 (0x 0100 0001)
# To change "A" to its lowercase, we need to increment the ASCII code by 32 (0x 0010 0000), i.e., change the index-2 bit from 0 to 1
setbit letter 2 1  # Set the index-2 bit to 1
get letter  # "a"

# (2) Getting

get key  # Get the string at "key"
mget key anotherkey  # Get the strings at "key" and "anotherkey"
getrange key 1 4  # Get a range (from index-1 to index-4) of the string at "key", inclusive

strlen key  # Get the length of the string at "key"

# (3) Operating as 

# Increment / Decrement operations
set key 10
incr key  # Increment the string (interpreted as integer) at "key" by 1
incrby key 5  # ... by 5
incrbyfloat key 1.5  # Increment the string (interpreted as floating-number) at "key" by 1.5
decr key  # Decrement ...
decrby key 5  # Decrement ...


# COMMANDS FOR LIST

lpush key "a" "b"  # Push the specified values to the left of the linked-list at "key"
rpush key "c" "d"  # ... to the right of ...

linsert key before|after "a" "new_a"  # Insert "new_a" before|after the first "a" in the linked-list at "key"

lindex key 2  # Show the value at index-2 of the linked-list at "key"
lrange key 0 -1  # Show a range (from index-0 to last index) of the linked-list at "key", inclusive
# "b", "a", "c", "d"

llen key  # Get the length of the linked-list at "key"

ltrim key 1 3 # Trim the linked-list at "key" to a range (from index-1 to index-3), inclusive

lpop key  # Pop the left-most value from the linked-list at "key"
rpop key  # ... right-most ...

lrem key 5 "a"  # Remove at most 5 "a" from the left of the linked-list at "key"
lrem key -5 "a"  # ... from the right of ...
```

***

<br>

## Redis Commands

Full command lists:

* About keys in general

  https://redis.io/commands#generic

* About `String`

  https://redis.io/commands#string

* About `List` (linked-list)

  https://redis.io/commands#list

* About `Hash` (hash map)

  https://redis.io/commands#hash

* About `Set` (hash set)

  https://redis.io/commands#set

* About `SortedSet` (tree set)

  https://redis.io/commands#sorted_set

<br>

## Python Support

`redis-py`
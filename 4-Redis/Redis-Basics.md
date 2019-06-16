# Redis Basics

**Key-value store (键-值存储)**

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

<br>

## Redis Commands

Full command lists:

* About connection

  ```bash
  select 2  # Change to DB-2
  
  swapdb 1 3  # Swaps all the data in DB-2 and DB-3
  # => All the clients connected with DB-2 will immediately see the new data, exactly like all the clients connected with DB-3 will see the data that was formerly of DB-2.
  ```
  
* About keys in general

  ```bash
  # (1) Check keys
  
  dbsize  # Return the number of keys in the currently-selected DB
  
  keys *  # By using the wildcard "*", show all the keys in the current DB
  keys o*  # ... show all the keys that start with an "o" in the current DB
  keys ???  # By using the wildcard "?", show all the keys that are exactly 3 characters long in the current DB
  keys on[aew]  # By using the wildcard "[]", show all the keys that start with "on" followed by any one character among "a"/"e"/"w" in the current DB
  
  # (2) Check one key's information
  
  exists key  # Check whether "key" exists
  type key  # Show the type of the value at "key"
  
  # (3) Move keys
  
  move key 3  # Move "key" to DB-3
  
  # (4) Delete keys
  
  del key anotherkey  # Delete the specified keys
  flushdb  # Delete all the keys in the current DB
  flushall  # Delete all the keys in all the DBs
  
  # (5) Keys lifetime
  expire key 50  # Set the lifetime of "key" to be 50 seconds
  pexpire key 5000  # Set the lifetime of "key" to be 5000 milliseconds
  ttl key  # Show the time-to-live (remaining lifetime) of "key", in seconds
  pttl key  # Show the time-to-live (remaining lifetime) of "key", in milliseconds
  ```

  https://redis.io/commands#generic

* About `String`

  ```bash
  # (1) String setting
  
  set key "foo" nx  # Store a string "foo" at "key", but only set when "key" doesn't already exist
  set key "foo" xx  # ... but only set when "key" already exists => So this is equivalent to updating the string at "key"
  mset key "foo" anotherkey "bar"  # Store a string "foo" at "key" and "bar" at "anotherkey"
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
  # Combining "setbit" and "getbit", we can use a string as an O(1) random-access arrays.
  # Check out "bitmap_for_user_login.py" for using strings (together as a bitmap) to keep user logins and find active users
  
  # (2) String getting
  
  get key  # Get the string at "key"
  mget key anotherkey  # Get the strings at "key" and "anotherkey"
  getrange key 1 4  # Get a range (from index-1 to index-4) of the string at "key", inclusive
  
  strlen key  # Get the length of the string at "key"
  
  # (3) String operated as number
  
  # Increment / Decrement operations
  set key 10
  incr key  # Increment the string (interpreted as integer) at "key" by 1
  incrby key 5  # ... by 5
  incrbyfloat key 1.5  # Increment the string (interpreted as floating-number) at "key" by 1.5
  decr key  # Decrement ...
  decrby key 5  # Decrement ...
  ```

  https://redis.io/commands#string

* About `List` (linked-list)

  ```bash
  # (1) Insertion
  
  lpush key "a" "b"  # Push the specified values to the left of the linked-list at "key"
  rpush key "c" "d"  # ... to the right of ...
  
  linsert key before|after "a" "new_a"  # Insert "new_a" before|after the first "a" in the linked-list at "key"
  
  lindex key 2  # Show the value at index-2 of the linked-list at "key"
  lrange key 0 -1  # Show a range (from index-0 to last index) of the linked-list at "key", inclusive
  # "b", "a", "c", "d"
  
  # (2) Retrieval
  
  llen key  # Get the length of the linked-list at "key"
  
  ltrim key 1 3 # Trim the linked-list at "key" to a range (from index-1 to index-3), inclusive
  
  # (3) Deletion
  
  lpop key  # Pop the left-most value from the linked-list at "key"
  rpop key  # ... right-most ...
  
  lrem key 5 "a"  # Remove at most 5 "a" from the left of the linked-list at "key"
  lrem key -5 "a"  # ... from the right of ...
  lrem key 0 "a"  # Remove all "a" from the linked-list at "key"
  ```

  https://redis.io/commands#list

* About `Hash` (hash map)

  ```bash
  # (1) Insertion
  
  hset key name "Kevin"  # Store a mapping "name" -> "Kevin" in the hash map at "key"
  hmset key name "Kevin" sex "M"  # Store mappings "name" -> "Kevin", "sex" -> "M" in the hash map at "key"
  
  # (2) Retrieval
  
  hexist key name  # Check whether the field "name" exists in the hash map at "key"
  
  hget key name  # Get the value of field "name" in the hash map at "key"
  hmget key name sex # Get the values of the fields "name" and "set" in the hash map at "key"
  hgetall key  # Get all the mappings in the hash map at "key"
  hkeys key  # Get all the fields in the hash map at "key"
  hvals key  # Get all the values in the hash map at "key"
  
  hlen key  # Get the number of mappings in the hash map at "key"
  
  # (3) Deletion
  hdel key sex  # Delete the field "name" in the hash map at "key"
  
  # (4) Value operated as number
  hincrby key age 10  # Increment the value of the field "age" in the hash map at "key" by 10
  hincrfloat key age 2.5  # ... by 2.5
  ```

  https://redis.io/commands#hash

* About `Set` (hash set)

  ```bash
  # (1) Insertion
  
  sadd key "Kevin" "John"  # Store the values "Kevin" and "John" in the set at "key"
  
  # (2) Retrieval
  
  sismember key "John"  # Check whether the value "John" exists in the set at "key"
  
  srandmember key  # Get a random value from the set at "key"
  smembers key  # Get all the values from the set at "key"
  
  scard key  # Get the number of values in the set at "key"
  
  # (3) Deletion
  
  spop key "Kevin"  # Pop out the value "Kevin" from the set at "key"
  srem key "Kevin" "John"  # Delete the values "Kevin" and "John" from the set at "key"
  ```

  https://redis.io/commands#set

* About `SortedSet` (tree set)

  ```bash
  # (1) Insertion
  
  zadd key 6 "Lily" 8 "Lucy" 7 "Kevin"  # Store the values "Lily" with score 6, "Lucy" with score 8, and "Kevin" with score 7 in the sorted set at "key"
  
  # (2) Retrieval
  
  zrange key 1 3 [withscores]  # Get a range (from rank-1 to rank-3 in ascending order) from the sorted set at "key", inclusive, [together with the corresponding score]
  zrevrange key 1 3 [withscores]  # ... in descending order ...
  zrangebyscore key 10 15 [withscores] limit 2 3  # Get a range (from score 10 to score 15 in ascending order) from the sorted set at "key", inclusive, [...], offset 2 values and limit the result to the first 3 values
  
  zrank key "Lucy"  # Calculate the rank of "Lucy" (ascending order) in the sorted set at "key"
  zrevrank key "Lucy"  # ... (descending order) ...
  
  zcard key  # Get the number of values in the sorted set at "key"
  zcount key 10 15  # Count the number of values with score [10, 15] in the sorted set at "key"
  
  # (3) Deletion
  zrem key "Lily" "Kevin"  # Delete the values "Kevin" and "John" from the sorted set at "key"
  zremrangebyrank key 1 3  # Delete a range (from rank-1 to rank-3 in ascending order) from the sorted set at "key", inclusive
  zremrankebyscore key 10 15  # ... (from score 10 to score 15 in ascending order) ...
  ```

  https://redis.io/commands#sorted_set

<br>

## Python Support

`redis-py`

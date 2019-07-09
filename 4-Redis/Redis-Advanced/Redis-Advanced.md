# Redis Advanced Topics

## Redis Queued Commands ("Transaction"?)

Check out https://redis.io/topics/transactions

```bash
set ziang 500
set mama 300

multi  # Multiple commands incoming (create a command queue)

# Simulate that "ziang" transfers 100 to "mama"
decrby ziang 100
# QUEUED
incrby mama 100
# QUEUED
# From the returned messages we can know that actually the commands are actually queued, waiting to be executed as a whole.

exec  # Execute all the queued commands
```

------

**NOTE!!!!!**

During the above process, there may be <u>two types of errors</u>:

1. <u>Syntax error</u> during queueing commands

   `sljvnskvnkjs svss`

   Redis is <u>able to detect that syntax error</u> during queueing commands, and will return an error message for the wrong-syntax command.

   When `exec`, Redis will also return an error message, and simply <u>discard the entire transaction</u>.

2. <u>Other errors</u> during queueing commands

   `sadd ziang rocks`

   *Correct syntax, but invalid command that doesn't work*

   Redis <u>cannot detect these kinds of errors</u>, and will queue this command.

   When `exec`, Redis will <u>execute the queued commands one by one, skipping the errored ones, but the successful ones still take effect</u>.

   *e.g., Assume there are 3 queued commands: the first 2 succeeded and the last one failed. Then the first 2 commands still take effect, while only discarding the last one.*

=> Thus, this mechanism is <u>NOT really a traditional "transaction"</u>, since it cannot be rolled back to the last `exec`.

------

```bash
discard  # Discard all the queued commands (delete the command queue)
```

Check out `redis_transaction.py`

<br>

### Redis Transaction - (Optimistic) Locking Mechanism

#### Scenario: Ticket-booking (But before `exec`, interfered by some other client)

```bash
set ziang 500
set tickets 1
```

"ziang" wants to book the only remaining ticket:

```bash
multi
decrby ziang 100
decr tickets

# exec
# Once "ziang" EXEC, Redis will not process any other requests in the middle of execution, and thus the entire transaction is atomic and will work as expected.
```

------

But before "ziang" `exec`, some other client booked this tickets:

```bash
# Anther Redis client booked the only remaining ticket.
decr tickets

get tickets
# 0
```

------

Then "ziang" EXEC:

```bash
exec

get ziang tickets
# 400
# -1
```

We can see that the `ticket` now becomes `-1`, so the booking becomes invalid.

#### Solution: Redis (Optimistic) Locking Mechanism

```bash
watch tickets  # Watch the key "tickets" => If during the further "exec", any watched key has been changed by some other Redis client, then the entire transaction is discarded.

multi
decrby ziang 100
decr tickets
```

------

```bash
# Anther Redis client booked the only remaining ticket.
decr tickets

get tickets
# 0
```

------

Then "ziang" `exec`:

```bash
exec
# (nil)
# indicating that some watched key has been changed, so the entire transaction is discarded.
```

Check out `redis_transaction_optimistic_lock.py`

#### => Application

- **订票系统 (如上)**

- **抢单、"秒杀"的实现**

  把<u>对某件商品的data全部操作放进一个transaction, 再加上optimistic lock</u>, 即可<u>避免data inconsistency问题 (race condition)</u>

<br>

## (Distributed System) Distributed Locking Mechanism (Using Redis)

For a distributed scenario, we can <u>use the Redis's single-threaded feature</u> to

* Implement a **naive** distributed lock

  <u>Simple but imperfect</u>

  => <u>In NOT so high-concurrent scenarios, this works just fine.</u>

* Use a **third-party library**

  <u>Complex but perfect</u>

  => <u>Works for high-concurrent scenarios</u>

  Check out `distributed_locking.py`

<br>

## Redis Data Persistance (数据持久化)

**RDB Snapshotting Data Persistence (RDB快照 数据持久化)**

vs

**AOF (Append-Only-File) Logging Data Persistence (AOF日志 数据持久化)**

(Including aggregated commands on some key "inverted" => single command on that key ("一步到位"))

Check out https://redis.io/topics/persistence

<br>

## Redis Replication (主从复制)

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/4-Redis/Redis-Advanced/master-slave.png?raw=true">

Check out https://redis.io/topics/replication and `redis.conf` "REPLICATION" section for more details

Example master/slave set-up:

```bash
mkdir redis_folder
cd redis_folder
mkdir pidfile
mkdir data

# We want Slave-1 to carry the work of RDB snapshotting to disk and AOF.

# Set up Master
scp /usr/local/redis/redis.conf redis_master.conf
# In the configuation file:
##### (-> Turned to Slave-1)
# Turn off RDB snapshotting to disk
# save 900 1
# save 300 10
# save 60 10000
# Turn off AOF
appendonly no
#####

# Set up Slave-1
scp /usr/local/redis/redis.conf redis_slave1_6380.conf
# In the configuration file:
replicaof localhost 6379
# Set the PID file
pidfile ./pidfile/redis_6380.pid
# Change the port
port 6380
##### (Work from Master)
# Keep RDB snapshotting to disk on
# Keep AOF on
#####
# When the partial/full synchronization with the master is in progress, we let the slave refuse to serve the out-of-date data (currently on the slave).
replica-serve-stale-data no
# For better read-only security, disable "config" command
rename-command CONFIG ""

# Set up Slave-2
scp /usr/local/redis/redis.conf redis_slave1_6381.conf
# Set the PID file
pidfile ./pidfile/redis_6381.pid
# Change the port
port 6381
#####
# Turn off RDB snapshotting to disk (-> Turned to Slave-1)
# save 900 1
# save 300 10
# save 60 10000
# Turn of AOF
appendonly no
#####
# When the partial/full synchronization with the master is in progress, we let the slave refuse to serve the out-of-date data (currently on the slave).
replica-serve-stale-data no
# For better read-only security, disable "config" command
rename-command CONFIG ""
```

Start the master/slave servers:

```bash
> redis-server redis_maser.conf
> redis-server redis_slave1_6380.conf
> redis-server redis_slave2_6381.conf
```

Simple demo:

```bash
> redis-cli
set title software_engineer
# OK

> redis-cli -p 6380
get title
# "software_engineer"
set title "data_scientist"
# (error) READONLY You can't write against a read only replica.
```

***

**Disk vs. Diskless Replication**

When doing <u>full synchronization</u>, an RDB file is transmitted from the master to the replicas. The transmission can happen in two different ways:

* Disk-backed

  1. The master creates a new process that <u>writes the RDB file on disk</u>.
  2. Later <u>the file is transmitted</u> by the parent process <u>to the replicas</u>.

  While the RDB file is generating, more replicas requesting a full synchronization can be queued.

  => Once the file finished its generation, it is transmitted to all the replicas, including the queued ones.

  ***

  e.g.

  1. Slaves S1, S2 and S3 replicas request full synchronization to the master M.
  2. M creates a new process that writes the RDB file on disk.
  3. While the RDB file is generating, more replicas S4 and S5 request a full synchronization.
  4. S4 and S5 are queued.
  5. Once the file finished its generation, it is transmitted to all the slaves, i.e., S1, S2, S3, S4 and S5.

  ***

* Diskless

  The master creates a new process that <u>directly write RDB file to the requesting replica sockets</u>, without touching the disk at all.

  Once the transfer starts, new replicas arriving will be queued, and only when the current transfer terminates, will a new transfer start.

  ***

  e.g.,

  1. Slaves S1, S2 and S3 replicas request full synchronization to the master M.
  2. M creates a new process that directly write RDB file to S1, S2 and S3.
  3. While the master is transmitting the file, more replicas S4 and S5 request a full synchronization.
  4. Only when the transfer terminates will a new transfer to S4 and S5 start

  ***

  Diskless replication can be turned on by setting:

  ```bash
  repl-dickless-sync yes  # Turn on diskless replication
  ```

  Since once a transfer starts, the master cannot serve newly arriving replicas, which will be scheduled for the next transfer,

  => We can configure the master to wait for some seconds, in order to let more replicas arrive in time, so that the master can do the transfer all at one.

  ```bash
  repl-dickless-sync-delay 5  # Let the master wait 5 seconds, in order to let more replicas arrive in time
  ```

***

<br>

## Publish-Subscribe Mechanism

Check out https://redis.io/topics/pubsub

```bash
# Redis client-1 subscribes to "news" channel.
subscribe news
# -----
# 1) "message"
# 2) "news" [channel]
# 3) "It's a good day!" [message content]
# -----

# Redis client-2 subscribes to "news" channel.
subscribe news
# -----
# 1) "message"
# 2) "news" [channel]
# 3) "It's a good day!" [message content]
# -----

# Redis client-3 publishes to "news" channel with some content.
publish news "It's a good day!"
# (integer) 2, indicating that 2 clients receives this message.
```

We can also use pattern for subscribing:

```bash
# Redis client-1 subscribes to any channel starting with "music".
psubscribe music*
# -----
# 1) "pmessage"
# 2) "music*" [pattern]
# 3) "music_radio" [specifc channel]
# 4) "Check out this awesome song!" [message content]
# -----

# Redis client-2 subscribes to any channel ending with "radio".
psubscribe *radio
# -----
# 1) "pmessage"
# 2) "music*" [pattern]
# 3) "music_radio" [specifc channel]
# 4) "Check out this awesome song!" [message content]
# -----

# Redis client-3 publishes to "music_radio" channel with some content.
publish music_radio "Check out this awesome song!"
# (integer) 2
```

------

**Note!!!!!**

The <u>Publish-Subscribe mechanism is across DBs (i.e., a channel is across DBs)</u>: publishing on DB-10 will be heard by a subscriber on DB-1.

------

Other commands include:

```bash
# "pubsub" is a group of commands used to inspect the state of the Pub/Sub subsystem.
pubsub channels [pattern]  # List the currently active channels [matching the pattern]
# Active channel: A channel with one or more subscribers

pubsub numsub [channel-1 ... channel-N]  # Returns the number of subscribers to the specified channels

pubsub numpat  # Returns the number of subscriptions to all the patterns
```

Check out `pub_sub.py`


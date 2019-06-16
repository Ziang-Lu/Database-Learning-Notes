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
# From the returned message we can know that actually the commands are actually queued, waiting to be executed as a whole.

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

***

*****Note!!!!!**

The <u>Publish-Subscribe mechanism is across DBs (i.e., a channel is across DBs)</u>: publishing on DB-10 will be heard by a subscriber on DB-1.

***

Other commands include:

```bash
# "pubsub" is a group of commands used to inspect the state of the Pub/Sub subsystem.
pubsub channels [pattern]  # List the currently active channels [matching the pattern]
# Active channel: A channel with one or more subscribers

pubsub numsub [channel-1 ... channel-N]  # Returns the number of subscribers to the specified channels

pubsub numpat  # Returns the number of subscriptions to all the patterns
```

Check out `pub_sub.py`
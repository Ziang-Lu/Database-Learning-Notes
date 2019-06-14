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

Check out ""

<br>

## Redis (Optimistic) Locking Mechanism

### Scenario: Ticket-booking (But before `exec`, interfered by some other client)

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

### Solution: Redis (Optimistic) Locking Mechanism

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

### => Application

- **订票系统 (如上)**
- **抢单、"秒杀"的实现**

<br>

## Publish-Subscribe Mechanism
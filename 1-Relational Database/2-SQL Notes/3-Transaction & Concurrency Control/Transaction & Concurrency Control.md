# Transaction (事务) & Concurrency Control (并发控制)

## Transaction

"ACID"

* Atomicity 原子性

  一个transaction是一个不可分割的工作单位: 一个Transaction中包括的操作要么都成功, 要么都不成功.

* Consistency 一致性

  一个transaction必须是使数据库从一个一致性状态变到另一个一致性状态.

  *这与atomicity是密切相关的*

* Isolation 隔离性

  一个transaction的执行不能被其他transactions干扰, 即一个事务内部的操作及使用的数据对并发的其他事务是隔离的, 并发执行的各个事务之间不能互相干扰

* Durability 持久性

<br>

## Transaction带来的读一致性的问题



<br>

## Concurrency Control
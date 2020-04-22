# Transaction (事务) & Concurrency Control (并发访问控制)

## Transaction

**"ACID"**

* **Atomicity 原子性**

  一个事务是一个不可分割的工作单位: 一个事务中包括的操作要么都成功, 要么都不成功.

  成功:

  <img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/3-Transaction%20&%20Concurrency%20Control/transaction_1.png?raw=true">

  失败:

  <img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/3-Transaction%20&%20Concurrency%20Control/transaction_2.png?raw=true">

* **Consistency 一致性**

  一个事务必须是使数据库从一个一致性状态变到另一个一致性状态.

  *这与atomicity是密切相关的*

* **Isolation 隔离性**

  一个事务的执行不能被其他事务干扰.

  即一个事务内部的操作及使用的数据对并发的其他事务是隔离的, 并发执行的各个事务之间不能互相干扰.

* **Durability 持久性**

  一个事务一旦`commit`, 它对数据库中数据的改变就应该是永久性的, 接下来的其他操作或故障不应该对其有任何影响.

<br>

## Concurrency Conrol 并发访问控制

既然transaction涉及一组SQL操作, 那么<u>并发访问数据库这个共享资源时, 必然会涉及并发控制的问题</u>.

***

### Transaction和 并发访问 带来的<读一致性>的问题

<读一致性>的问题: 即事务A在其操作过程中, 两次读到数据不一样

1. **脏读 (Dirty Read)**

   * 事务A在其操作过程中, 读取了一部分数据

   * 事务B更改了表的数据, 但未`commit`

   * 事务A读到了事务B还`uncommitted`的数据

     *事务A读到了事务B `uncommited`的"脏数据" => 因而这个问题叫做 "脏读"*

2. **不可重复读 (Non-Repeatable Read)**

   * 事务A在其操作过程中, 读取了一部分数据

   * 事务B`update/delete`了表的数据, 并`commit`

   * 事务A读到了事务B新`commit`的`update/delete`后的数据

     *事务A的"重复读"出现了问题 => 因而这个问题叫做 "不可重复读"*

3. **幻读 (Illusion Read)**

   * 事务A在其操作过程中, 读取了一部分数据

   * 事务B向表`insert`了新的数据, 并`commit`

   * 事务A读到了事务B新`commit`的新`insert`的数据

     *事务A读到了本来不存在的, 事务B新`insert`的数据 => 因为这个问题叫做 "幻读"*

***

<br>

### 如何解决上述各种<读一致性>的问题？

### 通过定义Transaction Isolation Level 事务隔离级别 来实现

**四种事务隔离级别:**

*(注: 类比像上面一样, 标记事务A为一个R事务, 事务B为一个W事务)*

| Name                           | 解释                          | 解决的问题 / 达到的效果                                      | 未解决的问题                                                 | 备注                                                         |
| ------------------------------ | ----------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **`Read Uncommited` 读未提交** | R不阻塞R/W<br>W不阻塞R, 阻塞W |                                                              | 由于W不阻塞R, 所以W的`uncommited`的"脏数据""也会被R读到, 所以连最基本的"1脏读"都没有解决 | Concurrency最高 (性能最好), 但是严格度最低, 不可取           |
| **`Read Commited` 读已提交**   | R不阻塞R/W<br>W阻塞R/W        | 由于R不阻塞W但W阻塞R, 所以R不会读到W的`uncommited`的"脏数据", 只有W `commit`了之后, 才不会阻塞R, 所以解决了"1脏读"的问题 | 也正是由于R不阻塞W, 所以R会读到B新`commit`的`update/delete`后的数据, 所以还会有"2不可重复读"的问题 | 也是很多RDBMS的默认级别                                      |
| **`Repeatable Read` 可重复读** | R不阻塞R, 阻塞W<br>W阻塞R/W   | 由于R阻塞W, 所以R既不会读到W的`uncommited`的"脏数据", 也不会读到W新`commit`的`update/delete`后的数据, 所以解决了"1脏读"和"2不可重复读"的问题 | (参考下面, 由于加的是行锁, 整张表本身并没有被锁住, 所以)     | <u>`MySQL`默认级别</u><br/><u>`InnoDB`引擎在`Repeatable Read`事务隔离级别下, 解决了"幻读"的问题, 从而解决了全部问题, 又保证了一定的concurrency</u> |
| **`Serializable` 串行化**      | 全部互相阻塞                  | 解决了全部的问题                                             |                                                              | 严格度最高, 但是concurrency最低 (性能极低), 不可取           |

<br>

### 事务隔离级别的实现方式:

### 1. Lock-Based Concurrency Control (LBCC) 基于锁的并发访问控制

***

#### 行锁 vs 表锁

|                     | 行锁                            | 表锁                                |
| ------------------- | ------------------------------- | ----------------------------------- |
| 定义 / 锁定粒度     | 小 (锁定一行)                   | 大 (锁定整张表)                     |
| => 是否会产生死锁?  | 低 (需要先找到改行)             | 不会 (锁定整张表, 粒度大)           |
| 加锁效率            | 低 (需要先找到改行)             | 高                                  |
| 冲突概率            | 低 (只锁定一行)                 | 高 (锁定整张表, 对于表中任意一行的) |
| => 并发性能         | 高                              | 低                                  |
| 偏向                | 偏向"写"                        | 偏向"读"                            |
| `MySQL`存储引擎实现 | `InnoDB`<br>=> `InnoDB`偏向"写" | `MyISAM`<br>=> `MyISAM`偏向"读"     |

***

#### (行锁 的) 读锁 (共享锁 Shared Lock) vs 写锁 (排他锁 Exclusive Lock)

| 比较项目 | 读锁                                                         | 写锁                              |
| -------- | ------------------------------------------------------------ | --------------------------------- |
| 定义     | 多个事务对于同一数据, 可以共享一把锁, 都能访问到数据, 但是只能R不能W<br>即针对R操作同一数据, 多个事务可以同时进行 | 当前W操作完成前, 阻塞其他所有操作 |

<u>上面的两个定义, 实际上就实现了`Repeatable Read`事务隔离级别</u>

***

获取 行-读锁:

```mysql
select *
from some_table
lock in share mode;  -- 手动获取
```

获取 行-写锁:

```mysql
select *
from some_table
for update;  -- 手动获取

-- insert/update/delete语句 自动获取
```

***

<br>

### 2. Multi-Version Concurrency Control (MVCC) 多版本的并发访问控制

*(非常类似于git的版本控制)*

* 在每一行中, 记录一个版本号
* 当一个事务开启时, 其看到一个特定版本的DB, 事务中的全部操作只能看到这个特定版本的DB, 所有的修改也只能对于这个特定版本的DB进行
* (=> 不同事务可以并发地进行, 而不用被彼此锁住)
* 事务`commit`时, 检查各个事务所做的修改: 对于某一行, 通过检查其版本号, 确定自从该行被读出来之后, 是否被修改过
* 只要事务之间不冲突, 即可`commit`成功, 同时更新对应行的版本号, 否则失败

<br>

***

### 悲观锁 (Pessimistic Lock) vs 乐观锁 (Optimistic Lock)

乐观锁和悲观锁, 讨论的不再是实现机制的不同, 而是<u>对锁的使用策略不同 => 关注于应用层面的不同</u>

<br>

**悲观锁** 认为: 事务并发频繁, 冲突频繁

<u>所以, "悲观地"靠具体的锁机制来实现并发访问控制</u>

=> 参见上面<u>LBCC的行锁机制</u>

<br>

**乐观锁** 认为: 事务并发不频繁, 冲突不频繁

<u>所以, 可以放心大胆地just do it, 如果`commit`时没有冲突, 即可`commit`成功, 否则失败</u>

=> 本质上没有加锁, 而是<u>通过MVCC完美实现</u>

<br>

|          | 悲观锁                    | 乐观锁                |
| -------- | ------------------------- | --------------------- |
| 应用场景 | 需要的并发量大            | 需要的并发量不大      |
| 优势     | 实实在在地加锁            | 性能好, concurrency高 |
| 劣势     | 性能不好, concurrency不好 | 用户体验不好          |

***

<br>

## 个人小总结

为了解决所有并发访问控制问题, 并保证一定的concurrency:

* 在`MySQL`中设置事务隔离级别为`Repeatable Read`
  * 若需要的并发量大, 选择使用"悲观锁" (LBCC的行锁机制实现)

    * ```mysql
      select *
      from some_table
      lock in share mode;  -- 手动获取 行-读锁
      ```

    * ```mysql
      select *
      from some_table
      for update;  -- 手动获取 行-写锁
      
      -- insert/update/delete语句 自动获取 行-写锁
      ```

  * 若需要的并发量不大, 选择使用"乐观锁" (MVCC实现)


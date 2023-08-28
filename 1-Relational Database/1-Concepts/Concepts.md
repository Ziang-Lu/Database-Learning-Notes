# Relational DB Concepts

## Relational Data Model (关系型数据模型)

### Entity-Relationship (ER) Diagram (实体关系图)

用来展示entities之间的关系

***

**ER Diagram Notations**:

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Concepts/ER_diagram-notations.png?raw=true">

***

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Concepts/ER_diagram.png?raw=true" width="600px">

<br>

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Concepts/ER_diagram-example.png?raw=true" width="600px">

这两个diagrams都使用了Crow's Foot Notation

<br>

## 数据存储

###  Tables (表)

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Concepts/data_storage-table.png?raw=true" width="600px">



#### Primary Key (PK) (主键)

A column or a set of columns that <u>uniquely identify each row</u> in the table

> Commonly use a simple numerical ID that is unique for each row

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Concepts/data_storage-primary_key.png?raw=true" width="600px">

PK <u>cannot be null</u>.



#### Index (索引): 用来快速检索数据

>  实现 (B-tree & B+ tree) 见:
>
> * 简介: https://mp.weixin.qq.com/s/cOdvz3SPltNQsm-C2Cyd0A
> * 实现: https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Concepts/B-Tree%20%26%20B%2B%20Tree/B-Tree%20%26%20B%2B%20Tree.md

* 每当创建一张表时, 会同时自动创建一个基于其PK的索引
  * 这个索引有时被称为"聚集索引" ("clustered index")

* 索引也可以基于多个column创建, 例如:

```mysql
create index composite_index_name
on some_table (column_name1, column_name2, column_name3);
```

>  在此情况下, 任何基于leftmost prefix of the indexed columns的检索, 都可以使用到这个索引
>
> * 换句话说, 基于 `column_name1`, `(column_name1, column_name2)` 或 全部indexed columns 的检索都可以使用到这个索引
> * 但是基于 `column_name2` 或类似于 `(column_name2, column_name1)` 的检索却无法使用到这个索引



#### Foreign Key (FK) (外键)

A column or a set of columns that <u>identify a row in another table</u>  (refer to the PK in another table)

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Concepts/data_storage-primary_key_and_foreign_key.png?raw=true" width="600px">

Like in the above example, in the `Department` table, each `Department` needs to uniquely identify its leader, which is a `Person`.

=> The `Department` table uses a column called `Department.leadPersonID` to refer to the values in `Person.ID`, which is the primary key of `Person` table, and thus uniquely identifies the leader.

=> In this way, `Department.leadPersonID` works as a foreign key from `Department` table to `Person` table.

***

<br>

## 与Relational DB的交互

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Concepts/comm_with_relational_DB.png?raw=true" width="600px">

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Concepts/comm_with_relational_DB_impl.png?raw=true" width="600px">


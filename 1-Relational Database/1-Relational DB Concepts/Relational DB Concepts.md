# Relational DB Concepts

## Relational Data Model (关系型数据模型)

### - Building Blocks

* **Entity**

  Unique, distinct, and distinguishable

* **Attribute**

  An ~ is a <u>characteristic of an entity</u>.

* **Relationship**

  Describes the <u>association between entities</u>

  * 1-to-1
  * 1-to-Many
  * Many-to-Many

### - Entity-Relationship (ER) Diagram (实体关系图)

-> Used to illustrate and document the relationships between entities

***

**ER Diagram Notations**:

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Relational%20DB%20Concepts/ER_diagram-notations.png?raw=true">

***

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Relational%20DB%20Concepts/ER_diagram.png?raw=true" width="600px">

<br>

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Relational%20DB%20Concepts/ER_diagram-example.png?raw=true" width="600px">

Note that these two diagrams uses Crow's Foot Notation

<br>

## Data Storage

We store all of the data **in the form of (related) tables**.

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Relational%20DB%20Concepts/data_storage-table.png?raw=true" width="600px">

***

**Primary Key (PK) (主键)**

**A column or a set of columns that <u>uniquely identify each row</u> in the table**

*(=> Commonly use a simple numerical ID that is unique for each row)*

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Relational%20DB%20Concepts/data_storage-primary_key.png?raw=true" width="600px">

PK <u>cannot be null</u>.

***

**Index (索引)**

**-> 用来快速检索数据**

每当一个table被创建时, 会同时自动创建一个基于其primary key的索引.

*(这个索引有时被称为"聚集索引" ("clustered index").)*

实现 (B-tree & B+ tree) 见:

* Brief introduction: https://mp.weixin.qq.com/s/cOdvz3SPltNQsm-C2Cyd0A
* Implementation: https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Relational%20DB%20Concepts/B-Tree%20%26%20B%2B%20Tree/B-Tree%20%26%20B%2B%20Tree.md

索引可以基于多个column创建, 例如:

```mysql
create index composite_index_name
on some_table (column_name1, column_name2, column_name3);
```

在此情况下, 任何基于leftmost prefix of the indexed columns的检索, 都可以使用到这个索引.

换句话说, 基于`column_name1`, `(column_name1, column_name2)`或`(column_name1, column_name2, column_name3)`的检索都可以使用到这个索引, 但是基于`column_name2`或类似于`(column_name2, column_name1)`的检索却无法使用到这个索引.

***

**Foreign Key (FK) (外部键)**

**A column or a set of columns that <u>identify a row in another table</u>** (refer to the PK in another table)

* The table containing the FK is called the child table, and the table containing the PK is called the parent table or referenced table.

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Relational%20DB%20Concepts/data_storage-primary_key_and_foreign_key.png?raw=true" width="600px">

Like in the above example, in the `Department` table, each `Department` needs to uniquely identify its leader, which is a `Person`.

=> The `Department` table uses a column called `Department.leadPersonID` to refer to the values in `Person.ID`, which is the primary key of `Person` table, and thus uniquely identifies the person (the leader).

=> In this way, `Department.leadPersonID` works as a foreign key from `Department` table to `Person` table.

***

<br>

## Normalized Table Design

#### Every row has the same number of columns.

- If for a given key, there are <u>many values having the same meaning</u>, they need to be <u>splitted into separate rows (separate records)</u>.

<br>

#### There is a **unique key (one column, or multiples columns combined)**, and the **non-key columns describes about the key**.

- The key can even be the entire row (all the columns)!!!
- In any row, the <u>key provides the topic of the sentence</u>, and the <u>rest of the row descibes about the that topic</u>.

<br>

#### (From previous one) **Facts that don't relate to the key belong in different tables.**

*这点需要特别注意!!!*

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Relational%20DB%20Concepts/normalized_table_design_rule_3_original.png?raw=true" width="600px">

Note that the <u>addresses actually describes locations, rather than particular items</u>!!! Thus, it should be designed as follows instead:

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Relational%20DB%20Concepts/normalized_table_design_rule_3_normalized.png?raw=true" width="600px">

<br>

## Communication with Relational DB

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Relational%20DB%20Concepts/comm_with_relational_DB.png?raw=true" width="600px">

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Relational%20DB%20Concepts/comm_with_relational_DB_impl.png?raw=true" width="600px">



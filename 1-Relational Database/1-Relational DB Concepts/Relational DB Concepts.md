# Relational DB Concepts

## Relational Data Model (关系型数据模型)

### - Building Blocks

* **Entity**

  Unique, distinct, and distinguishable

* **Attribute**

  A ~ is a <u>characteristic of an entity</u>.

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

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Relational%20DB%20Concepts/data_storage-primary_key.png?raw=true">

PK <u>cannot be null</u>.

***

**Foreign Key (FK) (外部键)**

**A column or a set of columns that <u>identify a row in another table</u>**

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Relational%20DB%20Concepts/data_storage-primary_key_and_foreign_key.png?raw=true" width="600px">

Like in the above example, in the `Department` tale, each `Department` needs to uniquely identify its leader, which is a `Person`.

=> The `Department` table uses a column called `Department.leadPersonID` to refer to the values in `Person.ID`, which is the primary key of `Person` table, and thus uniquely identifies the person (the leader).

=> In this way, `Department.leadPersonID` works as a foreign key from `Department` table to `Person` table.

***

<br>

## Communication with Relational DB

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Relational%20DB%20Concepts/comm_with_relational_DB.png?raw=true" width="600px">

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Relational%20DB%20Concepts/comm_with_relational_DB_impl.png?raw=true" width="600px">

<br>

## Operations

### 1. Fetching Data from DB

#### (1) Retrieving & Filtering

<br>

#### (2) Aggregation (聚合)

**Summarize multiple rows into a single row**

**(=> Compute a single value from a set of values)**

[On a single table]

* `count`   *(on any type)*

  -> Given a column, count the number rows in that colum that have the same value

  <img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Relational%20DB%20Concepts/operation-aggregation-count.png?raw=true">

  The above is achieved by:

  ```sql
  select species, count(species)
  from animals
  group by species;
  ```

* `sum`

* `avg`

* `max`

* `min`

<br>

#### (3) Join (合并)

**Linking multiple tables** to extract the desired information

[On multiple tables]

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Relational%20DB%20Concepts/operation-join-1-original_tables.png?raw=true" width="500px">

**Question: How many individual animals eat fish?**

Running the following `join` query results in the table on the left:

```sql
select animals.name, animals.species, diet.food from animals join diet on animals.species = diet.species;
```

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Relational%20DB%20Concepts/operation-join-2-mid_result_table.png?raw=true" width="500px">

By adding the row restriction `where food = 'fish'`, we can get the individual animals that eat fish.

After that, we can do a `count` aggregation on the above result table, and finally get the total number of individual animals that eat fish.

The whole process is explained by the following diagram:

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Relational%20DB%20Concepts/operation-join-3-process.png?raw=true" width="500px">

<br>

### 2. Inserting Data to DB

...
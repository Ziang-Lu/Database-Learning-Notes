# Relational Database (DB) Concepts

## Data Storage

We store all of the data **in the form of tables**.

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/Relational%20Database%20Concepts/data_storage-table.png?raw=true" width="600px">

**Primary Key (主键)**

<u>Unique for each row</u>

*(=> Commonly use a simple numerical ID that is unique for each row)*

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/Relational%20Database%20Concepts/data_storage-primary_key.png?raw=true">

<br>

## Operations

### 1. Fetching Data from DB

#### (1) Aggregation (聚合)

**Summarize multiple rows into a single row**

**(=> Compute a single value from a set of values)**

[On a single table]

* `count`   *(on any type)*

  -> Given a column, count the number rows in that colum that have the same value

  <img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/Relational%20Database%20Concepts/operation-aggregation-count.png?raw=true">

* `sum`

* `avg`

* `max`

* `min`

<br>

#### (2) Join (合并)

**Linking multiple tables** to extract the desired information

[On multiple tables]

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/Relational%20Database%20Concepts/operation-join-1-original_tables.png?raw=true" width="500px">

**Question: How many individual animals eat fish?**

Running the following `join` query results in the table on the left:

```sql
select animals.name, animals.species, diet.food from animals join diet on animals.species = diet.species
```

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/Relational%20Database%20Concepts/operation-join-2-mid_result_table.png?raw=true" width="500px">

By adding the row restriction `where food = 'fish'`, we can get the individual animals that eat fish.

After that, we can do a `count` aggregation on the above result table, and finally get the total number of individual animals that eat fish.

The whole process is explained by the following diagram:

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/Relational%20Database%20Concepts/operation-join-3-process.png?raw=true" width="500px">


# Relational Database (DB)

## Data Storage

We store all of the data **in the form of tables**.

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/data_storage-table.png?raw=true" width="600px">

**Primary Key (主键)**

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/data_storage-primary_key.png?raw=true">

<br>

## Operations

### Aggregation (聚合)

[On a single table]

**Summarize multiple rows into a single row**

**(=> Compute a single value from a set of values)**

* Count   *(on any type)*

  -> Given a column, count the number rows in that colum that have the same value

  <img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/operation-aggregation-count.png?raw=true">

* Sum   *(on number)*

* Avg   *(on number)*

* Max   *(on number)*

* Min   *(on number)*

### Join (合并)

[On multiple tables]

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/operation-join-1-original_tables.png?raw=true">

Running the following query results in the table on the left:

```sql
select animals.name, animals.species, diet.food from animals join diet on animals.species = diet.species
```

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/operation-join-2-mid_result_table.png?raw=true">

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/operation-join-3-process.png?raw=true">
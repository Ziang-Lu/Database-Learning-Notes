# SQL Notes

## Data Types in SQL

* `int`

  * $\approx$ Java `int` / Python `int`

* `decimal`

  An exact decimal value

  ```sql
  decimal(8, 2)
  -- At most 8 digits in total
  -- 2 digits to the right of the decimal place
  -- xxxxxx.xx
  ```

* `real`

  * $\approx$ Java `float`

* `double precision`

  * $\approx$ Java `double` / Python `float`

* `text`

  * $\approx$ Java `String` / Python `str`

  * Values are written <u>in single quotes</u>.

* `char(n)`

  A string of exactly *n* characters

* `varchar(n)`

  A string of up to *n* characters

* `date`

  A calendar date, including year, month and day

  * Values are written like `'2014-04-13'`.

* `time`

  A time of day

* `timestamp`

  A `data` and `time` together

<br>

## Operations

### 0. Creating DB

```sql
create database test;
```

After creating the DB, use the following command to show all existing DBs, to check if the creation is successful:

```mysql
show databases;
```

<br>

### 1. Fetching Data from DB

#### (1) Retrieving & Filtering

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/select_from_where.png?raw=true" width="600px">

```sql
select name, birthdate
from animals
where species = 'gorilla'
	and name = 'Max';
```

Note that <u>`where` applies before any aggregation</u>

***

**`in` operator** in `where` clause

Select a value from a selection of values:

```sql
select name, birthdate
from animals
where species in ('gorilla', 'llama', 'orangutan');
```

Use `not in` to exclude a selection of values:

```sql
select name, birthdate
from animals
where species not in ('gorilla', 'llama', 'orangutan');
```

***

**`between` operator** in `where` clause

Select a value from a <u>range</u> of values (inclusive):

```sql
select name, species
from animals
where birthdate between '1993-07-31' and '1993-10-05';
-- This will include both '1993-07-31' and '1993-10-05'.
```

Use `not between` to exclude a range of values (exclusive):

```sql
select name, species
from animals
where birthdate not between '1993-07-31' and '1993-10-05';
-- This will include neigher '1993-07-31' nor '1993-10-05'.
```

***

**`is null` operator** in `where` clause

Select only `null` values:

```sql
select name, species
from animals
where birthdate is null;
```

Use `is not null` to select only non-null values:

```sql
select name, species
from animals
where birthdate is not null;
```

***

**`like` operator** in `where` clause

Select values that follow a pattern:

Wildcards

* `%` represents any number of characters
* `_` represents a single character

```sql
select name, birthdate
from animals
where species like '_r%';
-- This will select all the species that have 'r' at the second position.
```

Use `not like` to exclude values that follow a pattern:

```sql
select name, birthdate
from animals
where species not like '_r%';
-- This will select all the species that does not have 'r' at the second position.
```

***

Note: **Use `*` to select all columns**:

```sql
select * from animals
where species = 'orangutan'
order by birthdate desc;
```

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/select_from_order-by.png?raw=true" width="500px">

<br>

```sql
select name, birthdate
from animals
where species = 'gorilla'
limit 5 offset 3;
```

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/select_from_limit_offset.png?raw=true" width="500px">

***

**Supported Comparison Operators**

`=`, `!=`, `<`, `>`, `<=`, `>=`

***

**Supported Math Operators**

`+`, `-`, `*`, `/`

```sql
select product_id, units_on_order, unit_price,
	units_on_order * unit_price as order_total_cost
from products
```

***

<br>

#### (2) Aggregation (聚合)

**Summarize multiple rows into a single row**

**(=> Compute a single value from a set of values)**

[On a single table]

* `count`

  * For each distinct species, find how many animals are there?

    ```sql
    select species, count(species)
    from animals
    group by species
    limit 5;
    ```

  * <u>For each distinct name, find how many animals are sharing that name?</u>

    <img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/select_from_group-by.png?raw=true" width="600px">

    ```sql
    select name, count(*) as num
    from animals
    group by name;
    ```

    This reads as:

    From `animals` table,

    - select the `name` column
    - do the aggregation: `count` all the selected rows grouping by the `name` column, i.e., <u>for each distinct `name`, `count` the number of selected rows with that `name`</u>

* `sum`

  ```sql
  select sum(unit_price) as total_prod_price
  from products;
  ```

* `avg`

  ```sql
  select avg(unit_price) as avg_price
  from products;
  ```

* `max`

  ```sql
  select max(name) as max_name
  from animals;
  ```

* `min`

  ```sql
  select species, min(birthdate)
  from animals
  group by species
  limit 5;
  ```

  This reads as:

  From `animals` table,

  - select the `species` column
  - do the aggregation: <u>for each distinct `species`, find the minimum `birthdate` with that `species`</u>

  Check the above illustration

***

**`having` clause**:

Works <u>similar to `where`</u> clause, but <u>after any aggregation</u>

```sql
select customer_id, count(*) as customer_orders
from orders
group by customer_id
having customer_orders >= 2;
```

***

<br>

#### (3) Join (合并)

**Linking multiples tables** to extract the desired information

[On multiple tables]

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/operation-join-1-original_tables.png?raw=true" width="500px">

**Question: How many individual animals eat fish?**

Running the following `join` query results in the table on the left:

```sql
select animals.name, animals.species, diet.food from animals join diet on animals.species = diet.species;
```

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/operation-join-2-mid_result_table.png?raw=true" width="500px">

By adding the row restriction `where food = 'fish'`, we can get the individual animals that eat fish.

After that, we can do a `count` aggregation on the above result table, and finally get the total number of individual animals that eat fish.

The whole process is explained by the following diagram:

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/operation-join-3-process.png?raw=true" width="500px">

Simplified version:

```sql
select animals.name, animals.species, diet.food from animals, diet where animals.species = diet.species;
```

<br>

### 2. Inserting Data to DB

#### (1) Creating New Table

* `not null`
* `unique`

* `primary key`
  * A combination of `not null` and `unique`

Note the difference in declaring a `primary key` in SQLite and MySQL:

**SQLite**

```sqlite
create table scores (
    id varchar(20) primary key,
    name varchar(20) not null,
    score int
)
```

**MySQL**

```mysql
create table scores (
	id varchar(20) not null,
    name varchar(20) not null,
    score int,
    primary key(id)
)
```

<br>

#### (2) Creating Temporary Table (临时表)

Temporary table:

* Creating faster than a real, permanent table
* Deleted when the current client session is terminated

```sql
create temporary table sandals as (
    select *
    from shoes
    where shoe_type = 'sandals'
)
```

*(有点像一个temporary的变量, 来暂时储存intermediate的结果, 为了后续使用)*

<br>

#### Inserting Data to Table

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/insert-into_values.png?raw=true" width="600px">

A single `insert` statement can only <u>insert rows into a single table</u>.


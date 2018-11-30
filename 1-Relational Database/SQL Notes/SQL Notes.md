# Structured Query Language (SQL) Notes

## Data Types in SQL

* `int`

  * $\approx$ Java `int` / Python `int`

* `decimal`

  An exact decimal value

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

### 1. Fetching Data from DB

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/SQL%20Notes/select_from_where.png?raw=true" width="600px">

```sql
select name, birthdate from animals where species = 'gorilla' and name = 'Max';
```

| name | birthdate  |
| :--: | :--------: |
| Max  | 2001-04-23 |

***

Note: Use `*` to select all columns:

```sql
select * from animals where species = 'orangutan' order by birthdate desc;
```

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/SQL%20Notes/select_from_order-by.png?raw=true" width="500px">

|  name   |  species  | birthdate  |
| :-----: | :-------: | :--------: |
|  Singa  | orangutan | 2012-11-03 |
|  Gajah  | orangutan | 2011-05-26 |
| Putera  | orangutan | 1993-06-29 |
|  Ratu   | orangutan | 1989-09-15 |
| Kambing | orangutan | 1988-11-12 |
|  Raja   | orangutan | 1975-04-09 |

<br>

```sql
select name, birthdate from animals where species = 'gorilla' limit 5 offset 3;
```

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/SQL%20Notes/select_from_limit_offset.png?raw=true" width="500px">

|  name   | birthdate  |
| :-----: | :--------: |
|   Liz   | 1998-06-12 |
| George  | 2011-01-09 |
| George  | 1998-05-18 |
| Wendell | 1982-09-24 |
|  Bjorn  | 2000-03-07 |

***

**Supported Comparison Operators**

`=`, `!=`, `<`, `>`, `<=`, `>=`

#### (1) Aggregation (聚合)

[On a single table]

* `count`

  * For each distinct species, find how many animals are there?

    ```sql
    select species, count(species) from animals group by species limit 5;
    ```

    |  species   | count(species) |
    | :--------: | :------------: |
    |   alpaca   |       5        |
    | brown bear |       3        |
    |   camel    |       3        |
    |   dingo    |       3        |
    |  echidna   |       1        |

  * <u>For each distinct name, find how many animals are sharing that name?</u>

    <img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/SQL%20Notes/select_from_group-by.png?raw=true" width="600px">

    ```sql
    select name, count(*) as num from animals group by name;
    ```

    This reads as:

    From `animals` table,

    - select the `name` column
    - do the aggregation: `count` all the selected rows grouping by the `name` column, i.e., <u>for each distinct `name`, `count` the number of selected rows with that `name`</u>

* `max`

  ```sql
  select max(name) as max_name from animals
  ```

  | max_name |
  | :------: |
  |   Zoe    |

* `min`

  ```sql
  select species, min(birthdate) from animals group by species limit 5;
  ```

  This reads as:

  From `animals` table,

  - select the `species` column
  - do the aggregation: <u>for each distinct `species`, find the minimum `birthdate` with that `species`</u>

  Check the above illustration

  |  species   | min(birthdate) |
  | :--------: | :------------: |
  |   alpaca   |   2001-01-16   |
  | brown bear |   1981-10-17   |
  |   camel    |   1971-03-08   |
  |   dingo    |   1999-08-04   |
  |  echidna   |   2003-01-31   |

<br>

#### (2) Join (合并)

[On multiple tables]

Full `join` query from the <a href="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/Relational%20Database%20Concepts/Relational%20Database%20Concepts.md">relational DB concepts notes</a>:

```sql
select animals.name, animals.species, diet.food from animals join diet on animals.species = diet.species;
```

Simplified version:

```sql
select animals.name, animals.species, diet.food from animals, diet where animals.species = diet.species;
```

<br>

### 2. Inserting Data to DB

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/SQL%20Notes/insert-into_values.png?raw=true" width="600px">

A single `insert` statement can only <u>insert a single row into a single table</u>.


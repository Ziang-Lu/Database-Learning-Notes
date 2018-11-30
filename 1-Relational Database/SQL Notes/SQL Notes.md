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

Note: Use `*` to select all columns:

```sql
select * from animals where species = 'orangutan' order by birthdate desc;
```

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/SQL%20Notes/select_from_order_by.png?raw=true" width="600px">

```sql
select * from animals limit 10 offset 20;
```

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/SQL%20Notes/select_from_limit_offset.png?raw=true" width="600px">

Supported Comparison Operators**

`=`, `!=`, `<`, `>`, `<=`, `>=`

#### (1) Aggregation (聚合)

[On a single table]

* `count`

  <img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/SQL%20Notes/select_from_group_by.png?raw=true" width="600px">

* `max`

  ```sql
  select max(name) as max_name from animals
  ```
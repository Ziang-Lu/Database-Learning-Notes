# Operations

## 0. Operations on DB

```mysql
create database test;
```

After creating the DB, use the following command to show all existing DBs, to check if the creation is successful:

```mysql
show databases;
```

To delete the DB, use the following command:

```mysql
drop database test;
```

<br>

## 0. Operations on Table Itself

#### (1) Creating Table

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/2-Operations/create-table.png?raw=true" width="500px">

*We can add `if not exists` between `table` and `tablename`, to create the table if it doesn't already exist.*

**Constraints:**

- `default`

- `not null`

- `check`

  ```mysql
  create table users (
      id integer primary key,
      username varchar(100) not null unique,
      age check(age >= 18)  -- Check a boolean expression
  );
  ```

- `unique`

- `primary key`

  - Essentially, a combination of `not null` and `unique`

- `autoincrement`

  ***

  *MySQL*:

  ```mysql
  create table students (
      id integer primary key auto_increment,  -- "autoincrement" implementation in MySQL
      name varchar(20) not null,
      email varchar(100) not null
  );
  ```

  *PostgreSQL*:

  ```sql
  create table students (
      id serial primary key,  -- "autoincrement" implementation in PostgreSQL
      name varchar(20) not null,
      email varchar(100) not null
  );
  ```

  ***

- `foreign key`

<br>

#### (2) Creating Index on Table

```mysql
create index index_name
on some_table (column_name);
```

<br>

***

#### Temporary Table (临时表)

- Creating faster than a real, permanent table
- Deleted when the current client session is terminated

```mysql
-- Create a temporary table containing all the sandals
create temporary table sandals as
    select *
    from shoes
    where shoe_type = 'sandals';
```

*(有点像一个temporary的变量, 来暂时储存intermediate的结果, 为了后续使用)*

***

#### View (视图)

View: A ~ is a <u>virtual table (illusion) based on the result-set of an SQL statement</u>.

* Creation

  ```mysql
  -- Create a view containing all the customers from Brazil
  create view brazil_customers as
      select name, contact_name
      from customers
      where country = 'Brazil';
  ```

  *(有点像一个temporary的变量, 来暂时储存intermediate的结果, 为了后续使用)*

  但是与temporary table不同的是, view本质上并没有写数据: 因此对于没有write权限的DB, 用view是更方便的.

* Update

  ```mysql
  -- Update the "brazil_customers" view by adding a "City" column to it
  create or replace view brazil_customers as
      select name, contact_name, city
      from customers
      where country = 'Brazil';
  ```

* Deletion

  ```mysql
  drop view brazil_customers;
  ```

***

<br>

#### (3) Altering Existing Table Itself

Add, modify, or delete columns of an existing table

- Rename table

  ```mysql
  alter table customers
  rename to my_customers;
  ```

- Rename column

  ```mysql
  alter table customers
  rename name to fullname;
  ```

- Add column

  ```mysql
  alter table customers
  add email varchar(255);
  ```

- Delete column

  ```mysql
  alter table customers
  drop email;
  ```

<br>

#### (4) Deleting Table

```mysql
drop table scores;  -- Delete all the information stored in the table, and then delete the table
```

```mysql
truncate table scores;  -- Delete all the information stored (including the headers) in the table, but not table itself
```

<br>

## 1. Fetching Data from DB

#### (1) Retrieving & Filtering

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/2-Operations/select_from_where.png?raw=true" width="600px">

```mysql
select name, birthdate
from animals
where species = 'gorilla'
    and name = 'Max';
```

Note that <u>`where` applies before any aggregation</u>

------

**`in` operator** in `where` clause

Select a value from a selection of values:

```mysql
select name, birthdate
from animals
where species in ('gorilla', 'llama', 'orangutan');
```

Use `not in` to exclude a selection of values:

```mysql
select name, birthdate
from animals
where species not in ('gorilla', 'llama', 'orangutan');
```

------

**`between` operator** in `where` clause

Select a value from a range of values (inclusive):

```mysql
select name, species
from animals
where birthdate between '1993-07-31' and '1993-10-05';
-- This will include both '1993-07-31' and '1993-10-05'.
```

Use `not between` to exclude a range of values (exclusive):

```mysql
select name, species
from animals
where birthdate not between '1993-07-31' and '1993-10-05';
-- This will include neither '1993-07-31' nor '1993-10-05'.
```

------

**`is null` operator** in `where` clause

Select only `null` values:

```mysql
select name, species
from animals
where birthdate is null;
```

Use `is not null` to select only non-null values:

```mysql
select name, species
from animals
where birthdate is not null;
```

------

**`like` operator** in `where` clause

Select values that follow a pattern:

Wildcards

- `%` represents any number of characters
- `_` represents a single character

```mysql
select name, birthdate
from animals
where species like '_r%';
-- This will select all the species that have 'r' at the second position.
```

Use `not like` to exclude values that follow a pattern:

```mysql
select name, birthdate
from animals
where species not like '_r%';
-- This will select all the species whose second position is not 'r'.
```

------

Note:

```mysql
select name, birthdate
from animals
where species = 'gorilla'
limit 5 offset 3;
```

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/2-Operations/select_from_limit_offset.png?raw=true" width="500px">

------

<br>

------

**`case` clause**

- Mimics the `if-then-else` scheme in most programming languages
- Do different processing based on some condition

```mysql
-- Add a corresponding description according to the "quantity" field
select order_id, quantity,
    (case
        when quantity > 30 then 'The quantity is greater than 30'
        when quantity = 30 then 'The quantity is 30'
        else 'The quentity is less than 30'
    end) as quantity_description
from order_details;
```

```mysql
-- Classify the tracks by size
select track_id, name, bytes,
    (case
        when bytes < 300000 then 'small'
        when bytes >= 300001 and bytes < 500000 then 'medium'
        when bytes >= 500000 then 'large'
        else 'other'
    end) as byte_category
from tracks;
```

------

<br>

#### (2) Aggregation (聚合)

**Summarize multiple rows into a single row**

**(=> Compute a single value from a set of values)**

- `count`

  - For each distinct species, find how many animals are there?

    ```mysql
    select species, count(*) as num
    from animals
    group by species
    limit 5;
    ```

  - For each distinct name, find how many animals are sharing that name?

    <img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/2-Operations/select_from_group-by.png?raw=true" width="600px">

    ```mysql
    select name, count(*) as num
    from animals
    group by name;
    ```

    This reads as:

    From `animals` table,

    - select the `name` column
    - do the aggregation: `count` all the selected rows grouping by the `name` column, i.e., <u>for each distinct `name`, `count` the number of selected rows with that `name`</u>

- `sum`

  ```mysql
  select sum(unit_price) as total_price
  from products;
  ```

- `avg`

  ```mysql
  select avg(unit_price) as avg_price
  from products;
  ```

- `max`

  ```mysql
  select max(name) as max_name
  from animals;
  ```

- `min`

  ```mysql
  select species, min(birthdate)
  from animals
  group by species
  limit 5;
  ```

  This reads as:

  From `animals` table,

  - select the `species` column
  - do the aggregation: <u>for each distinct `species`, find the minimum `birthdate` within that `species`</u>

  Check the above illustration

------

**`having` clause**:

Works <u>similar to `where`</u> clause, but <u>after any aggregation</u>

```mysql
select customer_id, count(*) as customer_orders
from orders
group by customer_id
having customer_orders >= 2;
```

------

<br>

#### (3) Subquery (子查询)

**Queries inside another query**

<u>Question: Need to know the region of each customer who ever had an order with freight > 100</u>

```mysql
-- Step 1: Select all the customers who ever had an order with freight > 100
select distinct customer_id
from orders
where freight > 100;

-- Step 2: Get the customer name, company name and region for those selected customers
select name, company_name, region
from customers
where id in ...;  -- Use the above resulting customer IDs

-- Combined using subquery:
select name, company_name, region
from customers
where id in (
    select distinct customer_id
    from orders
    where freight > 100
) as subq;  -- PostgreSQL requires an alias of the subquery result table
```

***

**"Common Table Expression" ("公共表表达式") - `with` 结构**

与subquery本质上相同，只是一个syntax sugar

```mysql
with events as (
    select channel, date_trunc('day', occurred_at), count(*) as daily_count  -- date_trunc() is a function defined in PostgreSQL
    from web_events
    group by 1, 2
)

select channel, avg(daily_count) as avg_daily_count
from events
group by channel;
```

***

<br>

#### (4) Join (合并)

**Linking multiples tables** to extract the desired information

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/2-Operations/join-1-original_tables.png?raw=true" width="500px">

**Question: How many individual animals eat fish?**

Running the following `join` query results in the table on the left:

```mysql
select animals.name, animals.species, diet.food
from animals join diet
on animals.species = diet.species
where diet.food = 'fish';
```

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/2-Operations/join-2-mid_result_table.png?raw=true" width="500px">

After that, we can do a `count` aggregation on the above result table, and finally get the total number of individual animals that eat fish.

The whole process is explained by the following diagram:

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/2-Operations/join-3-process.png?raw=true" width="500px">

```mysql
select count(*) as count
from (
    select animals.name, animals.species, diet.food
    from animals join diet
    on animals.species = diet.species
    where diet.food = 'fish'
);
```

<br>

------

**Different Types of `join`:**

- **CROSS JOIN** (Cartesian Join)

  For <u>each record in the left table, match it with all the records in the right table</u>.

  => Very <u>computationally taxing</u>, and potentially generates <u>a very large result set</u>!

  ```mysql
  select products.product_name, products.unit_price, suppliers.supplier_name
  from suppliers cross join products;
  ```

  *e.g., There are 29 rows in the "products" table, and 77 rows in the "customers" table; then there will be 29x77=2233 rows in the result set.*

  => <u>Not very useful!</u>

- **(INNER) JOIN**

  Returns records that <u>have matching values in both tables</u>

  - 是`join`的默认形式, 即上面的

    ```mysql
    select animals.name, animals.species, diet.food
    from animals join diet
    on animals.species = diet.species
    where diet.food = 'fish';
    ```

    即为`inner join`

  `inner join` three tables:

  ```mysql
  select order.id, customers.customer_name, shippers.shipper_name
  from orders
  join customers on orders.customer_id = customers.id
  join shippers on orders.shipper_id = shippers.id;
  ```

- **LEFT (OUTER) JOIN**

  Returns <u>all records from the left table</u>, as well as the <u>matching records from the right table</u>

  *Determine "left table" and "right table":*

  `from left_table left join right table`

  ```mysql
  select customers.customer_name, orders.id
  from customers left join orders
  on cutomers.customer_id = orders.id
  order by customers.customer_name;
  ```

- **RIGHT (OUTER) JOIN**

  Returns <u>all records from the right table</u>, as well as the <u>matching records from the left table</u>

  *与left (outer) join是完全对称的*

  ```mysql
  select orders.id, employees.last_name, employees.first_name
  from orders right join employees
  on orders.employee_id = employees.id
  order by orders.id;
  ```

- **FULL (OUTER) JOIN**

  Returns <u>all records in both tables</u> when there is a match in either table

  *本质上是一个left (outer) join再补上right table中的剩余部分*

  ```mysql
  select customers.curstomer_name, orders.id
  from customers full outer join orders
  on customers.id = orders.customer_id
  order by customers.customer_name;
  ```

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/2-Operations/join-types.png?raw=true" width="500px">

------

<br>

#### (5) Union / Union All

`union` is used to combine the result sets of 2 or more `select` statements.

```mysql
select supplier_id as 'id_value', supplier_name
from suppliers
where supplier_id > 2000
union
select company_id as 'id_value', company_name
from companies
where company_id > 1000
order by 1;
```

Notes:

* There must be the same number of expressions in both SELECT statements.
* The corresponding expressions must have the same data type in the SELECT statements.

`union all`

Only difference from `union`:

* `union` removes duplicate rows.
* `union all` does NOT remove duplicate rows.

<br>

## 2. Inserting Data to Table

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/2-Operations/insert-into_values.png?raw=true" width="600px">

A single `insert` statement can only <u>insert rows into a single table</u>.

<br>

## 3. Updating Data to Table

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/2-Operations/update.png?raw=true" width="500px">

```mysql
update customers
set contact_name = 'Aflred Schmidt',
    city = 'Frankfurt'
where customer_id = 1;
```

<br>

## 4. Deleting Data in Table

**在实际设计DB时, 应该只使用逻辑删除 (把对应record的`is_del`设置为`true`), 而不使用物理删除 (即实际删除掉对应record)**

```mysql
delete from customers
where customer_name = 'Alfred Futterkiste';
```

Note that

```mysql
delete from customers; -- Delete all the information (not including the headers) stored in the table, but not table itself
```



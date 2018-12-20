# Operations

## 0. Operations on DB

```sql
create database test;
```

After creating the DB, use the following command to show all existing DBs, to check if the creation is successful:

```mysql
show databases;
```

To delete the DB, use the following command:

```sql
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

  Check out the coding examples

- `check`

  ```sql
  create table users (
      id integer primary key,
      username varchar(100) not null unique,
      age check(age >= 18)
  );
  ```

- `unique`

  Check out the coding examples

- `primary key`

  - A combination of `not null` and `unique`

  Check out the coding examples

- `autoincrement`

  ***

  *SQLite:*

  ```sqlite
  create table students (
      id integer primary key autoincrement,  -- Specify autoincrement in SQLite
  	name varchar(20) not null,
      email varchar(100) not null
  );
  ```

  *MySQL*:

  ```mysql
  create table students (
      id integer primary key auto_increment,  -- Specify autoincrement in MySQL
      name varchar(20) not null,
      email varchar(100) not null
  );
  ```

  *PostgreSQL*:

  ```sql
  create table students (
      id serial primary key,  -- Specify autoincrement in PostgreSQL by using "serial" data type
      name varchar(20) not null,
      email varchar(100) not null
  );
  ```

  ***

- `foreign_key`
  - By using `foreign key` constraints, we establish links between tables.
  - Using `foreign key` constraint prevents actions that would break these links

  Check out the coding examples

<br>

#### (2) Creating Temporary Table (临时表)

Temporary table:

- Creating faster than a real, permanent table
- Deleted when the current client session is terminated

```sql
-- Create a temporary table containing all the sandals
create temporary table sandals as
    select *
    from shoes
    where shoe_type = 'sandals';
```

*(有点像一个temporary的变量, 来暂时储存intermediate的结果, 为了后续使用)*

<br>

#### (3) Creating View

View: A ~ is a <u>virtual table (illusion) based on the result-set of an SQL statement</u>.

```sql
-- Create a view containing all the customers from Brazil
create view brazil_customers as
    select customer_name, contact_name
    from customers
    where country = 'Brazil';
```

*(有点像一个temporary的变量, 来暂时储存intermediate的结果, 为了后续使用)*

<u>但是与temporary table不同的是, view本质上并没有写数据: 因此对于没有write权限的DB, 用view是更方便的.</u>

<br>

#### (4) Altering Existing Table Itself

- Add, modify, or delete columns of an existing table

  - Rename table

    ```sql
    alter table customers rename to my_customers;
    ```

  - Rename column

    ```sql
    alter table customers rename name to fullname;
    ```

  - Add column

    ```sql
    alter table customers
    add email /* column_name */ varchar(255) /* data_type */;
    ```

  - Delete column   (*Only in MySQL and PostgreSQL*)

    ```sql
    alter table customers
    drop email /* column_name */;
    ```


<br>

#### (6) Updating View   (*Only in MySQL & PostgreSQL*)

```sql
-- Update the "brazil_customers" view by adding a "City" column to it
create or replace view brazil_customers as
select customer_name, contact_name, city
from customers
where country = 'Brazil';
```

<br>

#### (7) Deleting Table

```sql
drop table scores;  -- Delete all the information stored in the table, and then delete the table
```

```sql
truncate table scores;  -- Delete all the information stored (including the headers) in the table, but not table itself
```

<br>

#### (8) Deleting View

```sql
drop view brazil_customers;
```

<br>

### 1. Fetching Data from DB

#### (1) Retrieving & Filtering

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/2-Operations/select_from_where.png?raw=true" width="600px">

```sql
select name, birthdate
from animals
where species = 'gorilla'
	and name = 'Max';
```

Note that <u>`where` applies before any aggregation</u>

------

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

------

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

------

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

------

**`like` operator** in `where` clause

Select values that follow a pattern:

Wildcards

- `%` represents any number of characters
- `_` represents a single character

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

------

Note: **Use `*` to select all columns**:

```sql
select * from animals
where species = 'orangutan'
order by birthdate desc;
```

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/2-Operations/select_from_order-by.png?raw=true" width="500px">

<br>

```sql
select name, birthdate
from animals
where species = 'gorilla'
limit 5 offset 3;
```

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/2-Operations/select_from_limit_offset.png?raw=true" width="500px">

------

**Supported Comparison Operators**

`=`, `!=`, `<`, `>`, `<=`, `>=`

------

<br>

------

**`case` clause**

- Mimics the `if-then-else` scheme in most programming languages
- Do different processing based on some condition

```sql
-- Add a corresponding description to the "quantity" field
select order_id, quantity,
    (case
        when quantity > 30 then 'The quantity is greater than 30'
        when quantity = 30 then 'The quantity is 30'
        else 'The quentity is under 30'
    end) as quantity_description
from order_details;
```

```sql
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

[On a single table]

- `count`

  - For each distinct species, find how many animals are there?

    ```sql
    select species, count(species)
    from animals
    group by species
    limit 5;
    ```

  - <u>For each distinct name, find how many animals are sharing that name?</u>

    <img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/2-Operations/select_from_group-by.png?raw=true" width="600px">

    ```sql
    select name, count(*) as num
    from animals
    group by name;
    ```

    This reads as:

    From `animals` table,

    - select the `name` column
    - do the aggregation: `count` all the selected rows grouping by the `name` column, i.e., <u>for each distinct `name`, `count` the number of selected rows with that `name`</u>

- `sum`

  ```sql
  select sum(unit_price) as total_prod_price
  from products;
  ```

- `avg`

  ```sql
  select avg(unit_price) as avg_price
  from products;
  ```

- `max`

  ```sql
  select max(name) as max_name
  from animals;
  ```

- `min`

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

------

**`having` clause**:

Works <u>similar to `where`</u> clause, but <u>after any aggregation</u>

```sql
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

```sql
-- Step 1: Select all the customers who ever had an order with freight > 100
select distinct customer_id
from orders
where freight > 100;

-- Step 2: Get the customer name, company name and region for those selected customers
select customer_name, company_name, region
from customers
where customer_id in ...;  -- Use the above resulting Customer IDs

-- Combined using subquery:
select customer_name, company_name, region
from customers
where customer_id in (
    select distinct customer_id, order_id
    from orders
    where freight > 100
) as subq;  -- PostgreSQL requires an alias of the subquery result table
```

<br>

<u>Question: What is the total number of orders placed by each customer?</u>

```sql
-- Count the total number of orders placed by a particular customer
select count(*)
from orders
where customer_id = 143569;

-- Use the above as a calculation
select customer_name, customer_state,
	(select count(*)
    from orders
    where orders.customer_id = customers.customer_id) as num_of_orders
from customers
order by customer_name;
```

<br>

#### (4) Join (合并)

**Linking multiples tables** to extract the desired information

[On multiple tables]

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/2-Operations/join-1-original_tables.png?raw=true" width="500px">

**Question: How many individual animals eat fish?**

Running the following `join` query results in the table on the left:

```sql
select animals.name, animals.species, diet.food
from animals join diet
on animals.species = diet.species
where diet.food = 'fish';
```

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/2-Operations/join-2-mid_result_table.png?raw=true" width="500px">

After that, we can do a `count` aggregation on the above result table, and finally get the total number of individual animals that eat fish.

The whole process is explained by the following diagram:

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/2-Operations/join-3-process.png?raw=true" width="500px">

Simplified version:

```sql
select animals.name, animals.species, diet.food
from animals, diet
where animals.species = diet.species;
```

<br>

------

**Different Types of `join`:**

- **CROSS JOIN** (Cartesian Join)

  For <u>each record in the left table, match it with all the records in the right table</u>.

  => Very <u>computationally taxing</u>, and potentially generates <u>a very large result set</u>!

  ```sql
  select products.product_name, products.unit_price, suppliers.supplier_name
  from suppliers cross join products;
  ```

  *e.g., There are 29 rows in the "products" table, and 77 rows in the "customers" table; then there will be 29x77=2233 rows in the result set.*

  => <u>Not very useful!</u>

- **(INNER) JOIN**

  Returns records that <u>have matching values in both tables</u>

  - 是`join`的默认形式, 即上面的

    ```sql
    select animals.name, animals.species, diet.food
    from animals join diet
    on animals.species = diet.species
    where diet.food = 'fish';
    ```

    即为`inner join`

  `inner join` three tables:

  ```sql
  select order.order_id, customers.customer_name, shippers.shipper_name
  from (
      (
          orders join customers
          on orders.customer_id = customers.customer_id
      ) join shippers
      on orders.shipper_id = shippers.shipper_id
  );
  ```

- **LEFT (OUTER) JOIN**

  Returns <u>all records from the left table</u>, as well as the <u>matching records from the right table</u>

  *Determine "left table" and "right table":*

  `from left_table left join right table` or `from left_table, righ_table`

  ```sql
  select customers.customer_name, orders.order_id
  from customers left join orders
  on cutomers.customer_id = orders.customer_id
  order by customers.customer_name;
  ```

- **RIGHT (OUTER) JOIN**

  Returns <u>all records from the right table</u>, as well as the <u>matching records from the left table</u>

  *与left (outer) join是完全对称的*

  ```sql
  select orders.order_id, employees.last_name, employees.first_name
  from orders right join employees
  on orders.employee_id = employees.employee_id
  order by orders.order_id;
  ```

- **FULL (OUTER) JOIN**

  Returns <u>all records in both tables</u> when there is a match in either table

  *本质上是一个left (outer) join再补上right table中的剩余部分*

  ```sql
  select customers.curstomer_name, orders.order_id
  from customers full outer join orders
  on customers.customer_id = orders.customer_id
  order by customers.customer_name;
  ```

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/2-Operations/join-types.png?raw=true" width="500px">

------

<br>

### 2. Inserting Data to Table

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/2-Operations/insert-into_values.png?raw=true" width="600px">

A single `insert` statement can only <u>insert rows into a single table</u>.

<br>

### 3. Updating Data to Table

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/2-Operations/update.png?raw=true" width="500px">

```sql
update customers
set contact_name = 'Aflred Schmidt',
	city = 'Frankfurt'
where customer_id = 1;
```

<br>

### 4. Deleting Data in Table

**在实际设计DB时, 应该只使用逻辑删除 (把对应record的`is_del`设置为`true`), 而不使用物理删除 (实际删除掉对应record)**

```sql
delete from customers
where customer_name = 'Alfred Futterkiste';
```

Note that

```sql
delete from customers; -- Delete all the information (not including the headers) stored in the table, but not table itself
```

<br>

***

### Transaction

*SQLite:*

```sqlite
begin transaction;  -- Start a transaction
-- Some SQL changes
commit;  -- Commit the transaction, updating the DB with the above two changes at the same time

rollback;  -- Rollback to the last commit, aborting all the changes since then
```

*MySQL and PostgreSQL:*

```mysql
begin;  -- Start a transaction
-- Some SQL changes
commit;  -- Commit the transaction, updating the DB with the above two changes at the same time

rollback;  -- Rollback to the last commit, aborting all the changes since then
```

***
# Operations

## 0. 数据库操作

```mysql
# Create DB
create database test;

# Show all existing DBs
show databases;

# Delete DB
drop database test;
```

<br>

## 0. 表操作

#### (1) 创建表

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/2-Operations/create-table.png?raw=true" width="500px">

We can add `if not exists` between `table` and `tablename`, to create the table if it doesn't already exist.

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

- `primary key` (Essentially, a combination of `not null` and `unique`)

- `autoincrement`

  ***

  ```mysql
  -- MySQL:
  create table students (
      id integer primary key auto_increment,  -- "integer + auto_increment": "autoincrement"在MySQL的实现
      name varchar(20) not null,
      email varchar(100) not null
  );
  
  -- PostgreSQL:
  create table students (
      id serial primary key,  -- "serial": "autoincrement"在PostgreSQL的实现
      name varchar(20) not null,
      email varchar(100) not null
  );
  ```

  ***

- `foreign key`

<br>

##### 在表上创建索引:

```mysql
create index index_name
on some_table (column_name);
```

<br>

***

##### Temporary Table (临时表)

有点像一个temporary的变量, 来暂时储存intermediate的结果, 为了后续使用

- 创建得比真实的、持久化的表更快
- 当当前的客户端session终止时，删除此临时表

```mysql
create temporary table sandals as
    select *
    from shoes
    where shoe_type = 'sandals';
```

***

##### View (视图)

与temporary table不同的是, view本质上并没有写数据. 因此对于没有write权限的DB, 用view是更方便的

```mysql
-- Creation
create view brazil_customers as
    select name, contact_name
    from customers
    where country = 'Brazil';

-- Update
create or replace view brazil_customers as
    select name, contact_name, city
    from customers
    where country = 'Brazil';

-- Deletion
drop view brazil_customers;
```

***

<br>

#### (2) 修改表

```mysql
-- Rename table
alter table customers
rename to my_customers;

-- Add column
alter table customers
add email varchar(255);

-- Rename column
alter table customers
rename name to fullname;

-- Delete column
alter table customers
drop email;
```

HiveSQL 删除分区：

```hive
alter table some_db.some_table
drop partition (date = 'deprecated_part')
```

<br>

#### (3) 删除表

```mysql
truncate table scores;  -- 删除表中全部信息, 但不删除表本身

drop table scores;  -- 删除表中全部信息, 然后删除表
```

<br>

## 1. 向表中插入数据 (Creation)

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/2-Operations/insert-into_values.png?raw=true" width="600px">

注: 一条 `insert` 语句只能向一张表中插入数据

<br>

## 2. Query数据 (Retrieval)

#### (1) `where`

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/2-Operations/select_from_where.png?raw=true" width="600px">

```mysql
select name, birthdate
from animals
where species = 'gorilla'
    and name = 'Max';
```

注: `where` 生效在任何聚合之前

***

**`is null` operator** in `where` clause

```mysql
-- Select only null values:
select name, species
from animals
where birthdate is null;

-- Use "is not null" to select only non-null values:
select name, species
from animals
where birthdate is not null;
```

***

**`in` operator** in `where` clause

```mysql
-- Select from a selection of values:
select name, birthdate
from animals
where species in ('gorilla', 'llama', 'orangutan');

-- Use "not in" to exclude a selection of values:
select name, birthdate
from animals
where species not in ('gorilla', 'llama', 'orangutan');
```

------

**`between` operator** in `where` clause

```mysql
-- Select from a range of values (inclusive):
select name, species
from animals
where birthdate between '1993-07-31' and '1993-10-05';
-- This will include both '1993-07-31' and '1993-10-05'.

-- Use "not between" to exclude a range of values (exclusive):
select name, species
from animals
where birthdate not between '1993-07-31' and '1993-10-05';
-- This will include neither '1993-07-31' nor '1993-10-05'.
```

------

**`like` operator** in `where` clause

Select values that follow a pattern

Wildcards

- `%` represents any number of characters
- `_` represents a single character

```mysql
select name, birthdate
from animals
where species like '_r%';
-- This will select all the species that have 'r' at the second position.

-- Use "not like" to exclude values that follow a pattern:
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

**`case` clause: 类似大多数编程语言里的 `if-then-else` 逻辑 或者 `case` 逻辑**

```mysql
-- According to "quantity" field, add a corresponding description
select order_id, quantity,
    case
        when quantity > 30 then 'The quantity is greater than 30'
        when quantity = 30 then 'The quantity is 30'
        else 'The quentity is less than 30'
    end as quantity_description
from order_details;
```

注: `case` 语句命中第一个条件后就退出, 不会继续check后面的条件

<br>

#### (2) Aggregation (聚合): Compute a single value from a set of values)

- `count`

  <img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/2-Operations/select_from_group-by.png?raw=true" width="600px">

  ```mysql
  select name, count(*) as num
  from animals
  group by name;
  
  -- count(*) / count(1): 所有行都计数, 不忽略null, null也计数
  -- count([column_name]): 忽略null, 只计数not null的行
  ```
  
- `sum`

  ```mysql
  select sum(unit_price) as total_price
  from products;
  
  -- sum(*) / sum([column_name]): 忽略null, 只sum not null的行
  ```

***

**大坑！！！** `count` vs `sum` 在计算有条件count时的区别：

```mysql
select count(if(name = 'Jerry', 1, 0)) as jerry_cnt
from animals
where species = 'gorilla';
-- 这种语法本质上类似于 count([column_name]), 忽略null, 只计数not null的行
-- => 错误!!! 不管name是否 = 'Jerry', count(1) / count(0) 都会计数该行, 即该条件 未生效

select count(if(name = 'Jerry', 1, null)) as jerry_cnt
from animals
where species = 'gorilla';
-- 这种语法本质上类似于 count([column_name]), 忽略null, 只计数not null的行
-- => 正确, 即该条件 生效

select sum(if(name = 'Jerry', 1, 0)) as jerry_cnt
from animals
where species = 'gorilla';
-- 正确
```

***

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


------

**`having` clause: 类似 `where`, 但在所有聚合之后**

```mysql
select customer_id, count(*) as customer_orders
from orders
group by customer_id
having customer_orders >= 2;
```

------

<br>

#### (3) Subquery (子查询): Queries inside another query

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
) as subq;
```

***

**"Common Table Expression" ("公共表表达式") - `with` 结构**

与subquery本质上相同，只是一个syntax sugar. 👆🏻的subquery可以改写成:

```mysql
with qualified_customers as (
  	select distinct customer_id
		from orders
		where freight > 100;
)

select name, company_name, region
from customers
where id in qualified_customers;
```

***

<br>

#### (4) Join (合并): Linking multiples tables to extract the desired information

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/2-Operations/join-1-original_tables.png?raw=true" width="500px">

<u>Question: How many individual animals eat fish?</u>

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

## 3. 向表中更新数据 (Update)

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/2-Operations/update.png?raw=true" width="500px">

```mysql
update customers
set contact_name = 'Aflred Schmidt',
    city = 'Frankfurt'
where customer_id = 1;
```

<br>

## 4. 从表中删除数据 (Deletion)

**在实际设计DB时, 应该不使用物理删除 (即实际删除掉对应行), 而只使用逻辑删除 (即把对应行的`is_del`设置为`true`)**

```mysql
delete from customers
where customer_name = 'Alfred Futterkiste';
```


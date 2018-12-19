# Data Types in SQL

## Data Types in SQL

- `integer`

  - 约等于 Java `int` / Python `int`

- `decimal`

  An exact decimal value

  ```sql
  decimal(8, 2)
  -- At most 8 digits in total
  -- 2 digits to the right of the decimal place
  -- xxxxxx.xx
  ```

- `real`

  - $\approx$ Java `float`

- `double precision`

  - $\approx$ Java `double` / Python `float`

------

**Supported Math Operators (Only for Numerical Types)**

`+`, `-`, `*`, `/`, `%`

```sql
select product_id, units_on_order, unit_price,
	units_on_order * unit_price as order_total_cost  -- Calculate the each order's total cost
from products;
```

<u>Note that `/` is using integer division!!!</u>

------

- `text`

  - 约等于 Java `String` / Python `str`

  - Find index of first occurrence of substring: `instr(str, substr)`

    ***

    *MySQL*: `locate(substr, str, pos)`

    ```mysql
    select locate('bar', 'foobarbar', 5);
    
    -- 7
    ```

    ***

  - Change case: `upper(s)` / `lower(s)`

    ***

    *MySQL*: `upper(s)` = `ucase(s)`, `lower(s)` = `lcase(s)`

    ***

  - Trim: `trim(s)`, `ltrim(s)`, `rtrim(s)`

    - `trim(s)`: Trim the leading and trailing space
    - `ltrim(s)`: Trim only the leading space
    - `rtrim(s)`: Trim only the trailing space

    ***

    *MySQL:* `trim([{BOTH | LEADING | TRAILING} [remstr] FROM] str)`

    ```mysql
    select trim('   bar   ');  -- BOTH is assumed + space is assumed
    
    -- bar
    
    select trim(LEADING 'x' FROM 'xxxbarxxx');
    
    -- barxxx
    
    select trim(TRAILING 'xyz' FROM 'barxxyz');
    
    -- barx
    ```

    ***

  - Substring: `substr(str_name, str_pos, substr_length)`

    Note that `str_pos` starts from 1!!!

    ```sql
    select first_name, substr(first_name, 2, 3)  -- Select only 3 characters, starting from the 2nd character
    from employees
    where department_id = 60;
    
    
    select substr('MySQL', -2, 2);  -- Select only 2 characters, starting from the 1st character from the right
    
    -- QL
    ```

    ***

    *MySQL*: `substr()` = `substring()`

    ***

  - Concatenate: `||`

    ```sql
    select company_name, contact_name,
        company_name || ' (' || contact_name || ')'  -- Concatenate "company_name" and "contact_name"
    from customers;
    ```

    ***

    *MySQL*:

    * `concat(str1, str2, ...)`

      ```mysql
      select concat('My', 'S', 'QL');
      
      -- MySQL
      
      -- If any argument is null, return null.
      select concat('My', null, 'QL');
      
      -- null
      ```

    * `concat_ws(separator, str1, str2, ...)`

      ```mysql
      select concat_ws(',', 'First name', 'Second name', 'Last name');
      
      -- 'First name,Second name,Last name'
      
      -- If the separator is null, the result is null.
      select concat_ws(',', 'First name', null, 'Last name');
      
      -- null
      ```

    ***

- `char(n)`

  A string of exactly *n* characters

- `varchar(n)`

  A string of up to *n* characters

- `date`

  A calendar date, including year, month and day

  - Values are written like `'2014-04-13'`.

  - `date(timestring, modifier, modifier, ...) -> date`

    *有点像一个constructor*

    ```sql
    -- Get today's date
    select date('now');  -- 本质上相当于 select strftime('%Y-%m-%s', 'now')
    
    -- '2018-12-09'
    ```

- `time`

  A time of day

- `datetime` / `timestamp`

  `data` and `time` together

  - Values are written like `'2014-04-13 13:17:48'`.

  - `datetime(timestring, modifier, modifier, ...)`

    `timestamp(timestring, modifier, modifier, ...)`

    *有点像一个constructor*

    ```sql
    -- Get the current datetime
    select datetime('now');  -- 本质上相当于 select strftime('%Y-%m-%d %H-%M-%S', 'now')
    
    -- 2018-12-09 15:40:48
    ```

    ```sql
    -- Select employees who have worked for the compnay for 15 years or more
    select first_name, last_name, hire_date
    from employees
    where (date('now') - hire_date) >= 15;
    ```

------

**Reformat date and time strings: `strftime(timestring, modifier, modifier, ...) -> text`**

```sql
-- Parse out and reformat the current datetime to "Year Month Day"
select strftime('%Y %m %d', 'now')
from employees;

-- 1993 10 05
```

```sql
-- Parse out and reformat the current datetime to "Hour Minute Second Millisecond"
select strftime('%H %M %S %s', 'now')
from employees;

-- 15 40 48 785
```

```sql
-- Parse out certain pieces from "birthdate"
select birthdate,
    strftime('%Y', birthdate) as year,
    strftime('%m', birthdate) as month,
    strftime('%d', birthdate) as day,
    date('now') - birthdate as age
from employees;

-- birthdate  year month day age
-- 1993-10-05 1993  10   05  25
```

------

**To make the queries simple and easy to maintain, DO NOT ALLOW TIME COMPONENT IN THE DATES!**
# Data Types in SQL

## Data Types in SQL

- `integer`

  - 约等于 Java `int` / Python `int`

- `decimal`

  An exact decimal value

  ```mysql
  decimal(8, 2)
  -- At most 8 digits in total
  -- 2 digits to the right of the decimal place
  -- xxxxxx.xx
  ```

- `real`

  - 约等于 Java `float`

- `double`

  - 约等于 Java `double` / Python `float`

- `text`

  - 约等于 Java `String` / Python `str`
  ***

  | Functionality                                   | MySQL                                                        | PostgreSQL                                                   |
  | ----------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
  | Take length                                     | `length(s)`                                                  | Same                                                         |
  | Find the index of first occurrence of substring | `locate(substr, str, pos)`                                   | `position(substr in str) / strpos(str, substr)`              |
  | Change case                                     | `upper(s) / ucase(s)`, `lower(s) / lcase(s)`                 | `upper(s)`, `lower(s)`                                       |
  | Trim                                            | `trim([{BOTH | LEADING | TRAILING} [remstr] FROM] s)`<br>`ltrim(s)`, `rtrim(s)` *Trims leading/trailing spaces* | `trim([leading | trailing | both] [characters] from s)`      |
  | Take out leading/trailing characters            | `left(s, n)`, `right(s, n)`                                  | Same                                                         |
  | Substring                                       | `substring(s, str_pos, substr_length) / substr(...)`         | `substring(s [from int] [for int]) / substr(s, from [, count])` |
  | Concatenation                                   | `|| / concat(s1, s2, ...) / concat_ws(separator, s1, s2, ...)` | Same                                                         |
  | Concatenation in aggregation                    | `group_concat([column_name])`                                |                                                              |
  | Replacement                                     | `replace(s, from_str, to_str)`                               | Same                                                         |

  MySQL examples:

  ```mysql
  select locate('bar', 'foobarbar', 5);
  -- 7 (1-based index)
  ```

  ```mysql
  select trim('   bar   ');  -- BOTH is assumed + space is assumed
  -- bar
  
  select trim(LEADING 'x' FROM 'xxxbarxxx');
  -- barxxx
  
  select trim(TRAILING 'xyz' FROM 'barxxyz');
  -- barx
  ```

  ```mysql
  select first_name, substr(first_name, 2, 3)  -- Select only 3 characters, starting from the 2nd character
  from employees
  where department_id = 60;
  -- Note that str_pos uses 1-based index!!!
  ```

  ```mysql
  select company_name, contact_name,
      company_name || ' (' || contact_name || ')'  -- Concatenate "company_name" and "contact_name"
  from customers;
  
  select concat('My', 'S', 'QL');
  -- MySQL
  
  -- If any argument is null, return null.
  select concat('My', null, 'QL');
  -- null
  
  select concat_ws(',', 'First name', 'Second name', 'Last name');
  -- 'First name,Second name,Last name'
  
  -- If any argument is null, return null.
  select concat_ws(',', 'First name', null, 'Last name');
  -- null
  ```

  ```mysql
  select sell_date, group_concat(distinct product order by product)
  group by sell_date;
  -- For each sell_date, collect the distinct products, order them lexicographically, and finally concatenates with ","
  ```

  ```mysql
  select replace('www.mysql.com', 'w', 'Ww')
  -- WwWwWw.mysql.com
  ```

  ***

- `char(n)`

  A string of exactly *n* characters

- `varchar(n)`

  A string of up to *n* characters

- `date`

  A calendar date, including year, month and day

  - Values are written like `'2014-04-13'`.

- `time`

  A time of day

- `datetime` / `timestamp`

  `data` and `time` together

  - Values are written like `'2014-04-13 13:17:48'`.

Check out `Date Types.md` for more about date-related types

------

**To make the queries simple and easy to maintain, <u>DO NOT ALLOW TIME COMPONENT IN THE DATES!</u>**


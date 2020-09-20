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

  - Find index of first occurrence of substring: `instr(str, substr)`

    ***

    *MySQL*: `locate(substr, str, pos)`

    ```mysql
    select locate('bar', 'foobarbar', 5);
    -- 7 (1-based index)!!!
    ```
    
  ***
  
  - Change case: `upper(s)` / `lower(s)`

    ***

    *MySQL*: `upper(s)` = `ucase(s)`, `lower(s)` = `lcase(s)`

    ***

  - Trim: `trim(s)`, `ltrim(s)`, `rtrim(s)`

    - `trim(s)`: Trim the leading and trailing spaces
    - `ltrim(s)`: Trim only the leading spaces
    - `rtrim(s)`: Trim only the trailing spaces

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

    Note that `str_pos` uses 1-based index!!!

    ```mysql
    select first_name, substr(first_name, 2, 3)  -- Select only 3 characters, starting from the 2nd character
    from employees
    where department_id = 60;
    ```
    
    ***
    
    *MySQL*: `substr(...)` = `substring(...)`
    
    ***
    
  - Concatenation: `||`

    ```mysql
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
      
      -- If any argument is null, return null.
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

- `time`

  A time of day

- `datetime` / `timestamp`

  `data` and `time` together

  - Values are written like `'2014-04-13 13:17:48'`.

Check out `Date Types.md` for more about date-related types

------

**To make the queries simple and easy to maintain, <u>DO NOT ALLOW TIME COMPONENT IN THE DATES!</u>**


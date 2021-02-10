## SQLite

有点像constructor

`date(timestring, modifier, modifier, ...) -> date`

```sqlite
-- Get today's date
select date('now');  -- 本质上等效于 select strftime('%Y-%m-%s', 'now')
-- '2018-12-09'
```



`datetime(timestring, modifier, modifier, ...) -> datetime`

```sqlite
-- Get the current datetime
select datetime('now');  -- 本质上等效于 strftime('%Y-%m-%d' %H:%M:%S, 'now')
-- 2018-12-09 15:40:48
```

```sqlite
-- Select employees who have worked for the compnay for 15 years or more
select first_name, last_name, hire_date
from employees
where (date('now') - hire_date) >= 15;
```



`timestamp(timestring, modifier, modifier, ...) -> timestamp`



Reformat date and time strings: `strftime(format, timestring, modifier, modifier, ...) -> string`

```sqlite
-- Parse out and reformat the current datetime to "Year Month Day"
select strftime('%Y %m %d', 'now');
-- 1993 10 05
```

```sqlite
-- Parse out and reformat the current datetime to "Hour Minute Second Millisecond"
select strftime('%H %M %S %s', 'now');
-- 15 40 48 785
```

```sqlite
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

***

<br>

## MySQL

Check out https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html

<br>

## PostgreSQL

```sql
-- Truncate the given timestamp to the given precision

select date_trunc('hour', timestamp '2001-02-16 20:38:40');
-- 2001-02-16 20:00:00

select date_trunc('year', timestamp '2001-02-16 20:38:40');
-- 2001-01-11 00:00:00
```



```sql
--- Parse out certain pieces from "birthdate"
select birthdate,
		date_part('year', birthdate) as year,
		date_part('month', birthdate) as month,
		date_part('day', birthdate) as day
from employees;
-- birthdate  year month day
-- 1993-10-05 1993  10   05
```

<br>

**To make the queries simple and easy to maintain, <u>DO NOT ALLOW TIME COMPONENT IN THE DATES!</u>**


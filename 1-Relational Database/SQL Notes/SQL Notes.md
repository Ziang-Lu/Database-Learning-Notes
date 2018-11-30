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

Note: Use `*` to select all columns

**Supported Logic Operators**

`and`, `or`, `not` (same as Python)

**Supported Comparison Operators**


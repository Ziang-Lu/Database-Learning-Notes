# Python DB-API

## Overview

**Python DB-API is NOT a particular Python library.**

**Python DB-API is an API standard that different Python libraries (drivers) with different DB systems must follow, to let your code connect to the different underlying DBs**

e.g., Python DB-API specifies <u>which functions you should call</u> to connect to a DB, send queries, and get results, <u>regardless of the actual DB system</u>.

=> If you <u>learned Python DB-API</u> functions, you should be able to <u>apply it to any DB systems</u>.

<br>

## Workflow

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/3-Python%20DB-API/python_db-api_workflow.png?raw=true" width="600px">

**Whenever we make changes to a DB, these changes will go into a <u>transaction</u>, and it will take effect only when we call `conn.commit()` method.**

=> **"Atomicity": A transaction happens as a whole, or not at all.**

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/3-Python%20DB-API/transaction_1.png?raw=true" width="500px">

=> If we close a connection or the code crashes without committing the changes, the changes will be <u>rolled back</u>.

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/3-Python%20DB-API/transaction_2.png?raw=true" width="500px">

*Note:*

*During the execution of the SQL statements within a transaction, these changes are still VISIBLE to the developer.*

*i.e., If we do `select` within a transaction, we can still see the changes we made.*

*But they are just not committed and not updated to the DB server.*

<br>

## Implementations

The following Python modules <u>all follow Python DB-API</u>.

| DB Management System |                Python DB-API Library (Driver)                |
| :------------------: | :----------------------------------------------------------: |
|        MySQL         | <a href="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/2-MySQL/mysql-connector_demo.py">`mysql.connector-python`</a><br/><a href="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/2-MySQL/pymysql_demo.py">`PyMySQL`</a> |
|      PostgreSQL      | <a href="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/3-PostgreSQL/psycopg2_demo.py">`psycopg2`</a> |

***

*Check out the corresponding demo program for detailed usage*

<br>

***

### Object-Relational Mapping (对象-关系映射) (ORM)

#### Problem:

Assume we have the following `users` table:

```sql
create table users (
    id integer primary key,
    name varchar(20) not null
);
```

Data structure returned by Python DB-API:

```python
# A list of tuples, where each tuple represents a record
[
    (1, 'Michael'),
    (2, 'Bob'),
    (3, 'Adam')
]
```

which is <u>not so intuitive</u>.

#### ORM: Change each table to a class, and each record (tuple) in that table to an object of that class

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/3-Python%20DB-API/orm.png?raw=true" width="500px">

| DB Representation | Table | Column (Field)  | Record |
| ----------------- | ----- | --------------- | ------ |
| ORM               | Class | Class attribute | Object |

In this way, writing code is much easier, since we <u>don't need to write SQL statements anymore</u>, but <u>just need to define plain Python classes (for tables) and objects (for records)</u>.

```python
# Similar to the following:
class User:
    """
    User class.
    """

    def __init__(self, id: int, name: str):
        """
        Constructor with parameter.
        :param id: int
        :param name: str
        """
        self._id = id
        self._name = name

    def __repr__(self):
        return f'User(id={self._id}, name={self._name})'

[
    User(id=1, name='Michael'),
    User(id=2, name='Bob'),
    User(id=3, name='Adam')
]
```

***

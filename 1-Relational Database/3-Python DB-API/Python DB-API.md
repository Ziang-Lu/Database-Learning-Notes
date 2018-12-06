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

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/3-Python%20DB-API/transaction_1.png?raw=true" width="400px">

=> If we close a connection or the code crashes without committing the changes, the changes will be <u>rolled back</u>.

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/3-Python%20DB-API/transaction_2.png?raw=true" width="400px">

<br>

## Implementations

The following Python modules <u>all follow Python DB-API</u>.

| DB Management System | Python DB-API Library (Driver) |
| :------------------: | :----------------------------: |
|        SQLite        |           `sqlite3`            |
|        MySQL         | `mysql.connector`<br>`pymysql` |
|      PostgreSQL      |           `psycopg2`           |

***

*Check out the corresponding demo program for detailed usage*


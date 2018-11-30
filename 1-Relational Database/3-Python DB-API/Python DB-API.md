# Python DB-API

## Overview

**Python DB-API is NOT a particular Python library.**

**Python DB-API is an API standard that different Python libraries with different DB systems must follow, to let your code connect to the different underlying DBs**

e.g., Python DB-API specifies <u>which functions you should call</u> to connect to a DB, send queries, and get results, <u>regardless of the actual DB system</u>.

=> If you <u>learned Python DB-API</u> functions, you should be able to <u>apply it to any DB systems</u>.

<br>

## Implementations

The following Python modules <u>all follow Python DB-API</u>.

| DB System  | Python DB-API Module |
| :--------: | :------------------: |
|   SQLite   |      `sqlite3`       |
|   MySQL    |  `mysql.connector`   |
| PostgreSQL |      `psycopg2`      |


# Database Learning Notes

These repo contains course notes in the following courses:

* **Database Systems Concepts & Design** from *Georgia Tech* on Udacity
* **Intro to Relational Database** on Udacity
* **SQL for Data Science** from *University of California, Davis* on Coursera

<br>

## Benefits

DB enables **safe concurrent access by multiple programs/users**.

***

*Why not just fetch all the data from DB to my application code, and do all the data operations there?*

* **Speed**

  <u>DB do the operations much faster.</u>

* **Space**

  Usually the data scale is too large to fit in memory or will take up too much memory.

<br>

## Data Model (数据模型)

**Data Modeling** is a way to **organize and join data**.

*Data Model should always represent a real-world problem as closely as possible.*

<br>

## DB Types (本质上是Data Model的不同type)

* Relational DB (关系型数据库)

  操作数据都是通过SQL statements来完成的

  * <a href="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Relational%20DB%20Concepts/Relational%20DB%20Concepts.md">Relational DB Concepts</a>
  * SQL Notes
    * <a href="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/1-Data%20Types%20in%20SQL/Data%20Types%20in%20SQL.md">Data Types in SQL</a>
    * <a href="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/2-SQL%20Notes/2-Operations/Operations.md">Operations</a>
      * Operations on DB
      * Fetching Data from DB
      * Inserting Data to Table
      * Updating Data in Table
      * Deleting Data in Table
  * <a href="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/3-Python%20DB-API/Python%20DB-API.md">Python DB-API</a>
  * Relational DB Management System (RDBMS) (关系型数据库管理系统)
    * <a href="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/2-SQLite/SQLite.md">SQLite</a>
      * 轻量级、嵌入式DB
      * 其一个DB就是一个文件(`xxx.db`), 存储在disk上
      * => 经常被集成到桌面和移动端应用之中
      * 不能承受高concurrency访问
      * Python support: `sqlite3`
    * <a href="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/3-MySQL/MySQL.md">MySQL</a>
      * 为server-side设计的, 使用最广泛的DB server
      * 能承受高concurrency访问
      * Python support: `mysql-connector-python` / `PyMySQL`
    * <a href="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/4-PostgreSQL/PostgreSQL.md">PostgreSQL</a>
      * 为server-side设计的, 使用流行度呈上升趋势
      * 能承受高concurrency访问
      * Python support: `psycopg2`
    * Oracle
      * 不开源、付费

* Not-only SQL (NoSQL)

  操作数据都是通过commands或prorgamming language来完成的

  * Key-value store (键-值存储)

    适用于要存储的data type相对简单, 但需要极高的retrieve和insert速度的嵌入式场景

    * <a href="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/5-Redis/Redis.md">Redis</a>
      * 存储的data有结构, 用来存储`String`, `List` (linked-list), `Hash` (hash table), `Set` (set), `SortedSet` (tree set) 等data type
      * => 常用作data structure server
      * Python support: `redis`
  * Document store (文档存储)

    * <a href="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/6-MongoDB/MongoDB.md">Mongo DB</a>

      => 多用于data的采集和分散处理 (Map/Reduce), 特别是在大数据处理方面比较擅长

<br>

***

**TIPS: Before Working through a Data Science Problem**

1. <u>Business Understading (业务理解)</u>

   - Understand the business problem to solve, and clarify the business goal
   - Translate this business understanding to a problem that the data analysis is trying to solve, and establish the success criteria for the data analysis

2. <u>Data Understanding (数据理解)</u>

   * <u>Data Governance (数据管制) / Data Profiling (数据剖析)</u>

     * Examine data accessibilty, availability

       *即查看公司对于data是如何管理的, 也查看自己对于哪些data有哪些权限*

   * <u>Data Profiling (数据剖析)</u>

     * Examine data completeness, consistency and accuracy
     * Summarize the potential problems in the data

   * e.g.. pay attention to the data type for each column in each table

   * e.g., figure out the relationships between tables, i.e., how the tables are linked together

     *(=> Foreign keys)*

***

<br>

## License

This repo is distributed under the <a href="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/LICENSE">MIT license</a>.

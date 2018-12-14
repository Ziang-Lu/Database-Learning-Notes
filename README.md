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

* Navigational DB (导航型数据库)
* Relational DB (关系型数据库) ***
  * <a href="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Relational%20DB%20Concepts/Relational%20DB%20Concepts.md">Relational DB Concepts</a>
  * SQL Notes
    * Data Types in SQL
    * Operations
      * Operations on DB
      * Fetching Data from DB
      * Inserting Data to Table
      * Updating Data in Table
      * Deleting Data in Table
  * <a href="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/3-Python%20DB-API/Python%20DB-API.md">Python DB-API</a>
  * Relational DB Management System (关系型数据库管理系统)
    * SQLite
      * 轻量级、嵌入式DB
      * 其一个DB就是一个文件(`xxx.db`), 存储在disk上
      * => 经常被集成到桌面和移动端应用之中
      * 不能承受高concurrency访问
    * MySQL ***
      * 为server-side设计的, 使用最广泛的DB server
      * 能承受高concurrency访问
    * PostgreSQL ***
    * Oracle
      * 不开源、付费
* Not-only SQL (NoSQL) ***
  * Key-value store (键-值存储)
    * 适用于数据类型相对简单, 但需要极高的retrieve和insert速度的嵌入式场景
      * Redis ***
  * Document store (文档存储)
    * Mongo DB ***

<br>

***

**Working through a Data Science Problem**

1. <u>Business Understading (业务理解)</u>

   - Understand the business problem to solve, and clarify the business goal
   - Translate this business understanding to a problem that the data analysis is trying to solve, and establish the success criteria for the data analysis

2. <u>Data Understanding (数据理解)</u>

   * <u>Data Governance (数据管制) / Data profiling (数据剖析)</u>
     * Examine data accessibilty, availability, completeness, consistency and accuracy
     * Summarize the potential problems in the data

   * e.g.. pay attention to the data type for each column in each table

   * e.g., figure out the relationships between tables, i.e., how the tables are linked together

     *(=> Foreign keys)*

***

<br>

## License

This repo is distributed under the <a href="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/LICENSE">MIT license</a>.


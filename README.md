# Database Learning Notes

These repo contains course notes in the following courses

* Intro to Relational Database on Udacity

<br>

DB enables **safe concurrent access by multiple programs/users**.

## Benefits

*Why not just fetch all the data from DB to my application code, and do all the data operations there?*

* **Speed**

  <u>DB do the operations much faster.</u>

* **Space**

  Usually the data scale is too large to fit in memory or will take up too much memory.

<br>

## Types

* Navigational DB (导航型数据库)
* **Relational DB (关系型数据库)**
  * SQLite
    * 嵌入式DB, 其DB就是一个文件
    * 经常被集成到桌面和移动端应用之中
  * **MySQL**
  * **PostgreSQL**
  * Oracle
    * 不开源、付费
* Key-value store (键-值存储)
  - 适用于数据类型相对简单, 但需要极高的retrieve和insert速度的嵌入式场景
  - **Non-Relational DB (非关系型数据库) (NoSQL)**
    - **MongoDB**
    - **Redis**

<br>

## Communication with DB

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/comm_with_DB.png?raw=true" width="500px">

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/comm_with_DB_impl.png?raw=true" width="600px">

<br>

## License

This repo is distributed under the <a href="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/LICENSE">MIT license</a>.


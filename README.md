# Database Learning Notes

This repo contains course notes in the following courses:

* **Database Systems Concepts & Design** from *Georgia Tech* on Udacity
* **Intro to Relational Database** on Udacity
* **SQL for Data Science** from *University of California, Davis* on Coursera

<br>

## Benefits

*Why not just fetch all the data from DB to my application code, and do all the data operations there?*

* **Speed**

  <u>DB do the operations much faster.</u>

* **Space**

  Usually the data scale is too large to fit in memory, or will take up too much memory.

<br>

## DB Types

### Relational DB (关系型数据库) => Relational DB Management System (RDBMS) (关系型数据库管理系统)

* SQLite
  * 轻量级、嵌入式DB
  * 其一个DB就是一个文件(`xxx.db`), 存储在disk上
  * => 经常被集成到桌面和移动端应用之中
  * 不能承受高concurrency访问
* <a href="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/2-MySQL/MySQL.md">MySQL</a>
  * 为server-side设计的, 使用最广泛的DB server
  * 能承受高concurrency访问
* <a href="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/3-PostgreSQL/PostgreSQL.md">PostgreSQL</a>
  * 为server-side设计的, 使用流行度呈上升趋势
  * 能承受高concurrency访问
* Oracle
  * 不开源、付费

优点:

* data的每个table都非常规整, 确保了每一个row (record) 都有相同数量的column (field)
* 通过foreign key的使用, 可以减少数据冗余

缺点:

* 很多时候为了拿到某个information, 需要把多个table join起来, 这是一个很耗时且占用资源的操作

<br>

### Not-only SQL (NoSQL)

#### Key-value store (键-值存储)

适用于要存储的data type相对简单, 但需要极高的retrieve和insert速度的嵌入式场景

* <a href="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/4-Redis/Redis-Basics.md">Redis</a>
  * In-memory存储
  
  * 存储的data有结构, 用来存储`String`, `List` (linked-list), `Hash` (hash table), `Set` (set), `SortedSet` (tree set) 等data type
  
  * => 常用作data structure server
  
  * 由于是in-memory存储, 所以也常常用作在application layer和实际DB (比如MySQL) 之间的一层cache来使用
  
    -> 详情看Redis overview页面

<br>

#### Document Store (文档存储)

Basic Concepts:

| Document store    | Relational DBMS |
| ----------------- | --------------- |
| DB                | DB (same)       |
| Collection (集合) | Table           |
| Document (文档)   | Record          |

* <a href="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/5-MongoDB/MongoDB.md">MongoDB</a>
    * 能承受高concurrency访问
    * => 多用于data的采集和分散处理 (Map/Reduce), 特别是在大数据处理方面比较擅长

<br>

#### Graph Store (图存储)

e.g., 每个entity对应一个node; 每个relation对应一条edge

<br>

## License

This repo is distributed under the <a href="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/LICENSE">MIT license</a>.

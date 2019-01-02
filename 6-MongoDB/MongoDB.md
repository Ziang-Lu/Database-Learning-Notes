# MongoDB

**Document store (文档存储)**

Basic Concepts:

| Document store    | Relational DBMS |
| ----------------- | --------------- |
| DB                | DB (same)       |
| Collection (集合) | Table           |
| Document (文档)   | Record          |

Difference between document and record:

* <u>All the documents don't necessarily have to have exactly the same fields, but in Relational DBMS, as long as a table is defined, all the records need to have the same fields.</u>

* <u>We can freely add fields to an existing document (本质上与上面一条相同).</u>

  ***

  But how to implement?

  *(On disk, there are already existing files, leaving the available spaces to be scattered. (See the below diagram))*



  * Copy the document to the next allocated space, add the new field to it, and delete the previous document

    *But in this way, there is a space fragment at the previous document's location, which leads an increased space fragment between documents and thus slower read & write speed.*

  * => Pre-allocate some padding space for each document, and each time a new field is added to a document, it is written to that document's corresponding padding space.

    *In this way, the document to which a new field is added still locates on its original space.*

  ***

<br>

## Overview

=> 多用于data的采集和分散处理 (Map/Reduce), 特别是在大数据处理方面比较擅长

<br>

## Setup

* Download and install PostgreSQL from `homebrew`

  ```bash
  > brew install mongodb
  ```

<br>

## Start/Stop MongoDB Server

**Start MongoDB Server   (Non-daemon process)**

```bash
> mongod --config /usr/local/etc/mongod.conf
```

**Stop MongoDB Server**

`ctl-C`

<br>

## MongoDB Command-Line Interface

```bash
> mongo
```

***

**[Inside the interactive shell] Common commands**

```bash
show dbs  # Show all the databases on the MongoDB server

use test  # Enter "test" database; create "test" database if it doesn't exist

db.stats()  # Display the statistics about the current database

db.createCollection("posts")  # Create a collection called "posts" in "test" database

show collections  # Show all the collections in "test" database

db.posts.drop()  # Delete the c

db.dropDatabase()  # Delete the current database
```

***
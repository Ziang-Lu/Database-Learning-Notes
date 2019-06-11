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

  <img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/5-MongoDB/documents_scattered.png?raw=true" width="400px">

  * Copy the document to the next allocated space, add the new field to it, and delete the previous document

    *But in this way, there is a space fragment at the previous document's location, which leads to an increased space fragment between documents and thus slower read & write speed.*

  * => Pre-allocate some padding space for each document, and each time a new field is added to a document, it is written to that document's corresponding padding space.

    *In this way, the document to which a new field is added still locates on its original space.*

    <img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/5-MongoDB/documents_with_padding.png?raw=true" width="200px">

  ***

<br>

## Overview

=> 多用于data的采集和分散处理 (Map/Reduce), 特别是在大数据处理方面比较擅长

<br>

## Setup

 * Download and install MongoDB from `homebrew`

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

or

```bash
> mongo test  # Directly enter "test" database
```

***

**[Inside the interactive shell] Common commands**

* DB-level commands

  ```javascript
  show dbs;  // Show all the databases on the MongoDB server
  
  use test;  // Enter "test" database; create "test" database if it doesn't exist
  
  db.stats();  // Display the statistics about the current database
  
  db.dropDatabase();  // Delete the current database
  ```

* Collection-level commands

  ```javascript
  db.createCollection("posts");  // Create a collection called "posts" in "test" database
  
  show collections;  // Show all the collections in "test" database
  
  db.posts.renameCollection("articles");  // Rename the "posts" to "articles"
  
  db.posts.drop();  // Delete the "posts" collection
  ```

* Document-level commands

  * Insert documents

    ````javascript
    db.posts.insert({
        title: "My First Blog",
        content: "What to write???",
        tags: ["diary"]
    })
    
    for (let i = 2; i <= 10; ++i) {
        db.posts.insert({
            title: "Blog-" + i,
            content: ""
        })
    };
    ````

  * Select documents

    ```javascript
    // Filtering
    
    db.posts.find()  // Select all the documents in "posts" collection
    db.posts.find({tag: "diary"});  // ... where "tag" is "diary" ...
    db.posts.find({rank: {$gte: 5}});  // ... where "rank" >= 5 ...
    // We can also use $gt, $lte, $lt, $eq and $ne to represent >, <=, <, = and !=, respectively.
    // But for $eq, we can simply use "tag": "diary".
    
    // We can also use regex to specify the selection condition.
    db.posts.find({title: /u/});  // ... whose title contains "u" ...
    db.posts.find({title: /^R/});  // ... whose title starts with "R" ...
    
    db.posts.find({$or: [{tag: "diary"}, {rank: {$gte: 5}}]});  // ... where "tag" is "diary" OR "rank" >= 5 ...
    // We can also use $and to represent "AND".
    // But, we can simply combine the selection conditions into one single JSON object.
    
    db.posts.find({rank: {$exists: true}});  // ... where "rank" field exists ...
    db.posts.find({rank: {$in: [3, 4, 5]}});  // ... where "rank" is in [3, 4, 5] ...
    
    // Projection
    
    db.posts.find({}, {title: true, rank: true});  // Select all the documents in "posts" collection, but only select out "title" and "rank" fields
    // Note that if a document only has some matchings of the specified fields, that document still will be selected out with only those matchings
    
    // However, by default, MongoDB also selects out "_id". Therefore to avoid this, we need to
    // db.posts.find({}, {title: true, rank: true, _id: false});
    
    // Post-processing
    
    db.posts.distinct("name");  // Select all the distinct "name"s in the documents in "posts" collection
    
    db.posts.find().sort({rank: 1});  // Select all the documents in "posts" collection, sorted by "rank" in ascending order
    db.posts.find().sort({rank: -1});  // ... in descending order
    db.posts.find().sort({rank: 1}).limit(3);  // Select the first 3 documents ...
    db.posts.find().sort({rank: 1}).skip(10).limit(3);  // Skipping the first 10, select the first 3 documents ...
    
    db.posts.count();  // Count the number of documents in "posts" collection
    ```

  * Update documents (Manipulate fields)

    ```javascript
    // Update the entire document
    
    db.posts.update({title: "My First Blog"}, {rank: 99});  // Change the document where "title" is "My First Blog" in "posts" collection, deleting all the fields and setting only one field: "rank" is 99
    // This is DANGEROUS!!!
    
    db.posts.update({title: "My First Blog", {title: "My First Blog", rank: 99, tag: "diary"}}, {upsert: true});  // ..., deleting all the fields and setting the specified fields
    // (UPSERT) if the document does not exist, create the document
    
    
    // Update fields
    
    db.posts.update({tag: "diary"}, {$set: {rank: 10}});  // Set "rank" to be 10 for the FIRST!!! document where "tag" is "diary" in "posts" collection
    db.posts.update({tag: "diary"}, {$set: {rank: 10}}, {multi: true});  // ... all the documents ...
    // Note that if the field doesn't exist for a document, it will be created
    
    db.posts.update({title: "My First Blog"}, {$inc: {rank: 5}});  // Increment "rank" by 10 for the document where "title" is "My First Blog" in "posts" collection
    db.posts.update({title: "My First Blog"}, {$mul: {rank: 2}});  // Multiply "rank" by 2 ...
    
    db.posts.update({title: "My First Blog"}, {$rename: {rank: "ranking"}});  // Rename "rank" field to "ranking" ...
    
    
    // Delete fields
    
    db.posts.update({title: "My First Blog"}, {$unset: {rank: ""}});  // Delete "rank" field ...
    ```

  * Delete documents

    ```javascript
    db.posts.remove({});  // Delete all the documents in "posts" collection
    db.posts.remove({title: "Blog"});  // ... where "title" is "Blog" ...
    ```

* Index commands

  ```javascript
  db.posts.getIndexes();  // Get all the indexes of "posts" collection
  // By default, MongoDB will provide an index on "_id".
  
  db.posts.createIndex({rank: -1});  // Create an index on "rank" in descending order in "posts" collection
  db.posts.createIndex({title: 1}, {unique: true});  // ... on "title" in ascending order and must be unique ...
  // Since this index specifies that "title" must be unique, it can work as a PRIMARY KEY.
  
  db.posts.dropIndex({rank: -1});  // Delete the index on "rank" in descending order in "posts" collection
  ```

***

<br>

## MongoDB Aggregation Framework

**-> Built-in analytics tools**

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/5-MongoDB/aggregation_framework_overview.png?raw=true" width="400px">

<br>

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/5-MongoDB/aggregation_framework_stage.png?raw=true" width="400px">

*(Similar to Linux shell pipeline)*

For more practical examples of Aggregation Framework, check out the MFlix project:

https://github.com/Ziang-Lu/Intro-to-MongoDB/tree/master/notebooks

<br>

## Python Support

`PyMongo`

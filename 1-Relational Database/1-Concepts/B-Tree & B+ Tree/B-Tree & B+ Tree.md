## B-Tree & B+ Tree

### Definition

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Relational%20DB%20Concepts/B-Tree%20&%20B+%20Tree/B-Tree%20Definition.png?raw=true" width="600px">

*从操作上讲: Search的次数比insertion、deletion要多得多*

### Search

The idea is similar to a normal BST.

### Insertion

1. Follow a similar procedure as searching, finding the leaf to insert the new key

2. Check whether the leaf is full:

   * Not full:

     Simply insert the new key

   * Full:

     Split the leaf to two leaves, percolating up the middle key to the parent node

     *-> If necessary (the parent node is also full), repeat the same splitting and percolating up procedure, upwards*

<br>

### Database Multi-level Indexing

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Relational%20DB%20Concepts/B-Tree%20&%20B+%20Tree/Multilevel%20Indexing.png?raw=true" width="600px">

**=> This form of multi-level indexing leads to the use of B-tree.**

Compare to a pure B-tree structure:

* **Keys in a node <=> Primary keys of the table to create an index on**
* **For each key, store the corresponding table record address associated with it**

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Relational%20DB%20Concepts/B-Tree%20&%20B+%20Tree/B-Tree%20Multilevel%20Indexing.png?raw=true">

<br>

## B+ Tree

应用在database multi-level indexing上, 与B-tree实现的区别:

* **所有的key-record mapping都存在leaf中**
* **而在internal nodes中只存储keys, 而不再存储对应的record address**

与最上方相同的B-Tree, 其B+ tree的结构如图:

<img src="https://github.com/Ziang-Lu/Database-Learning-Notes/blob/master/1-Relational%20Database/1-Relational%20DB%20Concepts/B-Tree%20&%20B+%20Tree/B+%20Tree%20Demo.png?raw=true">

*注意: 当split内部node时, 由于我们只存储key而不存储对应的record address, 则无需再保存重复的key即可正确nagivate至正确的leaf中*


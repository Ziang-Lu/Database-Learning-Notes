# Geospatial DB with Geohashing

Imagine we design an App like Yelp, we may have the following relational DB schema:

**USERS**

| id (Primary Key) | username |
| ---------------- | -------- |
| 1                |          |
| 2                |          |
| 3                |          |

**PLACES**

| id (Primary Key) | name | long | lat  |
| ---------------- | ---- | ---- | ---- |
| 1                |      |      |      |
| 2                |      |      |      |
| 3                |      |      |      |

**RATINGS**

| id (Primary Key) | user_id (Foreign Key) | place_id (Foreign Key) | rating |
| ---------------- | --------------------- | ---------------------- | ------ |
| 1                | 2                     | 1                      |        |
| 2                | 3                     | 1                      |        |
| 3                | 1                     | 2                      |        |

**COMMENTS**

| id (Primary Key) | user_id (Foreign Key) | place_id (Foreign Key) | content |
| ---------------- | --------------------- | ---------------------- | ------- |
| 1                | 2                     | 1                      |         |
| 2                | 1                     | 2                      |         |
| 3                | 1                     | 3                      |         |

However, consider the following <u>use case</u>:

**For a user with some location information, find the places within some proximity.**

<u>Naive solution:</u>

Scan through all the places, and do a range query based on the user's longitude and latitude, comparing to the longitude and latitude of each place.

Normally, we use Index to speed up queries, but *Index is usually designed for string queries*, so the above range query is very SLOW!!!

<u>Optimized solution: (Sharding + Geohashing)</u>

1. Sharding

   Consider our use case, we can shard the DB into different regions, like North America, Asia, ...

2. Geohashing

   * Split a shard into larger to smaller geohashing strings

     *e.g., "9C23AB" would zoom in the shard to "9", and within "9", zoom in to "C", …...*

     In this way, if we take a geohashing string:

     * Remove a trailing character => Zoom out one level
     * Add a trailing character => Zoom in one level

   * Save the geohashing string to another column in PLACES table like this:

     | id (Primary Key) | name | long | lat  | geohashing_6 | geohashing_5 | geohashing_4 |
     | ---------------- | ---- | ---- | ---- | ------------ | ------------ | ------------ |
     | 1                |      |      |      | 9C23AB       | 9C23A        | 9C23         |
     | 2                |      |      |      |              |              |              |
     | 3                |      |      |      |              |              |              |

     In this way, when a user wants find the places within some proximity, we just need to:

     * Convert the user's location information to a geohashing string

     * Based on the desired proximity, determine the number of geohashing string characters to use

       * The more the number of characters to use, the finer the search will be, and vice versa.

     * In this way, the previous range query on two columns => one string query on one column

       We can *create Index for each geohashing string length (Geospatial Index), to speed up the queries*.


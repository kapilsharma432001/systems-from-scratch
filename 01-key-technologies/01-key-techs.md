- System design involves assembling the most effectivce building blocks to solve a problem, so it's crucial to have a good understanding of most commonly used building blocks.

## Core Database
- Almost all system design problems will require you to store some data and you're most likely going to be storing it in a database (or Blob Storage).
- While there are many different types of databases, the most common are relational databases (e.g. Potgres) and NoSQL databases (e.g. DynamoDB) - recommendation is picking one of them for the interview.
- If you're taking predominently product design interviews - recommendation is picking a relational database.
- If you're taking predominentely infrastructure design interviews - recommendation is picking a NoSQL database.

![Choosing SQL or NoSQL](image.png)

- Choosing SQL or NoSQL is a choice - but whatever you are choosing - choose with a reason - choose it because it is solving some problem of yours. Like "I am using Postgres here because its ACID properties will allow me to maintain data integrity."
# biotrends
Author:  Dario Ghersi

Collection of simple scripts to track the "popularity" of MeSH terms in the biomedical literature.

## Setup

### MySQL database creation

As ```MySQL``` root user, create the ```medline``` user and database:

```

CREATE USER 'medline'@'localhost' IDENTIFIED BY 'pubmed2015';
CREATE DATABASE medline;
GRANT ALL ON medline.* TO 'medline'@'localhost';

```

Then, as ```medline``` user run the ```createTables.sql```:

```
mysql --database medline -u medline -p < createTables.sql
```

### Populate the MySQL database


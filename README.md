# biotrends
Author:  Dario Ghersi

Required module: pymysql

Collection of simple scripts to track the "popularity" of MeSH terms in the biomedical literature.

## Setup

### MySQL database creation

As ```MySQL``` root user, create the ```medline``` user and database:

```

CREATE USER 'medline'@'localhost' IDENTIFIED BY 'pubmed2015';
CREATE DATABASE medline;
GRANT ALL ON medline.* TO 'medline'@'localhost';

```

Then, as ```medline``` user run the ```createTables.sql``` script:

```
mysql --database medline -u medline -p < createTables.sql
```

### Populate the MySQL database

1. Populate the MeSH term and qualifier tables by running the following script on the mesh data:

```
python fillMeshTable.py mesh/d2015.bin pubmed2015
python fillMeshQualifTable.py mesh/q2015.bin pubmed2015
```

2. Populate the articles and records tables by running the following script on the (unzipped) Medline XML files:

```
python fillArticleTable.py medline/medline15n0778.xml
```

Of course you need to download the full collection of medline XML files, available at:

https://www.nlm.nih.gov/databases/download/pubmed_medline.html

and run the script on each XML file.

## Compute the popularity of MeSH terms over the years

The following script computes the number of articles containing given mesh terms:

```
python extractTimeCourses.py pubmed2015
```

If you want a denominator to normalize the number of articles published every year, run the following script:

```
python getNumOfPapersPerYear.py pubmed2015
```

#!/usr/bin/python

######################################################################
# getNumberOfPapersPerYear.py                                        #
# Author:  Dario Ghersi                                              #
# Version: 20151201                                                  #
# Goal:    extract the total number of papers per year               #
# Usage:   extraxctTimeCourses.py PASSWORD                           #
######################################################################

import pymysql
import sys

DATABASE = "medline"
USER = "medline"

years = range(1995, 2015)

## parse the arguments
if len(sys.argv) != 2:
  print "Usage:  getNumberOfPapersPerYear.py PASSWORD"
  sys.exit(1)
password = sys.argv[1]

## connect to the database
db = pymysql.connect(host="localhost", user=USER, passwd=password,
                     db=DATABASE)
cur = db.cursor()

## extract the total number of papers published in each year
for year in years:
  query = "SELECT COUNT(year) FROM articles WHERE year = " +\
    str(year) + ";"
  cur.execute(query)
  for row in cur:
    print year, row[0]


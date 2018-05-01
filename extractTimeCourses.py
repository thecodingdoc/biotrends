#!/usr/bin/python

######################################################################
# extractTimeCourses.py                                              #
# Author:  Dario Ghersi                                              #
# Version: 20151119                                                  #
# Goal:    extract the time courses for each mesh keyword            #
# Usage:   extraxctTimeCourses.py PASSWORD                           #
######################################################################

from collections import Counter
import pymysql
import sys

######################################################################
# CONSTANTS                                                          #
######################################################################

DATABASE = "medline"
USER = "medline"
MIN_NARTICLES = 100 # minimum number of articles to consider
                    # for each keyword
years = range(1995, 2015)

######################################################################
# FUNCTIONS                                                          #
######################################################################

def processYears(results):
  """
  """

  counts = Counter(results)
  yearDistr = []
  for year in years:
    if counts.has_key(year):
      yearDistr.append(str(counts[year]))
    else:
     yearDistr.append("0") 

  return " ".join(yearDistr)
  
######################################################################
  
def runQuery(cur, keyword):
  """
  """

  query = "SELECT articles.year FROM articles INNER JOIN records"
  query += " ON records.meshID = '" + keyword
  query += "' AND articles.pubmedID = records.pubmedID;"
  cur.execute(query)

  results = []
  for row in cur:
    results.append(row[0])

  return results

######################################################################
# MAIN PROGRAM                                                       #
######################################################################

## parse the arguments
if len(sys.argv) != 2:
  print "Usage:  extraxctTimeCourses.py PASSWORD"
  sys.exit(1)
password = sys.argv[1]

## connect to the database
db = pymysql.connect(host="localhost", user=USER, passwd=password,
                     db=DATABASE)
cur = db.cursor()

## get all keywords and definitions
query = "SELECT meshID, definition FROM mesh;"
cur.execute(query)
meshKW = []
definitions = []
for row in cur:
  meshKW.append(row[0])
  definitions.append(row[1])

## process each keyword
for i in range(len(meshKW)):
  keyword = meshKW[i]
  results = runQuery(cur, keyword)
  if results != None and len(results) >= MIN_NARTICLES:
    yearDistr = processYears(results)
    print keyword + "\t" + definitions[i] + "\t" + yearDistr
    
## clean up
cur.close()
db.close()

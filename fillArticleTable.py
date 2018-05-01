#!/usr/bin/python

######################################################################
# fillMeshArticleTable.py                                            #
# Author:  Dario Ghersi                                              #
# Version: 20151118                                                  #
# Goal:    fill in the ARTICLE table in the MySQL medline DB         #
# Usage:   fillArticleTable.py XML PASSWORD                          #
######################################################################

import pymysql
import sys

######################################################################
# CONSTANTS                                                          #
######################################################################

DATABASE = "medline"
USER = "medline"
MIN_YEAR = 1995

######################################################################
# FUNCTIONS                                                          #
######################################################################

def extractFields(record):
  """
  extract the pubmed ID, affiliation, year, and
  mesh terms from a record
  """

  pubmedID = ""
  #title = ""
  #abstract = ""
  affiliation = ""
  year = ""
  noMesh = False
  pubDate = False
  isAffiliation = False
  isMesh = False
  addAffiliation = True
  meshData = []
  record = record.split("\n")

  ## process the record
  for line in record:

    if line.find("<PMID ") != -1: # pubmedID
      pubmedID = line.split(">")[1].split("<")[0]
      
    #if line.find("<ArticleTitle>") != -1: # title
    #  title = line.replace("<ArticleTitle>", "")
    #  title = title.replace("</ArticleTitle>", "")[:-1]

    #if line.find("<AbstractText") != -1: # extract the abstract
    #  temp = line.split(">")[1]
    #  temp = temp.split("<")[0]
    #  abstract += temp

    if pubDate: # extract the year of publication
      year = line.split(">")[1][:4]
      pubDate = False
      
    if line.find("<PubDate") != -1:
      pubDate = True

    if isAffiliation and addAffiliation:
      affiliation = line.split(">")[1].split("<")[0]
      isAffiliation = False
      addAffiliation = False
      
    if line.find("<AffiliationInfo>") != -1:
      isAffiliation = True

    if isMesh:
      meshData.append(line[:-1])
      
    if line.find("<MeshHeadingList>") != -1:
      isMesh = True

    if line.find("</MeshHeadingList>") != -1:
      isMesh = False
      
  if affiliation == "" or year == "" or int(year) < MIN_YEAR or noMesh:
    return False
  else:
    meshInfo = getMeshInfo(meshData)
    
    return [pubmedID, affiliation, year, meshInfo]
    
#######################################################################

def getMeshInfo(meshData):
  """
  extract the mesh data
  """

  meshInfo = []
  currentTopic = ""
  isMajor = False
  toRecord = False
  meshID = "D000000"
  qualifID = "Q000000" # ID of the null qualifier

  for line in meshData:
    
    if line.find("<DescriptorName") != -1: # descriptor

      if line.find("MeshHeading") != -1: # skip
        continue
      
      if toRecord: # store the previous record with no qualifiers
        meshInfo.append([meshID, qualifID, isMajor])

      # get the new record
      meshID = line.split('UI="')[1].split('"')[0]
      qualifID = "Q000000"
      toRecord = True

      if line.find('MajorTopicYN="Y"') != -1: # is this a major topic?
        isMajor = True
      else:
        isMajor = False

      continue
      
    if line.find("<QualifierName") != -1: # qualifier
      qualifID = line.split('UI="')[1].split('"')[0]
      toRecord = False
      
      if line.find('MajorTopicYN="Y"') != -1: # is this a major topic?
        isMajor = True
      else:
        isMajor = False

      # store the qualified record
      meshInfo.append([meshID, qualifID, isMajor])

      continue

  # store the last record
  if toRecord:
    meshInfo.append([meshID, qualifID, isMajor])
  
  return meshInfo
  
#######################################################################
    
def getNextRecord(xmlFile):
  """
  extract a chunk of xml text corresponding to a record
  """

  record = ""
  newRec = False
  title = ""
  for line in xmlFile:

    if line.find("</MedlineCitation>") != -1: # end of record
      return record
    
    elif line.find("<MedlineCitation ") != -1: # new record
      newRec = True
      
    elif newRec:
      record += line    

  return record

######################################################################

def storeRecord(record, db, cur):
  """
  insert the record into the MySQL database
  """

  # insert the article record
  try:
    cur.execute("INSERT INTO articles VALUES (%s, %s, %s)",\
               (record[0], record[1], record[2]))
 
  except:
    pass
 
  # insert the mesh data
  for mesh in record[3]:
    try:
      cur.execute("INSERT INTO records VALUES (%s, %s, %s, %s)",\
                  (record[0], mesh[0], mesh[1], mesh[2]))
    except:
      pass
    
######################################################################
# MAIN PROGRAM                                                       #
######################################################################

## parse the arguments
if len(sys.argv) != 3:
  print "Usage: fillArticleTable.py XML PASSWORD"
  sys.exit(1)
xmlFileName, password = sys.argv[1:]

## open the xml file
xmlFile = open(xmlFileName, "r")

## connect to the database
db = pymysql.connect(host="localhost", user=USER, passwd=password,
                     db=DATABASE)
cur = db.cursor()
cur.execute("SET NAMES utf8;") # Unicode

## process the xml file
while True:
  record = getNextRecord(xmlFile)
  if len(record) == 0:
    break
  else:
    procRec = extractFields(record)

    if procRec:
      storeRecord(procRec, db, cur)

## commit the changes
db.commit()
    
## clean up
cur.close()
db.close()
xmlFile.close()

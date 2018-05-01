#!/usr/bin/python

######################################################################
# fillMeshTable.py                                                   #
# Author:  Dario Ghersi                                              #
# Version: 20150825                                                  #
# Goal:    fill in the MESH table in the MySQL medline DB            #
# Usage:   fillMeshTable.py MESH_TERMS PASSWORD                      #
######################################################################

import pymysql
import sys

######################################################################
# CONSTANTS                                                          #
######################################################################

DATABASE = "medline"
USER = "medline"

######################################################################
# MAIN PROGRAM                                                       #
######################################################################

## parse the arguments
if len(sys.argv) != 3:
  print "Usage: fillMeshTable.py MESH_TERMS PASSWORD"
  sys.exit(1)
meshTermsFileName, password = sys.argv[1:]

## open the mesh file
meshTermsFile = open(meshTermsFileName, "r")

## connect to the database
db = pymysql.connect(host="localhost", user=USER, passwd=password,
                     db=DATABASE)
cur = db.cursor()

## fill the mesh table
## insert the NULL keyword
command = 'INSERT INTO mesh VALUES ("D000000", "");'
cur.execute(command)
for line in meshTermsFile:
  if line[:4] == "MH =":
    definition = line[:-1].split(" = ")[1]

  if line[:4] == "UI =":
    meshID = line[:-1].split()[-1]

    # create the SQL command
    command = 'INSERT INTO mesh VALUES ("' + meshID + '", "' +\
      definition + '");'

    # execute the SQL command
    cur.execute(command)

## commit the changes
db.commit()
    
## clean up
cur.close()
db.close()
meshTermsFile.close()


#!/usr/bin/python

######################################################################
# fillMeshQualifTable.py                                             #
# Author:  Dario Ghersi                                              #
# Version: 20150825                                                  #
# Goal:    fill in the MESH_QUALIF table in the MySQL medline DB     #
# Usage:   fillMeshTable.py MESH_QUALIF PASSWORD                     #
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
  print "Usage: fillMeshTable.py MESH_QUALIF PASSWORD"
  sys.exit(1)
meshQualifFileName, password = sys.argv[1:]

## open the mesh file
meshQualifFile = open(meshQualifFileName, "r")

## connect to the database
db = pymysql.connect(host="localhost", user=USER, passwd=password,
                     db=DATABASE)
cur = db.cursor()

## fill the mesh table
## enter the empty qualifier
command = 'INSERT INTO meshQualif VALUES ("Q000000", "");'
cur.execute(command)

for line in meshQualifFile:
  if line[:4] == "SH =":
    definition = line[:-1].split(" = ")[1]

  if line[:4] == "UI =":
    meshID = line[:-1].split()[-1]

    # create the SQL command
    command = 'INSERT INTO meshQualif VALUES ("' + meshID + '", "' +\
      definition + '");'

    # execute the SQL command
    cur.execute(command)

## commit the changes
db.commit()
    
## clean up
cur.close()
db.close()
meshQualifFile.close()


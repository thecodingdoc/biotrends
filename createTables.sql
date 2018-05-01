CREATE TABLE articles (pubmedID VARCHAR(10), title TEXT, abstract TEXT,
affiliation TEXT, year YEAR(4),
PRIMARY KEY(pubmedID));
ALTER TABLE articles ADD INDEX(pubmedID), ADD INDEX(year);

CREATE TABLE mesh (meshID VARCHAR(7), definition VARCHAR(150),
PRIMARY KEY(meshID));

CREATE TABLE meshQualif (qualifID VARCHAR(7), definition VARCHAR(150),
PRIMARY KEY(qualifID));

CREATE TABLE records (pubmedID VARCHAR(10), meshID VARCHAR(7),
qualifID VARCHAR(7),isMajor BOOL,
PRIMARY KEY(pubmedID, meshID, qualifID));
ALTER TABLE records ADD INDEX(meshID), ADD INDEX(qualifID), ADD INDEX(isMajor);

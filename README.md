1. Problems Encountered in the Map

Boston : 

Being a historical city it's obvious to find roads which are not properly planned and I
think that's why we Bostonian are crazy when it comes to Driving. To add into, most of
the street in boston has zigzag property.

Leaving all those characteristics apart, Boston street map data was really great source to 
analyze as there are bunch of different street in the city.

After exploring the Boston OpenStreetMap data, I found three potential flows in the dataset.

1)

is a historical city. As far as I know when History word comes
in any discussion there would be a debate about the historical information.

# Data-Wrangle-OpenStreetMaps-Data
2. Data Overview

This section contains basic statistics about the dataset and the MongoDB queries used to gather them.

File sizes

boston_massachusetts.osm ......... 360 MB
boston_massachusetts.osm.json .... 391.2 MB

# Number of documents

db.boston.find().count()
1853071
# Number of nodes
> db.boston.find({"type":"node"}).count()
1605728
# Number of ways

> db.boston.find({"type":"way"}).count()
246265
# Number of unique users

> db.boston.distinct({"created.user"}).length
336

# Top 1 contributing user

> > db.boston.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}},{"$sort" : { "count" : -1}},{"$limit":1}])
{ "_id" : "crschmidt", "count" : 1058798 }
# Number of users appearing only once (having 1 post)
> db.boston.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}},Ê{"$group":{"_id":"$count", "num_users":{"$sum":1}}},Ê{"$sort":{"_id":1}}, {"$limit":1}])
{ "_id" : 1, "num_users" : 225 }
# Ò_idÓ represents postcount
from TwitterSearch import *
from geopy import geocoders

import arcpy
from arcpy import env
arcpy.env.overwriteOutput = True
env.workspace = "F:/UWTacoma/GIS_501_AU_2014/lab_7/"
path = "F:/UWTacoma/GIS_501_AU_2014/lab_7"
fc = "/twitter.shp"
spatialref = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]"

def geo(location):
        g = geocoders.GoogleV3()
        loc = g.geocode(location)
        return loc.latitude, loc.longitude   

#Create a Feature Class with defined Fields:
arcpy.management.CreateFeatureclass(path, fc, "POINT","","","",spatialref)
arcpy.management.AddField(fc, "lat", "FLOAT")
arcpy.management.AddField(fc, "lng", "FLOAT")
arcpy.management.AddField(fc, "tweet", "TEXT")

#Use Insert Cursor to populate the Feature Class table:
cur = arcpy.da.InsertCursor(fc, ["SHAPE@XY","lat","lng", "tweet"])

#Defining Search terms and Twitter API keys:
try:
        tso = TwitterSearchOrder()
        tso.set_keywords(['bus','trip'])
        tso.set_language('en')
        tso.set_include_entities(False)
        
        ts = TwitterSearch(
                consumer_key = 'A0rrcj60c4eta1nNUu4oJt5Sl',
                consumer_secret = 'kz3Anz3gPiZWWeKDqZ7mrezSrt7k1OFTiEVizDWzL4aYxl9x1f',
                access_token = '2865066196-0Ut3GUetKeRzWIrSZQs7W1BxEyfeIhM42IqTkzH',
                access_token_secret = '9g5QgTyOVeJp445VIHiAW2pVZLnXBgS6ZvxiyMlkjejg4',
                )

#Iterating through the tweets for ones with defined Places:
        for tweet in ts.search_tweets_iterable(tso):
                if tweet['place'] is not None:
                        print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text']))
                        try:
                                (lat, lng) = geo(tweet['place']['full_name'])
                                print 'And they said it from (' + str(lat) +', ' +str(lng)+')'
                        except ValueError:
                                print("Error: geocode failed on input %s with message %s"%(tweet, error_message))
                                continue 

#Defining the items contained in each row:
                        for row in tweet:
                                row = [(lng,lat),lat,lng,tweet['text']]
                        cur.insertRow(row)


except TwitterSearchException as e:
                print(e)

#Create a Feature Layer for analysis:
arcpy.management.MakeFeatureLayer('twitter.shp', 'twitter_lyr')

#Select by Location with a US cartographic boundary shapefile in WGS 1984 projection:
arcpy.management.SelectLayerByLocation('twitter_lyr', 'intersect', 'US_proj.shp')

#Check selection and create a new shapefile:
matchcount = int(arcpy.GetCount_management('twitter_lyr').getOutput(0)) 
if matchcount == 0:
    print('no features matched spatial and attribute criteria')
else:
    arcpy.CopyFeatures_management('twitter_lyr', 'UStweet')

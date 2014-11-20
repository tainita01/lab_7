from TwitterSearch import *
from geopy import geocoders

def geo(location):
	g = geocoders.GoogleV3()
	loc = g.geocode(location)
	return loc.latitude, loc.longitude
	
try:
	tso = TwitterSearchOrder()
	tso.set_keywords(['winter','storm'])
	tso.set_language('en')
	tso.set_include_entities(False)
	
	ts = TwitterSearch(
		consumer_key = 'A0rrcj60c4eta1nNUu4oJt5Sl',
		consumer_secret = 'kz3Anz3gPiZWWeKDqZ7mrezSrt7k1OFTiEVizDWzL4aYxl9x1f',
		access_token = '2865066196-0Ut3GUetKeRzWIrSZQs7W1BxEyfeIhM42IqTkzH',
		access_token_secret = '9g5QgTyOVeJp445VIHiAW2pVZLnXBgS6ZvxiyMlkjejg4',
		)
	
	for tweet in ts.search_tweets_iterable(tso):
		if tweet['place'] is not None:
			print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text']))
			(lat, lng) = geo(tweet['place']['full_name'])
			print 'And they said it from (' + str(lat) +', ' +str(lng)+')'

except TwitterSearchException as e:
		print(e)

except GeocoderQuotaExceeded as q:
		print(q)

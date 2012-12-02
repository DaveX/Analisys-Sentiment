import json as json

'''
coordenadas rectangulo chile (lon/lat)
-76.992188,-47.525114,-67.895508,-17.319875
Comando:
curl -d @locations_chile http://stream.twitter.com/1/statuses/filter.json -ujuan_twitero:<coloca pwd> > captured_tweets_chile.json 
'''
f = open('salida_curl.json','r')
ln = 1
for l in f:
	print "************ ",ln," *************"
	#print l
	try:
		l_data = json.loads(l)
		print l_data
	except ValueError:
		print "ERROR AL LEER LINEA ",ln
	ln = ln + 1

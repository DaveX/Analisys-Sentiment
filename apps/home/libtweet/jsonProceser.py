import json as json

'''
coordenadas rectangulo chile (lon/lat)
-76.992188,-47.525114,-67.895508,-17.319875
Comando:
curl -d @locations_chile http://stream.twitter.com/1/statuses/filter.json -ujuan_twitero:<coloca pwd> > captured_tweets_chile.json 
'''

file= '/home/davex/Escritorio/dataset/tweets/4.json'
out = file + ".txt"
log = file + ".log"

f = open(file,'r')
o = open(out,'w')
lg = open(log,'w')

#print type(f)
ln = 1
lgn=1
tw=1
for l in f:
	#print "************ ",ln," *************"
	#print l
	#proc = str(l)
	#print type(l)
	#print "HOLE"+ proc
	#print l
	try:
	    content = json.loads(str(l))
	    #print "BIEN!"	        	
	    if "text" in content:
		print "\nTWITTER: " + str(tw)
		print u"{0[user][name]}: {0[text]}".format(content)
		#o.write("<newtweet>\n"+ u"{0[user][name]}: {0[text]}".format(content)+"\n</newtweet>\n")
		o.write("<newtweet><id=\""+str(tw)+"\"/>\n\t<user=\""+ u"{0[user][name]}".format(content) +"\" />\n\t<text>"+ u"{0[text]}".format(content)+"</text>\n</newtweet>\n")
		tw += 1
	except ValueError:
		print "\nERROR AL LEER LINEA ",ln
		#lg.write(l)
		#lg.write("\n")
		#lgn += 1
		#print l
	
	ln = ln + 1

f.close()
o.close()
lg.close()

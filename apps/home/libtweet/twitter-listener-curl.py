from curl import curl
from getpass import getpass
from string import strip
import json as json
from utilitarios import print_titulo


print_titulo('Recoleccion de tweets')
file_out = '/home/davex/Escritorio/dataset/tweets/12Jul-4.json'/home/davex/Escritorio/Codigos Proyecto/twitter_python_listener

print "ARCHIVO A USAR: " + file_out
#calcula tweets (lineas) en el archivo actual
try:
	fout = open(file_out)
	acm = sum([1 for line in fout]) + 1
	print "Archivo contiene actualmente: " + str(acm) + " TWEETS"
	fout.close()
except:
	print "El archivo aun no se ha creado, se creara"
	acm = 1

m=raw_input("...continuar")

fout = open(file_out,'a')
             
'''
	try:
		l_data = json.loads(response)
		#print l_data
	except ValueError:
		print "ERROR AL LEER FLUJO "
'''

buffer = ""
ln = 0

def write_f(data):
	global ln
	global acm	
	#print "ESCUCHA : -------" + str(ln)
	#print data
	global buffer
	content = ""
	#print response.strip().replace('\\','')
	#fout.write(response.strip().replace('\\',''))
	
	buffer += data
	if data.endswith("\n") and buffer.strip():
		#print "encontre uno!" 
		#print buffer
		try:
			content = json.loads(buffer)
			#print type(content)
			#fout.write(str(content))
			fout.write(buffer)
			#fout.write(str(content)+"\r")
			print "TWITTER" + str(acm)
		#print content		
		#print "limpia buffer"	
			acm += 1	
			if "text" in content:
        			print u"{0[user][name]}: {0[text]}".format(content)
	#	print content
		except ValueError:
			print "ERROR AL BUFFER ",ln
	#content = json.loads(data.strip())
		
		buffer = ""
	 	

#	fout.write(content)
	#print content
	
	ln = ln + 1

#user = 'juan_twitero'
user = raw_input('Ingrese nombre de usuario:')
pwd = getpass(''.join(['Ingrese pwd asociado a cuenta "',user,'":']))
params = strip( open('locations_chile','r').read())
#params.close()
#params = strip( open('count','r').read())

'''
curl -d @locations_chile http://stream.twitter.com/1/statuses/filter.json -ujuan_twitero:<coloca pwd> > captured_tweets_chile.json 
'''


curl({ 
	'url'  : 'https://stream.twitter.com/1/statuses/filter.json',
	'post' : params,
	'write': write_f,
	'user_passwd' : ''.join([user,':',pwd])
})	
     
fout.close()

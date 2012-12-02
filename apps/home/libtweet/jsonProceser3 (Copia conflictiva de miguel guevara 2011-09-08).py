# -*- coding: utf-8 -*-
import json as json
import codecs
from utilitarios import print_titulo
import os

print_titulo('Procesar JSON de archivos Tweets')

#VARIABLES DE CONFIGURACIÓN GLOBAL
id=1
acum_error=1
dataset_dir="/home/mguevara/data"
data_out_dir="/home/mguevara/datasets/tweetscontinuossolotexto"

out = "salida"
log= "errores.log"
tweets_por_archivo= 172000
numero_archivo=1
acum_nuevo_archivo = 1

def procesa(file):
	global id
	global acum_error	
	global out
	global log	
	global tweets_por_archivo
	global acum_nuevo_archivo
	#se deben codificar a unicode utf-8 de lo contrario resultan errores con caracteres extraños
	f = codecs.open(file, encoding='utf-8', mode='r')
	
	
	#f = open(file,'r')
	#o = open(out,'w')

	#print type(f)
	ln = 1
	tw=1
	lgn=1
	for l in f:	
		try:	
		    content = json.loads(str(l))
		    #print "BIEN!"	        	
	 	    if "text" in content:
			    #print "\nTWITER: " + str(tw)
			    #print u"{0[user][name]}: {0[text]}".format(content)
			    
			    #print u"{0[]}".format(content)
			    #m=raw_input("cont")
			    #MIRA si debe crearotro archivo
			    if acum_nuevo_archivo == (tweets_por_archivo + 1):
				inicia_archivo()
				acum_nuevo_archivo = 1
			    #con id y con usuario y fecha	
			    #cadena = "<newtweet>"
			    #cadena+= "<id=\""+str(id)+"\"/>"
			    #cadena+= "\n\t<user=\"" + u"{0[user][name]}".format(content) +"\" />"
			    #cadena+= "\n\t<date>"+ u"{0[created_at]}".format(content)+"</date>"
			   
			    #Exportación para Hoja de Calculo
			    cadena = ""
			   #INFORMACION BASICA
			    #cadena+= u"{0[text]}".format(content) + "\n"
			    #cadena+= u"{0[user][name]}".format(content) + "\n"				    		   
			    #cadena+= u"{0[created_at]}".format(content) + "\n"
			    #cadena+= u"{0[text]}".format(content).lower() + "\n"

			   #RELACIONADO AL RETWEET
#			    cadena+= u"{0[retweet_count]}".format(content) + "\t"
#			    cadena+= u"{0[retweeted]}".format(content) + "\t"
			    #cadena+= u"{0[retweeted]}".format(content) + "\t"		
#			    cadena+= u"{0[in_reply_to_user_id_str]}".format(content) + "\n"			   
			   
				#HASHTAGS Y URLS
			    #cadena+= u"{0[entities][urls]}".format(content) + "\t"
			   # cadena+= u"{0[entities][urls][url]}".format(content) + "\t"
			   # cadena+= u"{0[entities][urls][indices]}".format(content) +"\t"
			    #cadena+= u"{0[entities][hashtags]}".format(content) +"\n"
			   
				#DE LOCALIZACION Y GEOGRAFICOS
			    #cadena+= u"{0[geo]}".format(content) +"\t"
			    #cadena+= u"{0[coordinates]}".format(content) +"\t"
			    cadena+= u"{0[place]}".format(content) +"\n"
			   # cadena+= u"{0[source]}".format(content) +"\n"

												
			    #cadena+= "\n\t<text>"+ u"{0[text]}".format(content)+"</text>"
			    #cadena+= "\n</newtweet>\n"
   			   #o.write("<newtweet><id=\""+str(id)+"\"/>\n\t<user=\""+ u"{0[user][name]}".format(content) +"\" />\n\t<text>"+ u"{0[text]}".format(content)+"</text>\n</newtweet>\n")
			    o.write(cadena)
  			   #Solo nombre y texto
			   # o.write("<newtweet>\n"+ u"{0[user][name]}: {0[text]}".format(content)+"\n</newtweet>\n")
		    	    tw += 1
			    id += 1
			    acum_nuevo_archivo +=1
		except ValueError:
			#print "\nERROR AL LEER LINEA ",ln
			lg.write("ID:" + str(id) + " " +str(l))
			#lg.write("\n")
			lgn += 1
			acum_error += 1
			#print l
	
		ln = ln + 1

	f.close()
	

	print "\n\tEstadisticas del Archivo procesado"
	print "\t\tTweets extraidos: " + str(tw-1)
	print "\t\tLineas no leídas: " + str(lgn-1)


#inicia un nuevo archivo
def inicia_archivo():
	global o
	global numero_archivo
	archivo = os.path.join(data_out_dir,out + str(numero_archivo)+".txt")	
	print "\t[...generando archivo: " + archivo + "]"	
	o = codecs.open(archivo, encoding='utf-8', mode='w')
	numero_archivo+=1
	o.write("<dataset>\n")
	

def cierra_archivo(archivo):
	global o
	o.write("</datset>")
	o.close()
	
#INICIA PRINCIPAL
def configura():
	global dataset_dir
	global out
	global log
	global tweets_por_archivo
	global o
	global lg

	print_titulo("Configuraciones iniciales")
	files = os.listdir(dataset_dir)	
	directorios = dict()	
	acum = 1
	for name in files:
	    path = os.path.join(dataset_dir, name)
	    if not(os.path.isfile(path)):
		directorios[acum] = name	
		print "\t" + str(acum) + ") " + name	
		acum+=1
	#print f_json

	m=raw_input("Indique directorio a procesar " + dataset_dir + " : ")
	dataset_dir = os.path.join(dataset_dir, directorios[int(m)])

	log1 = os.path.join(data_out_dir,log) #arcvhivo abierto para guardar errores	
	print "Archivo con tweets erróneos: " + log1
	#m=raw_input("...continuar")
	
	#abre log
	lg = codecs.open(log1, encoding='utf-8', mode='w')
	inicia_archivo() #inicia el primer archivo	
	
	return 	dataset_dir


def iniciar(cwd):
	print_titulo("Elija el archivo a procesar, ENTER para todos")
	files = os.listdir(cwd)
	files.sort()
	#print type(files2)
	#print files2
	acum = 0
	f_json = dict()

	for name in files:
	    if name[-5:] == ".json":	
		acum+=1
		f_json[acum] = name	
		print "\t" + str(acum) + ") " + name	
	#print f_json
	m=raw_input(": ")
	ac=1
	if m == "" or m =="0":
	    for file in f_json:
		aprocesar = cwd + "/" + f_json[int(file)]
		print_titulo("Procesando Archivo: " +str(ac)+ " " + aprocesar)
		procesa(aprocesar)
		ac+=1
	
	else:
	    aprocesar= cwd + "/" + f_json[int(m)]
	    print "Procesando: " + aprocesar
	    procesa(aprocesar)


	
cwd = configura()
iniciar(cwd)


print_titulo('Estadisticas FINALES')
print "\tTweets extraidos: " + str(id-1)
print "\tTweets erróneos: " + str(acum_error-1)  
print_titulo("FIN EJECUCION")

lg.close()

	
	
#file= '/home/mguevara/datasets/tweets/12Jul-3.json'


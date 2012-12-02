# -*- coding: utf-8 -*-
from curl import curl
from getpass import getpass
from string import strip
import codecs
import json as json
import os
from utilitarios import print_titulo

print_titulo('Obtencion de datos para grafo de usuarios')
dir_out="/home/mguevara/datasets/tweetscontinuossolotexto"
users_file="/home/mguevara/datasets/tweetscontinuossolotexto/Usuarios2.csv"

#log = os.path.join(dir_out, 'log')
numero_archivo = 1
max_usuarios = 2
f_out = str(numero_archivo)+ ".csv"
file_out = os.path.join(dir_out, f_out)
id_usuario=221441490

def crea_archivo():
    global file_out
    global fout
    global acm
    global numero_archivo
     
    numero_archivo+=1
    f_out = str(numero_archivo)+ ".csv"
    file_out = os.path.join(dir_out, f_out)
    print "ARCHIVO A USAR: " + file_out
    fout = open(file_out,'w')
    fout.write("Target,Source\n")
    acm = 1
    #actualiza log
    #lg = open(log, 'w')
    #lg.write(str(numero_archivo))
    #lg.close()
   
	

#busca si ya se ha iniciado la recoleccion y que archivo

m=raw_input("...continuar")
crea_archivo()


"""función que se llama desde el listener"""
def write_f(data):
	global ln
	global acm	
	#print "ESCUCHA : -------" + str(ln)
	#print data
	global id_usuario
	content = {}
	#print response.strip().replace('\\','')
	#fout.write(response.strip().replace('\\',''))
	print data	
	try:	
		content = json.loads(data)
		if "ids" in content:
		  cadena=content["ids"]
		  for id in cadena:
		     fout.write(str(id_usuario) + "," + str(id) + "\n")
		if "error" in content:
		  fout.write("error")

		acm += 1	
	except ValueError:
		print "excepcion" + data
	

f = codecs.open(users_file, encoding='utf-8', mode='r')

for l in f:
	print "vamos con " + l
	id_usuario = l.rstrip('\n')
	url ="https://api.twitter.com/1/followers/ids.json?cursor=-1&user_id=" + str(id_usuario)
	print url
	try:
		curl({ 
			'url'  : url,
			#'post' : params,
			'write': write_f,
			#'user_passwd' : ''.join([user,':',pwd])
		})	
	except ValueError:
		print "No tiene seguidores o algo fue mal\n"
		
fout.close()
f.close()

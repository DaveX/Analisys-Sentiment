# -*- coding: utf-8 -*-
from curl import curl
from getpass import getpass
from string import strip
import json as json
import os, re
from utilitarios import print_titulo

f=open('/home/davex/escritorio/dataset/tweets/textoparacorpus.txt')
	#funciona pero ineficiente
	# raw=''.join(l[:-1] for l in open('articulos/articulo'+str(i)+'.txt'))
#html=f.read()
#raw = nltk.clean_html(html)
html=f.read()

#*************************************************
#***********Colectar documentos*******************
#*************************************************
print_titulo('Crear Archivos del Corpus')
print 'Se dividira documentos con etiqueta NEWTWEET...'
articles = re.split(r'<newtweet>',html)
#articles = [nltk.clean_html(w) for w in articles]
#print articles[930:931]
tam=len(articles)
print 'Cantidad de articulos a procesar: ' + str(len(articles))
print 'Creando documentos ...'

#crear archivos de articulos
i=0
j=0
sintitu=[]
titulos=[]
t=''
voc=[]
#posts=[t,voc]
for art in articles:
	#output_file = open('/home/davex/escritorio/dataset/tweets/' + str(i) + '.txt', 'w')
	output_file = open('/home/davex/escritorio/dataset/tweets/'+ str(i), 'w')
	output_file.write(art)
	output_file.close()
	#f=open('articulos/articulo'+str(i)+'.txt')
	##f=open('articulos2/'+str(i))
	#funciona pero ineficiente
	# raw=''.join(l[:-1] for l in open('articulos/articulo'+str(i)+'.txt'))
	##html=f.read()
	##html=html.replace('\n','',j)
	##title=re.findall("<title>('*.+\n*.*\n*.*\n*.*)</title>",html)
	i=i+1
	

M=raw_input("...Continuar")
print 'Cantidad de titulos:' + str(len(titulos))

# -*- coding: utf-8 -*-
import nltk
from scipy import linalg,array,dot,mat,transpose
import numpy
from numpy import linalg
import math
from utilitarios import *
import os
import codecs

#CONFIGURACIONES-----------------------------
global nd
nd=2  #numero de decimales para la matriz de caracteristicas
IV=0
export_matrices=''
export_indices=''
export_vocabularios=''
dataset = 1  #elegir dataset
label=''
numero_features=''

print_titulo("PROCESA COLECCION DE TEXTO")
print("\nConfiguraciones iniciales\n")
op = raw_input("Elija la coleccion:\n\t1)Ejemplo Libro IR \n\t2)Articulos Cientificos \n\t3)Reuters  \n\t4)Tweets  ")
if op =='': op='1'

dataset=int(op)

if dataset == 2:
#articuloscientificos
	corpus_root='/home/davex/Escritorio/datosprcesadonjson/' #// AQUI VA EL ARCHIVO PUNTO TXT CON LOS TWEETS A CONTAR PALABRAS PARA FORMAR VOCABULARIO.
	export_indices='/home/davex/Escritorio/articulo/indices/'   #//crear carpeta una carpeta.
	export_matrices ='/home/davex/Escritorio/articulo/matrices/'   #// asumo que aqui tambien hay que crear carpeta.
	export_vocabularios ='/home/davex/Escritorio/articulo/vocabulario/'   #//crear carpeta con vocabulario.
	exp_archivos='.*'
	termino_ejemplo = 'actor' #'articulo857.txt'
	documento_ejemplo = '857'
	print_titulo("CREAR CORPUS")
	from nltk.corpus import PlaintextCorpusReader
		corpus = PlaintextCorpusReader(corpus_root, exp_archivos)   #// Conflicto en esta linea al parecer porblemas de recibir corpus_root y exp_archivos.


if dataset == 3:
	export_indices='/home/davex/Escritorio/articulo/indices'
	export_matrices ='/home/davex/Escritorio/articulo/matrices'
	export_vocabularios ='/home/davex/Escritorio/articulo/vocabulario'
	#exp_archivos='.*'
	termino_ejemplo = 'aguila' #'articulo857.txt'
	documento_ejemplo = 'training/844'
	print_titulo("CREAR CORPUS")
	from nltk.corpus import reuters
	corpus = reuters
	
#reuters27000
#corpus_root = '/home/mguevara/datasets'
#exp_archivos='reuters/.*'
#termino_ejemplo = 'machine'
#documento_ejemplo = 'reuters/reut2-000.sgm'
if dataset == 1:
#articuloscientificos
	corpus_root='/home/davex/Escritorio/dataset/book/'                            ###################### AUN QUEDA POR MODIFICAR ESTO#################
	export_indices='/home/davex/Escritorio/datasetinfo/indices/book/'
	export_matrices = '/home/davex/Escritorio/dataset/info/matrices/book/'
	export_vocabularios = '/home/davex/Escritorio/dataset/vocabularios/book/'
	exp_archivos='.*'
	termino_ejemplo = 'ship' #'articulo857.txt'
	documento_ejemplo = 'd2'
	print_titulo("CREAR CORPUS")
	from nltk.corpus import PlaintextCorpusReader
	corpus = PlaintextCorpusReader(corpus_root, exp_archivos)

if dataset == 4:
#tweets
	corpus_root='/home/davex/datasets/tweetsarchivos/'
	export_indices='/home/davex/datasets/info/indices/tweetscontinuos/'
	export_matrices = '/home/davex/datasets/info/matrices/tweetscontinuos/'
	export_vocabularios = '/home/davex/datasets/info/vocabularios/tweetscontinuos/'
	exp_archivos='.*'
	termino_ejemplo = 'presentar' #'articulo857.txt'
	documento_ejemplo = '10'
	print_titulo("CREAR CORPUS")
	from nltk.corpus import PlaintextCorpusReader
	corpus = PlaintextCorpusReader(corpus_root, exp_archivos)

if len(corpus.words()) < 100: print corpus.fileids()
#print corpus.fileids()
print "\n\t\t\t\t...Corpus creado"

#Imprime frecuencia de vocabulario completo
fdist = nltk.FreqDist([w for w in corpus.words()])
arch=export_vocabularios + 'vocTotalFreq.txt'
fre_voc = open( arch , mode = 'w')
#print fdist.type()
for term in fdist:
	fre_voc.write(str(term) + "\t" + str(fdist[term]) + "\n")
print "Creado archivo con frecuencias!!!"


#print fdist

a_stopwords = 0
a_porter = 0
a_lema = 0
a_alpha = 1
a_lower = 0
verbose = 0   #para mostrar mensajes en la funcion MiraVocab

#corpus_root = '/home/mguevara/datasets'
#corpus = PlaintextCorpusReader(corpus_root, 'reuters/.*')
#print inverted_index['SELZ']
#termino_ejemplo = 'machine'



#corpus_root = '/home/mguevara/Dropbox/DOCTORADO/TECNOLOGIA BUSQUEDA/Tarea1/SolucionconNLTK/'
#corpus_root = '/home/mguevara/datasets'
#corpus = PlaintextCorpusReader(corpus_root, 'reuters/.*')
#print inverted_index['SELZ']
#termino_ejemplo = 'machine'

#Esta funcion crea un archivo de texto con el vocabulario recibido
def miravocab(vocab, titulo):
	global IV
   	print 'Tamano vocabulario'+ str(IV)+' generado: '+ str(len(vocab))
	#M=raw_input("...Continuar")

	#print 'Muestra primeros 20 terminos:' 
	#print(vocab[:20])

	#print 'Muestra ultimos 20170 terminos:' 
	#print(vocab[-20:])

	#output_file = open('Vocabulario' + titulo + '.txt', 'w')
    	output_file = open( titulo + '.txt', mode='w')
	for word in sorted(vocab):
   		output_file.write(word + "\n")
	#print '[Se ha generado el archivo: ' + titulo + '.txt]\n'
	print '[Se ha generado el archivo: ' + titulo + '.txt]\n'
	IV+=1

def procesa_vocabulario(text, c_stopwords, c_porter, c_lematizacion, c_alpha, c_lower, v):
	#print 'Creando vocabulario...'
    global export_vocabularios

    if c_lower:
    	words = [w.lower() for w in text]
    else:
	words = [w for w in text]
    vocab = sorted(set(words))
    #type(vocab)
    #miravocab(vocab, 'Tokens')
    
    if c_stopwords:
	stopwords = nltk.corpus.stopwords.words('spanish')
	#print 'Vocabulario Elimina STOPWORDS'
	words = [w for w in words if w.lower() not in stopwords]
	vocab = sorted(set(words))
	type(vocab)
	if v: miravocab(vocab, export_vocabularios + 'Sin Stopwords')

    if c_alpha:
	#print 'Vocabulario Solo Terminos de letras (Alpha. Sin numeros)'
	words = [w for w in words if w.isalpha()]
	vocab = sorted(set(words))

	if v: miravocab(vocab, export_vocabularios + 'Solo Alpha')

    if c_porter:
	porter = nltk.PorterStemmer()
	#print 'Vocario aplicado Porter'
	words = [porter.stem(t) for t in words]
	vocab = sorted(set(words))
	if v: miravocab(vocab, export_vocabularios + 'Con Porter')

    if c_lematizacion:
	wnl = nltk.WordNetLemmatizer()
	#print 'Vocabulario + Lematizacion'
	words=[wnl.lemmatize(t) for t in words]
	vocab = sorted(set(words))
	if v: miravocab(vocab, export_vocabularios + 'Con Lematizacion')

#Imprime frecuencia de vocabulario Procesado
    fdist = nltk.FreqDist([w for w in words])
    arch=export_vocabularios + 'vocProcesadoFreq.txt'
    fre_voc = open( arch,  mode = 'w')
	#print fdist.type()
    for term in fdist:
		fre_voc.write(str(term) + "\t" + str(fdist[term]) + "\n")
    print "Creado archivo con frecuencias2!!!"

    return vocab



#crea indice invertido, recibe un corpus y un vocabulario de terminos
def make_inverted_index(corpus, vocab):
    global exporta_indices
    inverted_index = {}
    for filename in corpus.fileids():
	#obtiene el vocabulario del documento segun configuraciones
      vocab = procesa_vocabulario(corpus.words(filename),a_stopwords, a_porter, a_lema, a_alpha, a_lower,0)
      for term in vocab:
	#for term in corpus.words(filename): consideramos solo los terminos en el vocabulario
	   # if term.isalpha():   
	   # if term in vocab:
		if term in inverted_index:
		   inverted_index[term].add(filename)
		else:
		   inverted_index[term] = set((filename,))
    guarda_indice(inverted_index, export_indices + 'Indice Invertido')  #se lleva a un archivo
    return inverted_index

#crea indice invertido, recibe un corpus y un vocabulario de terminos
def make_matrix(corpus, inverted_index):
    global numero_features
    global label
    nd = 2
    #obtiene features y frecuencia de terminos en todo el corpus
    words= procesa_words(corpus.words(),a_stopwords, a_porter, a_lema, a_alpha, a_lower)
    vm=5
    vm=raw_input("Elija el tipo de valor para los datos de la matriz \n\t1)Binario \n\t2)Tf \n\t3)TfNormalizado(max) \n\t4)TfSuavizado (log) \n\t5)TfIdf\n\t\t:")
    if vm == '': vm='1'

    if vm == str(1): #binario
      label = 'Bin'
    if vm == str(2):  #tf
      label = 'Tf'
    if vm == str(3): #tf normalizado
      label = 'TfNorm'
    if vm == str(4): #tf suavizado con log
      label = 'TfSuavLog10'
    if vm == str(5): #tf idf
      label = 'Tf.idf'
      ni = {}  #para la cantidad de documentos en los que aparece term
    
    M = len(inverted_index)  #numero de terminos colweccion
    N = len(corpus.fileids()) #numero de documentos
 	   
    #Elegir los features o terminos a usar para la matriz
    n='-1'
    while not(int(n)>=0 and int(n) <=5):
	    n=raw_input("\nLimitar terminos (max " + str(M) + ") a la siguiente cantidad [0 para todos]: ")
	    if n == '': n = '0'

    numero_features = n	
    if int(n) > 0:    
	frecuencia_termino = nltk.FreqDist(w for w in words) #frec del termino en todo el corpus
        word_features = frecuencia_termino.keys()[:int(n)]
        if int(n)<100: print word_features
    else:
	word_features= inverted_index

    feature_matrix = {}
    for filename in corpus.fileids():
	#obtiene los terminos del documento segun configuraciones CON repeticiones
	words = procesa_words(corpus.words(filename),a_stopwords, a_porter, a_lema, a_alpha, a_lower)
	#obtiene frecuencia de terminos en el vocabulario
	tfi=nltk.FreqDist(w for w in words)
	#print "mas frequente" 
	#print tf[tf.max()]

	#vocab = set(words)

        for term in word_features:
	#for term in corpus.words(filename): consideramos solo los terminos en el vocabulario
	   # if term.isalpha():   
	   # if term in vocab:
		if term in tfi:
		   if vm == str(1): #binario
		      val = 1
		   if vm == str(2):  #tf
		      val = tfi[term]
		   if vm == str(3): #tf normalizado
		      val = round(float(float(tfi[term])/float(tfi[tfi.max()])),nd)
		   if vm == str(4): #tf suavizado con log
		      val = round(1.0 + float(math.log10(float(tfi[term]))),nd)
		   if vm == str(5): #tf idf
		      tf = 1.0 + float(math.log10(float(tfi[term])))
		      ni[term] = len(inverted_index[term]) #numero de documentos en que aparece term
		      idf = math.log10(float(N)/float(ni[term])) 	
		      val = round(tf * idf,nd)
		      #val = "%.2f" %val    #pretty print
		      
		else:
		   val = 0
		
		if term in feature_matrix:
                   feature_matrix[term].append(val)
	        else:		
		   feature_matrix[term]= [val]
		

    guarda_indice(feature_matrix, export_matrices + 'Matriz-Caracteristicas-'+label+'-'+n)  #se lleva a un archivo
    #print feature_matrix
    print "\nMatriz de caracteristicas creada\n"
    return feature_matrix


def document_features(document):
    document_words = set(document)

def invierte_diccionario(d):
    inv = {}
    for key in d:
        conjunto = d[key]
	#print val	
	for val in conjunto:	
	    if val not in inv:
                inv[val] = [key]
	 #  inv[val] = set((key,))
	    else:
	        inv[val].append(key)
    guarda_indice(inv, export_indices + 'Indice')
    return inv

def transform_dic_mat(matrix):
    matriz = []
    for term in matrix:
    	matriz.append(matrix[term])
    return matriz

def imprime_caracteristicas_matriz(matriz):
    print matriz.shape()


def encuentra_svd(matriz):
    pause=raw_input("\nSe iniciara la obtencion de SVD, este proceso puede demorar ....continuar.")
    u,sigma,vt = linalg.svd(matriz,full_matrices=False)
    if len(sigma) < 10:	
	print "resultados svd"
	print "\nU: SVD Matriz de Terminos"
	print u
	#print type(u)
	print "\nSIGMA: Valores Singulares"
	print sigma
	print "\nVt: SVD Matriz de Documentos"
	print vt
    guarda_matriz_u(u,export_matrices + "U-MatrizTerminos-" + label+"-"+numero_features,feature_matrix)
    guarda_matriz_sigma(sigma,export_matrices + "Sigma-ValoresSingulares-"+ label+"-"+numero_features)
    guarda_matriz_vt(vt,export_matrices + "Vt-MatrizDocumentos-"+ label+"-"+numero_features, indice)
    	    
    return u, sigma, vt

def reduce_dimension(u,sigma,vt, dimensions):
	#print "--> Reducing Matrix ("+str(len(sigma))+"iterations)"
	#Dimension reduction, build SIGMA'
	ssigma = []
	for ind in xrange(len(sigma)):#, len(sigma)):
		#print index
		if ind < dimensions:
			ssigma.append(sigma[ind])
		else:
			sigma[ind] = 0
	#uEliminate the first dimension
	#sigma[0] = 0
	#print sigma
	#print linalg.diagsvd(sigma,len(self.matrix), len(vt))
	un = []
 	for i in u:
		un.append([j for j in i[:dimensions]])
	un = array(un)
	
	vtn= []

	for i in range(dimensions):
	   vtn.append(vt[i])

	vtn = array(vtn)
	
	

	''' DEBUG
	unt = transpose(un)
	ident = dot(unt,un)
	print ident
	'''
	#Reconstruct MATRIX'
	#reconstructedMatrix = dot(un,linalg.diagsvd(ssigma,len(ssigma),dimensions))
	#reconstructedMatrix = dot(un,scipy.linalg.diagsvd(ssigma,len(ssigma),dimensions))
	print "Sigma reducida"	
	print numpy.diagflat(ssigma)	
	print "U reducido"
	print un
	rec = numpy.dot(un,numpy.diagflat(ssigma))
	print "Vt reducido"
	print vtn
	print "fin vtn"	
	#print "primera reconstruccion"	
	#reconstructedMatrix= dot(dot(u,linalg.diagsvd(sigma,len(self.matrix),len(vt))),vt)
	#print rec
	reconstructedMatrix=numpy.dot(rec,vtn)
	#print "Matriz reducida"
	#print reconstructedMatrix
	#Save transform
	return reconstructedMatrix


text = corpus.words()    
flag='1'
while flag=='1':
	print_titulo("ANALISIS DEL VOCABULARIO")
	#text = [term for term in inverted_index]
	print "Indique No(Enter) o Si(1) para cada opcion\n"
	a_stopwords = raw_input("\tEliminar Stopwords: ")
	a_porter = raw_input("\tAplica Porter: ")
	a_lema = raw_input("\tAplica Lematizacion: ")
	a_alpha = raw_input("\tSolo Letras: ")
	a_lower = raw_input("\tTodo a minusculas: ")
	print "\n"

	vocab = procesa_vocabulario(text,a_stopwords, a_porter, a_lema, a_alpha, a_lower, True)
	print "\nCANTIDAD DE TERMINOS DEL VOCABULARIO PARA LA COLECCION: " + str(len(vocab))
	flag=''
	flag=raw_input("\n\t\t\t\t....ENTER Para continuar, 1 Para Repetir: ")
#print vocabif len(corpus.words()) < 100: print corpus.fileids()
	#print "\n...Corpus creado"

print_titulo("CREAR INDICE INVERTIDO")
inverted_index = make_inverted_index(corpus, vocab)
print "TERMINO EJEMPLO: " + termino_ejemplo
print inverted_index[termino_ejemplo]
print "\nCONFIRMA CANTIDAD DE TERMINOS: " + str(len(inverted_index))
#pause=raw_input("\t\t\t\t....continuar")

print_titulo("CREAR INDICE DOCUMENTOS")
indice = invierte_diccionario(inverted_index)
print "DOCUMENTO EJEMPLO: " + documento_ejemplo
print indice[documento_ejemplo]

print "\nCONFIRMA CANTIDAD DE DOCUMENTOS: "+ str(len(indice))
#pause=raw_input("\t\t\t\t....continuar")

#print inverted_indeX(['articles.txt'])

print_titulo("COMPONE MATRIZ")
#crea_matriz(inverted_index)
#obtiene todas las palabras del corpus sin perder repeticiones pero procesadas
feature_matrix = make_matrix(corpus, inverted_index)
matriz = transform_dic_mat(feature_matrix) #transforma a numpyarray

print_titulo("ENCONTRAR SVD")
#guarda_matriz(vt,"Vt-MatrizDocumentos")
u,sigma,vt = encuentra_svd(matriz)

print_titulo("REDUCIR MATRIZ")
#guarda_matriz(vt,"Vt-MatrizDocumentos")
rows= len(sigma)
dimensiones = raw_input("Ingrese dimensiones (max "+str(rows)+") :")
matriz_reducida=reduce_dimension(u,sigma,vt,int(dimensiones))
#print matriz_reducida
print_titulo("Fin")






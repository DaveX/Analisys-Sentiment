# -*- coding: utf-8 -*-
from curl import curl
from getpass import getpass
from string import strip
import json as json
import os
from utilitarios import print_titulo

print_titulo('Recolección de tweets')
dir_out = '/home/davex/Descargas'
log = os.path.join(dir_out, 'log')
numero_archivo = 1
max_tweets = 10000
f_out = str(numero_archivo)+ ".json"
file_out = os.path.join(dir_out, f_out)

def crea_archivo():
    global file_out
    global fout
    global acm
    global numero_archivo

    numero_archivo+=1
    f_out = str(numero_archivo)+ ".json"
    file_out = os.path.join(dir_out, f_out)
    print "ARCHIVO A USAR: " + file_out
    fout = open(file_out,'a')
    acm = 1
    #actualiza log
    lg = open(log, 'w')
    lg.write(str(numero_archivo))
    lg.close()

def calcula_tweets():
    global acm
    global fout
    #calcula tweets (lineas) en el archivo actual
    try:
        fout = open(file_out)
        acm = sum([1 for line in fout]) + 1
        print "Archivo " + file_out + " contiene actualmente: " + str(acm-1) + " TWEETS"
        fout.close()
        fout = open(file_out,'a')
    except:
        print "Error abriendo el archivo"


#busca si ya se ha iniciado la recoleccion y que archivo
try:
    lg = open(log, 'r')
    numero_archivo = int(lg.read())
    f_out = str(numero_archivo)+ ".json"
    file_out = os.path.join(dir_out, f_out)
    calcula_tweets()
    fout = open(file_out,'a')
    lg.close()
except:
    print "No se ha iniciado la recolección en esta carpeta:" + dir_out + "\n\t\t\tse iniciará"
    print log
    m=raw_input("...continuar")
    crea_archivo()

#inicia recoleccion
buffer = ""   #va guardando las cadenas hasta tener un tweet completo
ln = 0

def sentiment_cb(data):
    print data

"""función que se llama desde el listener"""
def write_f(data):
    global ln
    global acm
    global buffer
    content = ""

    buffer += data
    if data.endswith("\n") and buffer.strip():
        try:
            content = json.loads(buffer)
            if acm > max_tweets:
                fout.close()
                crea_archivo()

            fout.write(buffer)
            acm += 1
            if "text" in content:
                    #print "\t" + u"{0[user][name]}: {0[text]}".format(content)
                    t = "{0[text]}".format(content)
                    params = "{'data': [{'text': '%s'}]}" %t
                    curl({
                        'url'  : 'http://www.sentiment140.com/api/bulkClassifyJson?appid=david.vargas@solem.cl',
                        'post' : params,
                        'write': sentiment_cb,
                    })
        except ValueError:
            print "ERROR AL BUFFER ",ln

        buffer = ""
    ln = ln + 1


if __name__ == "__main__":
    #con lectura de parametros'
    #user = raw_input('Ingrese nombre de usuario:')
    #pwd = getpass(''.join(['Ingrese pwd asociado a cuenta "',user,'":']))

    user = "davexdvx"
    pwd = "therealkey5"

    print_titulo("Inicia recoleccion con usuario" + user)

    #Ubicacion geografica
    #params = strip( open('locations_chile','r').read())
    params = strip( open('track','r').read())
    curl({
        'url'  : 'https://stream.twitter.com/1/statuses/filter.json',
        'post' : params,
        'write': write_f,
        'user_passwd' : ''.join([user,':',pwd])
    })

    fout.close()

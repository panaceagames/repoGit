# -*- coding: utf-8 -*-

import pymysql as MySQLdb

DB_HOST = '200.107.200.107'
DB_USER = 'asterisk'
DB_PASS = 'Pule1210'
DB_NAME = 'asterisk'

Alcdr = [ DB_HOST, DB_USER, DB_PASS, DB_NAME ]

def run_query(query=''):
    conn = MySQLdb.connect(*Alcdr)
    cursor = conn.cursor()
    cursor.execute(query)

    if query.upper().startswith('SELECT'):
        data = cursor.fetchall()
    else:
        data = "No valido"

    cursor.close()
    conn.close()
    return data


def dat():  #resive el diccionario del formulario de busqueda
    query = "SELECT * FROM asterisk.cdr WHERE dcontext='empresaClinicaBera' "

    #Hace la busqueda en la base
    cont = run_query(query)
    return cont

c = dat()

print (c)

print ("hola")
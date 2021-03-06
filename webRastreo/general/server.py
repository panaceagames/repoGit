import socketserver
import threading
import time
import json
import psycopg2
from passlib.hash import django_pbkdf2_sha256
import datetime

#Los datos llegan en json, solo hay que transformarlos para cambiara al diccionario original
class MiTcpHandler(socketserver.BaseRequestHandler):

    def MarcaTiempo(self, j): #convierte el string que mando la app a tipo datetime python para BD
        k = datetime.datetime.strptime(j, "%Y-%m-%d %H:%M:%S.%f")
        return k

    # Simple routine to run a query on a database and print the results:
    def doQuery(self,conn,final):
        try:
            coordinates = "POINT(%s %s)" % (final["lat"], final["lon"])
            #MarcaDeTiempo = MarcaTiempo(final["fechas2"])
        except:
            print("salto")
        cur = conn.cursor()
        print("dentro2")
        horaActual= datetime.datetime.now()
        #CHEQUEAR PORQUE ME PIDIO EN LOS CAMPOS NUEVOS USAR "" LO ARREGLE CON LA \ PERO NO ESTA BIEN REHACER LA BASE DE DATOS DESPUES QUE TODO FUNCIONE A VER SI SE PUEDE PONER NORMAL
        cur.execute("INSERT INTO general_location(name, point, bearing, altitud, speed, accuracy, email, fecha2, \"FinRecorrido\", \"InicioRecorrido\", imei, \"horarioIngreso\") VALUES (%s, ST_GeomFromText(%s,4326),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (final["numero"], coordinates, final["bearing"], final["altitude"], final["speed"], final["accuracy"], final["email"], final["fechas"], final["FinRecorrido"], final["InicioRecorrido"], final["imei"], horaActual))
        conn.commit()
        print("guardo")

    def handle(self):
        data="salir"
        hostname_postgre = 'localhost'
        username_postgre = 'testgis_user'
        password_postgre = '1234'
        database_postgre = 'testgis_db3'

        try: #corta el hilo si no se puede conectar a la base de datos
            myConnection = psycopg2.connect(host=hostname_postgre, user=username_postgre, password=password_postgre, dbname=database_postgre)
            cur = myConnection.cursor()
            login2 = self.request.recv(10024) #recibe la primera informacion solo user y password
            finallogin = json.loads(login2.decode("utf-8", errors="strict"))
            print (finallogin)
            print("Reportando al sistema")
            print(self.request)
            email= finallogin["email"]
            q = "SELECT * FROM auth_user WHERE email = '%s' " % email
            print("user")
            print(q)
            cur.execute(q)
            rows = cur.fetchall() #pasa los datos a la varible
            print(rows)
            self.validacion = {}
            try: #si el usuario no existe corta el hilos ya que rows esta vacio y va a tirar error en la asignacion
                #buscamos los datos del perfir dle usuario para saber si es una cuenta individual y se puede rastrear
                print("user2")
                UA = "SELECT * FROM clientes_userprofile WHERE user_id = '%s' " % rows[0][0]
                cur.execute(UA)
                UsuarioActual = cur.fetchall()
                if (UsuarioActual[0][11] != "Individual"): #hace que salta el try al no ser la cuenta tipo individual
                    print("dentrouser")
                    kjc = rows[32]
                hash1 = rows[0][1]
                print("user5")
                if len(finallogin) == 2: #chequea si solo hay dos elementos es porque esta logueando si hay mas es poruqe ya se logueo y esta mando info pasando directo al bucle
                    clave = finallogin["ppp"]
                    bool1 = django_pbkdf2_sha256.verify(clave, hash1)  #chequea si el password recibido conincide con el hash de la BD
                    if bool1:
                        self.validacion["si"] = "1"
                        self.informacionValida = json.dumps(self.validacion)
                        self.request.sendall(self.informacionValida.encode('utf-8'))  #si la se autentifica devuelve 1 sino manda 0
                        data = "corriendo"
                        datalogin = self.request.recv(10024) #esto guarda el segundo envio de la app con la marca de inicio o de fin
                        flogin = json.loads(datalogin.decode("utf-8", errors="strict"))
                        print (flogin)
                        print("luegoLogueo")
                        self.doQuery(myConnection,flogin)
                    else:
                        print ("Clave incorrecta")
                else:
                    data = "corriendo"
            except:
                print ("Usuario no existe Error")

                self.request.send("0") #le mando cero de falso
                data = "salir"
        except:
            print ("unable to connect to the database o anterior")
            data = "salir"
        if len(finallogin) != 2:
            while data != "salir":
                try:
                    final = finallogin
                    if final["email"] != email:
                        print ("el cliente esta mandando otro usuario diferente al cual se autentico se corta hilo")
                        data = "salir"
                    else:
                        try:
                            self.doQuery(myConnection,final)
                        except:
                            print ("error guardar base de datos")
                    time.sleep(0.5)
                    data2 = self.request.recv(10024)
                    finallogin = json.loads(data2.decode("utf-8", errors="strict"))
                    print (finallogin)
                except:
                    print ("cliente desconectadoo hubo error general")
                    data="salir"
        myConnection.close()

class ThreadServer(socketserver.ThreadingMixIn, socketserver.ForkingTCPServer):
    pass

def main():
    host = ""
    port= 33423
    server = ThreadServer((host,port), MiTcpHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    print("server corriendo")


main()





from django.shortcuts import render
from polyline.codec import PolylineCodec
from .models import Location
from .forms import Busqueda
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import json
from clientes.models import userProfile
import simplekml
from django.contrib.gis.geos import Point
import datetime
from geopy.geocoders import Nominatim
from django.contrib.auth.models import User
# Create your views here.

#MIRAR DISTINCT EN LOS FILTROS DE BUSQUEDA PARA PODER FILTRAR RESULTADOS CERCANOS EN EL ARMADO DE RUTA

def search(request):
    mensaje = "."
    distanciaTotal = "."
    if request.user.is_authenticated():
        if (request.method == 'POST'):
            form = Busqueda(request.POST)
            lista = request.POST.getlist("checkbox") #recupero los datos marcados en los box
            if (len(lista) == 1):
                if form.is_valid():
                    datosss = form.cleaned_data  #me crea el diccionario de los datos del formulario
                    usuarioTrasar = lista[0]
                    datosListos = manipularDatosBusqueda(datosss, usuarioTrasar)
                    datosListos1, distanciaTotal, listaPopupInicio = CrearListaPoint(datosListos)
                    if (datosListos1 != "Usuario no existe"): #chequeamos que el usuario existio en la base antes del polilyne
                        datosListos2 = []
                        for x in range(len(datosListos1)):
                            datosListos2.append(CrearPolyline(datosListos1[x]))
                        m = ""
                        for b in range(len(datosListos2)):
                            if b == (len(datosListos2)-1): #esto se puso para mandar un string que se puede manipular con js
                                m = m + datosListos2[b]
                            else:
                                if datosListos2[b] != "":
                                    m = m + datosListos2[b] + ","
                        datosListos2 = m
                    else: #enviamos en blanco si el user no existe entonces solo muestra el mapa y no error
                        datosListos2 = ""
                    user = request.user
                    lista = CuentaAsociadas(user)
                    datosIniciales = CrearPointSeguimientoSearch(usuarioTrasar) #da los datos para el zoom inicial
                    try: #para que no de error si el usuario en nuevo y no tiene recorridos
                        y = datosIniciales[0][0]
                        x = datosIniciales[0][1]
                    except:
                        x = ""
                        y = ""
                    if datosss['Distancia'] == False:
                        distanciaTotal = "."
                    datosUser = getDatosUserSearch(usuarioTrasar)
                    ctx = {'form': form, "lista": lista, "datosUser": datosUser, "listaPopupInicio": listaPopupInicio, "long": x, "lat": y, "usuarioMostrado": usuarioTrasar, "mensaje": mensaje,  "dato": datosListos2, "distanciaTotal": distanciaTotal}
                    return render(request,'search.html', ctx)
                else:
                    user = request.user
                    lista = CuentaAsociadas(user)
                    ctx = {'form': form, "lista": lista, "mensaje": mensaje,  "distanciaTotal": distanciaTotal}
                    return render(request, 'search.html', ctx)
            else:
                mensaje = "No a marcado ninguna cuenta. Por favor marque una"
                user = request.user
                lista = CuentaAsociadas(user)
                ctx = {'form': form, "lista": lista, "mensaje": mensaje,  "distanciaTotal": distanciaTotal}
                return render(request, 'search.html', ctx)
        else:
            form = Busqueda()
            form.fields["id_diaFin"] = '04'
            user = request.user
            lista = CuentaAsociadas(user)
            ctx = {'form': form, "lista": lista, "mensaje": mensaje, "distanciaTotal": distanciaTotal }
            return render(request, 'search.html', ctx)
    else:
        return HttpResponseRedirect('/')

def manipularDatosBusqueda(DicFormulario, usuarioTrasar):
    diaInicio = DicFormulario['diaInicio']
    mesInicio = DicFormulario['mesInicio']
    anoInicio = DicFormulario['anoInicio']
    diaFin = DicFormulario['diaFin']
    mesFin = DicFormulario['mesFin']
    anoFin = DicFormulario['anoFin']
    horaInicio = DicFormulario['horaInicio']
    minutoInicio = DicFormulario['minutoInicio']
    horaFin = DicFormulario['horaFin']
    minutoFin = DicFormulario['minutoFin']
    Cuenta = usuarioTrasar
    Distancia = DicFormulario['Distancia']
    inicial = anoInicio + "-" + mesInicio + "-" + diaInicio + " " + horaInicio + ":" + minutoInicio + ":00.0"
    finales = anoFin + "-" + mesFin + "-" + diaFin + " " + horaFin + ":" + minutoFin + ":00.0"
    datosss = { "Cuenta": Cuenta, "Distancia": Distancia, "inicial": inicial, "finales": finales}
    return datosss

def CrearListaPoint(datosListos): #trae los puntos para el polyline y suma la distancia recorrida
    kml1 = simplekml.Kml()
    hh = [] # para las cordenadas de KML reveer si se puede cambiar para menos memoria
    distance22 = 0 #control de cuenta kilometros
    distanciatotal = 0
    lista = [] #lista a devolver con los recorridos
    listaPopupInicio = []
    try:
        traso = Location.objects.filter(email=datosListos["Cuenta"])
        traso1 = traso.filter(fecha2__gte=datosListos["inicial"])
        traso2 = traso1.filter(fecha2__lte=datosListos["finales"])
        corteInicio = traso2.filter(InicioRecorrido="SI")
        corteFin = traso2.filter(FinRecorrido="SI")
        if (len(corteInicio) == len(corteFin)):  #Caso perfecto mismos inicios que finales marcados
            for m in range(len(corteInicio)):
                try:
                    recorridos = traso2.filter(fecha2__gt=corteInicio[m].fecha2) #filtro desde cada inicio
           #         print(corteInicio[m].fecha2)
                    traso3 = recorridos.filter(fecha2__lt=corteFin[m].fecha2) #termino el filtro con cada final
                    tres = [] #para guardas cada recorrido antes de pasarlo a la lista
                    v = traso3[0].point.x
                    b = traso3[0].point.y
                    p1 = Point(v, b)
                    listaPopupInicio.append(traso3[0])
                    for x in traso3:
                        v = x.point.x
                        b = x.point.y
                        tres.append((v, b))
                        hh.append((b,v))
                        if distance22 > 2:
                            p2 = Point(v, b)
                            distanciatotal += p1.distance(p2)
                            p1 = Point(v, b)
                            distance22 = 0
                        distance22= distance22 +1
                    listaPopupInicio.append(x)
                    if tres != []:
                        lista.append(tres)
                except:
                    continue
            kml1.newlinestring(name="AFTrakers", description="--", coords=hh)
            kml1.save(datosListos["Cuenta"]+".kml")
        else:
            if (len(corteInicio) != len(corteFin)): #casos especiales mas inicios que fin, puede quedar sin baterio o cualquier cosa que no deja
                #marcar el fin del recorrido cortando el recorrido de inicio a inicio sin contar los finales
                datos = traso2.filter(fecha2__gt=corteInicio[0].fecha2) #cargamos desde el primer dato de corte
                tres = [] #para guardas cada recorrido antes de pasarlo a la lista
                primero = True
                checkPop = True
                for m in range(len(datos)):
                    if ((datos[m].InicioRecorrido != "SI") and (datos[m].FinRecorrido != "SI")):
                        if checkPop:
                            listaPopupInicio.append(datos[m])
                            checkPop = False
                        v = datos[m].point.x
                        b = datos[m].point.y
                        if primero:
                            p1 = Point(v, b)
                            primero = False
                        tres.append((v, b)) #guarda para la web
                        hh.append((b,v)) #guarda para el KML
                        if distance22 > 2:
                            p2 = Point(v, b)
                            distanciatotal += p1.distance(p2)
                            p1 = Point(v, b)
                            distance22 = 0
                        distance22= distance22 +1
                    else:
                        if datos[m].InicioRecorrido == "SI":
                            primero = True
                            if tres != []: #es porque si hay un inicio y fin juntos no me genere una entrada vacia y de error
                                lista.append(tres)
                                if (datos[m - 1].FinRecorrido == "SI"):
                                    listaPopupInicio.append(datos[m - 2])
                                    checkPop = True
                                else:
                                    listaPopupInicio.append(datos[m - 1])
                                    checkPop = True
                            tres = []
    #chequeamos el ultimo dato si se corto con un fin o se desconecto o simplemente continio a un rango mayor lo corta en el criterio de busqueda
                if ((datos[len(datos)-1].FinRecorrido == "SI") or (datos[len(datos)-1].InicioRecorrido == "ContI")):
                    if tres != []:
                        lista.append(tres)
                kml1.newlinestring(name="AFTrakers", description="--", coords=hh)
                kml1.save(datosListos["Cuenta"]+".kml")
            else:
                lista = "Usuario no existe 2"
                print("no coninciden las aperturas con los cierres")
    except:
        lista = "Usuario no existe"
        distanciatotal = 0
    distanciatotal = distanciatotal * 100
    return lista, distanciatotal, listaPopupInicio

def CrearPointSeguimientoSearch(usuarioTest): #solo lo usa marcado de ruta para darle el zoom inicial
    try:
        x = Location.objects.filter(email=usuarioTest)  #[0]
        cantidad = len(x) -1
        while ((x[cantidad].InicioRecorrido == "SI") or (x[cantidad].FinRecorrido == "SI")):
            cantidad -= 1
        x = x[cantidad]
        v = x.point.x
        b = x.point.y
        tres = []
        tres.append((v, b))
    except:
        tres = "Usuario no existe"
    return tres

def CrearKML2(request, usuarioMostrado):  #Busca el archivo KML generado al ver el recorrido y lo envia al template para descarga
    if request.user.is_authenticated():
        if (request.method == 'GET'):
            email = usuarioMostrado
            archivo = open(email+".kml", "r")
            contenido = archivo.read()
            archivo.close()
        return HttpResponse(contenido)

def CrearPolyline(tres):
    try:
        tresCodificada = PolylineCodec().encode(tres)
        uno = "\\"
        dos = "\\\\"
        ff = tresCodificada.replace(uno, dos) #remplaso las barras que me da error al representar la ruta en JS
    except:
        ff = ""
    return ff

def getDatosUserSearch(usuario):
    datos = User.objects.get(email=usuario)
    RestoDatos = userProfile.objects.get(user=datos)
    return RestoDatos

def Seguimiento_view(request): #muestra la lista de posibles cuentas a localizar en vivo
    mensaje = "."
    if request.user.is_authenticated():
        if request.method == 'POST': #recupero los datos de quienes se asocian
            lista = request.POST.getlist("checkbox") #recupero los datos marcados en los box
            if (len(lista) > 1):
                mensaje = "A seleccionado mas 1 usuario, Por favor solo marque uno"
                user = request.user
                lista = CuentaAsociadas(user)
                ctx = {"lista": lista, "mensaje": mensaje }
                return render(request, 'seguimiento1.html', ctx)
            else:
                if (len(lista) != 0):
                    lista = lista[0]
                    datosIniciales = ChequeaSiNoSeConecto(lista) #da los datos para el zoom inicial
                    try: #chequeamos si es nuevo usuario y nunca a reportado salta la exception con el mensaje
                        y = datosIniciales[0][0]
                        x = datosIniciales[0][1]
                    except:
                        if datosIniciales == "NO":
                            mensaje =  "El Usuario no esta conectado" #esto es por si no esta reportando
                        else:
                            mensaje= "El usuario no a reportado" #esto es por su nunca se conecto(cliente nuevo)
                        user = request.user
                        lista = CuentaAsociadas(user)
                        ctx = {"lista": lista, "mensaje": mensaje }
                        return render(request, 'seguimiento1.html', ctx)
                    ctx = {"lista": lista, "mensaje": mensaje, "long": x, "lat": y }
                    return render(request, 'seguimiento.html', ctx)
        user = request.user
        lista = CuentaAsociadas(user)
        ctx = {"lista": lista, "mensaje": mensaje }
        return render(request, 'seguimiento1.html', ctx)
    else:
        return HttpResponseRedirect('/')

def ChequeaSiNoSeConecto(usuarioTest):
    try:
        x = Location.objects.filter(email=usuarioTest)  #[0]
        cantidad = len(x) -1
        if ((x[cantidad].InicioRecorrido == "SI") or (x[cantidad].FinRecorrido == "SI")):
            tres = "NO"
            return tres
        x = x[cantidad]
        v = x.point.x
        b = x.point.y
        tres = []
        tres.append((v, b))
    except:
        tres = "Usuario no existe"
    return tres

def dirt_count(request, lista):  #funcion para el restreo en vivo de un user la usa JScript
    if request.user.is_authenticated():
        if (request.method == 'GET'):
            dato = CrearPointSeguimiento(lista)
            dato1 = json.dumps(dato)
        return HttpResponse(dato1, content_type='application/json')

def darUbicacion(v,b): #tiene el try porque no siempre da la localizacion o se para de darla
    try:
        geolocator = Nominatim(scheme='http')
        location = geolocator.reverse((v,b),timeout=10)
        datos = location.address
        return datos
    except:
        return "Buscando Ubicacion..."

def CrearPointSeguimiento(usuarioTest):
    try:
        x = Location.objects.filter(email=usuarioTest)  #[0]
        usuario = User.objects.get(email=usuarioTest)
        numeroBusqueda = 0
        cantidad = len(x) -1
        estado = True  #chequiamos si se desconecta se pone en falsa y la vista cambia el icono de desconectado
        horaActual = datetime.datetime.now()
        horaAcomparar = horaActual - datetime.timedelta(0,30)
        if ((x[cantidad].FinRecorrido == "SI") or (x[cantidad].horarioIngreso <= horaAcomparar)):
            estado = False
        while ((x[cantidad].InicioRecorrido == "SI") or (x[cantidad].FinRecorrido == "SI")):
            numeroBusqueda += 1
            cantidad = cantidad - numeroBusqueda
        x = x[cantidad]
        v = x.point.x
        b = x.point.y
        berin = x.bearing #angulo para darle la direccion
        ubicacion = darUbicacion(v,b)
        horario = x.fecha2.strftime("%Y-%m-%d %H:%M:%S")
        print(horario)
        tres = []
        tres.append((v, b, berin, ubicacion, usuario.username,estado, horario ))
    except:
        tres = "Usuario no existe"
    return tres

def CuentaAsociadas(user): # no me toma el usuario creado con comandos nunca
    UsuarioActual = userProfile.objects.get(user=user)
    if (UsuarioActual.Tipo_Cuenta == "Admin"):
        lista = userProfile.objects.all()
        return lista
    else:
        #solo deja si el usuario puede tener cuentas osiadas y lista las cuentas posibles de asociar
        if (UsuarioActual.Tipo_Cuenta == "Chequeo"):
            empre = UsuarioActual.Empresa.all()[0]

            Cuentas = userProfile.objects.filter(Empresa=empre)
            Cuentas1 = Cuentas.filter(Asociado_A_Cuenta=user)
            Cuentas2 = Cuentas1.filter(Tipo_Cuenta="Individual")
            return Cuentas2
        elif (UsuarioActual.Tipo_Cuenta == "Cliente"):
            empre = UsuarioActual.Empresa.all()[0]

            Cuentas1 = userProfile.objects.filter(Empresa=empre)
            Cuentas2 = Cuentas1.filter(Tipo_Cuenta="Individual")
            return Cuentas2
        else:
            g = []
            g.append(UsuarioActual) #se retorna una lista para que pueda ser itinerante en la vista la mustra de los clientes
            return g

def userActivo(request, lista):  #funcion para estimar que usuarios estan activos
    if request.user.is_authenticated():
        print(lista)
        if (request.method == 'GET'):
            print("dentro")
            dato = chequearEnBaseActivo(lista)
            dato1 = json.dumps(dato)
        return HttpResponse(dato1, content_type='application/json')

#Me parece muy ineficiente el uso de memoria y consulta porque puede llegar a traer demasiados datos REVISAR
def chequearEnBaseActivo(usuarioTest): #busca ultimos reportes para chequear estados aprox segun tiempo
    tres = []
    try:
        estado = True
        horaActual = datetime.datetime.now()
        x = Location.objects.filter(email=usuarioTest)
        e = x.count()
        fechass= x[e -1].fecha2
        horaAcomparar = horaActual - datetime.timedelta(0,30)
        if ((x[e -1].FinRecorrido == "SI") or (x[e-1].horarioIngreso <= horaAcomparar)):
            estado = False
        tres.append(str(fechass))
        tres.append(estado)
        tres.append(usuarioTest)
    except:
        tres.append("Nunca se Conecto")
        tres.append(False)
        tres.append(usuarioTest)
    return tres
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
                    datosListos1, distanciaTotal = CrearListaPoint(datosListos)
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
                        print(datosListos2)
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
                    ctx = {'form': form, "lista": lista, "long": x, "lat": y, "usuarioMostrado": usuarioTrasar, "mensaje": mensaje,  "dato": datosListos2, "distanciaTotal": distanciaTotal}
                    return render(request,'search.html', ctx)
                else:
                    user = request.user
                    lista = CuentaAsociadas(user)
                    ctx = {'form': form, "lista": lista, "mensaje": mensaje,  "distanciaTotal": distanciaTotal}
                    return render(request, 'search.html', ctx)
            else:
                mensaje = "A seleccionado mas 1 o ningun usuario, Por favor solo marque uno"
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
    try:
        traso = Location.objects.filter(email=datosListos["Cuenta"])
        traso1 = traso.filter(fecha2__gte=datosListos["inicial"])
        traso2 = traso1.filter(fecha2__lte=datosListos["finales"])
        corteInicio = traso2.filter(InicioRecorrido="SI")
        corteFin = traso2.filter(FinRecorrido="SI")
        if (len(corteInicio) == len(corteFin)):  #Caso perdecto mismos inicios que finales marcados
            for m in range(len(corteInicio)):
                try:
                    recorridos = traso2.filter(fecha2__gt=corteInicio[m].fecha2)
           #         print(corteInicio[m].fecha2)
                    traso3 = recorridos.filter(fecha2__lt=corteFin[m].fecha2)
                    tres = [] #para guardas cada recorrido antes de pasarlo a la lista
                    v = traso3[0].point.x
                    b = traso3[0].point.y
                    p1 = Point(v, b)
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
                    distanciatotal = distanciatotal * 100
                    kml1.newlinestring(name="AFTrakers", description="--", coords=hh)
                    kml1.save(datosListos["Cuenta"]+".kml")
                    lista.append(tres)
                except:
                    continue
        else:
            if (len(corteInicio) != len(corteFin)): #casos especiales mas inicios que fin, puede quedar sin baterio o cualquier cosa que no deja
                #marcar el fin del recorrido cortando el recorrido de inicio a inicio sin contar los finales
                datos = traso2.filter(fecha2__gt=corteInicio[0].fecha2) #cargamos desde el primer dato de corte
                tres = [] #para guardas cada recorrido antes de pasarlo a la lista
                primero = True
                for m in range(len(datos)):
                    if ((datos[m].InicioRecorrido != "SI") and (datos[m].FinRecorrido != "SI")):
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
                            distanciatotal = distanciatotal * 100
                            kml1.newlinestring(name="AFTrakers", description="--", coords=hh)
                            kml1.save(datosListos["Cuenta"]+".kml")
                            if tres != []: #es porque si hay un inicio y fin juntos no me genere una entrada vacia y de error
                                lista.append(tres)
                            tres = []
    #chequeamos el ultimo dato si se corto con un fin o se desconecto o simplemente continio a un rango mayor lo corta en el criterio de busqueda
                if ((datos[len(datos)-1].FinRecorrido == "SI") or (datos[len(datos)-1].InicioRecorrido == "ContI")):
                    distanciatotal = distanciatotal * 100
                    kml1.newlinestring(name="AFTrakers", description="--", coords=hh)
                    kml1.save(datosListos["Cuenta"]+".kml")
                    lista.append(tres)
            else:
                lista = "Usuario no existe 2"
                print("no coninciden las aperturas con los cierres")
    except:
        lista = "Usuario no existe"
        distanciatotal = 0
    return lista, distanciatotal


def CrearPointSeguimientoSearch(usuarioTest): #solo lo usa marcado de ruta para darle el zoom inicial
    try:
        x = Location.objects.filter(email=usuarioTest)  #[0]
        cantidad = len(x)
        x = x[cantidad -2]
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
                    datosIniciales = CrearPointSeguimiento(lista) #da los datos para el zoom inicial
                    try: #chequeamos si es nuevo usuario y nunca a reportado salta la exception con el mensaje
                        y = datosIniciales[0][0]
                        x = datosIniciales[0][1]
                    except:
                        mensaje= "El usuario no a reportado"
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

def dirt_count(request, lista):  #funcion para el restreo en vivo de un user la usa JScript
    if request.user.is_authenticated():
        if (request.method == 'GET'):
            print("dentro")
            dato = CrearPointSeguimiento(lista)
            dato1 = json.dumps(dato)
        return HttpResponse(dato1, content_type='application/json')

def CrearPointSeguimiento(usuarioTest):
    try:
        x = Location.objects.filter(email=usuarioTest)  #[0]
        cantidad = len(x)
        x = x[cantidad -2]
        v = x.point.x
        b = x.point.y
        tres = []
        tres.append((v, b))
    except:
        tres = "Usuario no existe"
    return tres

def CuentaAsociadas(user): # no me toma el usuario creado con comandos nunca
    UsuarioActual = userProfile.objects.get(user=user)
    print (UsuarioActual.Tipo_Cuenta)
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

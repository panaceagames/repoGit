from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from .forms import LoginForm, RegisterForm, editUserForm, editUserFormIndividuales
from .models import userProfile
from django.contrib.auth.models import User

#loguea al usuario y redirige acorde a sus permisos el admin y solo users
def login_view(request):
    mensaje = ""
    if request.user.is_authenticated() and request.user.is_superuser:
        return HttpResponseRedirect('/registro/')
    elif request.user.is_authenticated():
        return HttpResponseRedirect('/maps/seguimiento/')
    else:
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                usuario = authenticate(username=username,password=password)
                if usuario is not None and usuario.is_active:
                    login(request,usuario)
                    if usuario.is_staff:
                        return HttpResponseRedirect("/registro/")
                    else:
                        return HttpResponseRedirect('/maps/seguimiento/')
                else:
                    mensaje = "usuario y/o password incorrectos"
        form = LoginForm()
        ctx = {'form':form,'mensaje':mensaje}
        return render(request, 'usuarios/login.html',ctx)

def logout_view(request):  #logout del user
    logout(request)
    return HttpResponseRedirect('/')

#@login_required
def register_view(request): #nuevo usuario primera etapa
    if request.user.is_authenticated():
        form = RegisterForm()
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                usuario = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password_one = form.cleaned_data['password_one']
                password_two = form.cleaned_data['password_two']
                u = User.objects.create_user(username=usuario, email=email, password=password_one)
                u.save()
                ff = userProfile(user=u)
                ff.save()
                UsuarioNuevo = User.objects.get(username=usuario)
                #le resto uno porque nose porque me los toma con un id menos hay que revisar
                numero_id = UsuarioNuevo.id - 1
                return HttpResponseRedirect('/EditarDatos/%s'%numero_id)
            else:
                form = RegisterForm(request.POST)
                ctx = {'form': form}
                return render(request, 'usuarios/register.html', ctx)
        else:
            ctx = {'form': form}
            return render(request, 'usuarios/register.html', ctx)
    else:
        return HttpResponseRedirect('/')

def edit_user_view(request,id_user): #ediatar usuario y segunda etapa de creacion del usuario
    if request.user.is_authenticated():
        info = "iniciado"
        UsuarioEnSesion = userProfile.objects.get(user=request.user) #usuario con la sesion abierta
        usuarioActual = userProfile.objects.get(pk=id_user) #usuario a editar
        if (UsuarioEnSesion.Tipo_Cuenta == "Admin"):
            if request.method == "POST":
                form = editUserForm(request.POST, request.FILES, instance=usuarioActual)
                if form.is_valid():
                    edit_user = form.save(commit=False)
                    form.save_m2m()  #guarda las relaciones ManyToMany
                    edit_user.status = True
                    edit_user.save()  #guarda la informacion
                    info = "Correcto"
                    info = "Guardado Satisfactoriamente"
                    return HttpResponseRedirect('/DatosPersonales/%s'%edit_user.id)   # recordemos que add se convirtio en un objeto restaurante mas arriba
            else:
                form = editUserForm(instance=usuarioActual)
            ctx = {'form': form, 'informacion': info, 'usuarioActual': usuarioActual}
            return render(request, 'usuarios/editusuario.html', ctx)
        else:
            if ((UsuarioEnSesion.Tipo_Cuenta == "Cliente") and (UsuarioEnSesion.Empresa.all()[0] == usuarioActual.Empresa.all()[0])): #chequea que solo si es de lamisma empresa pueda ver
                if request.method == "POST":
                    form = editUserFormIndividuales(request.POST, request.FILES, instance=usuarioActual)
                    if form.is_valid():
                        edit_user = form.save(commit=False)
                        form.save_m2m()  #guarda las relaciones ManyToMany
                        edit_user.status = True
                        edit_user.save()  #guarda la informacion
                        info = "Correcto"
                        info = "Guardado Satisfactoriamente"
                        return HttpResponseRedirect('/DatosPersonales/%s'%edit_user.id)   # recordemos que add se convirtio en un objeto restaurante mas arriba
                else:
                    form = editUserFormIndividuales(instance=usuarioActual)
                ctx = {'form': form, 'informacion': info, 'usuarioActual': usuarioActual}
                return render(request, 'usuarios/editusuario.html', ctx)
            else:
                return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def singleUser_view(request, id_user):   #vista datos de usuarios
    if request.user.is_authenticated():
        UsuarioEnSesion = userProfile.objects.get(user=request.user) #usuario con la sesion abierta
        usuarioActual = userProfile.objects.get(id=id_user)
        if ((UsuarioEnSesion.Tipo_Cuenta == "Admin") or ((UsuarioEnSesion.Tipo_Cuenta == "Cliente") and (UsuarioEnSesion.Empresa.all()[0] == usuarioActual.Empresa.all()[0]))):
            try:
                empre = usuarioActual.Empresa.all()[0] #asi me trae el nombre de la empresa solo
            except:
                empre = "Null"
            ctx = {'usuarioActual': usuarioActual, "empresa": empre}
            return render(request, 'usuarios/vistausuario.html', ctx)
        else:
            return HttpResponseRedirect('/')

def target_register_view(request):
    if request.user.is_authenticated():
        form = RegisterForm()
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                usuario = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password_one = form.cleaned_data['password_one']
                password_two = form.cleaned_data['password_two']
                u = User.objects.create_user(username=usuario, email=email, password=password_one)
                u.save()
                ff = userProfile(user=u)
                ff.save()
                return render(request, 'usuarios/thanks_register.html')
            else:
                form = RegisterForm(request.POST)
                ctx = {'form': form}
                return render(request, 'usuarios/register.html', ctx)
        else:
            ctx = {'form': form}
            return render(request, 'usuarios/register.html', ctx)
    else:
        return HttpResponseRedirect('/')


def ClientesGeneral_view(request):
    if request.user.is_authenticated():
        mensaje = "."

        UsuarioActual = userProfile.objects.get(user=request.user)
        #solo lista las cuentas asociadas y dejar editarlas y que no sean cuentas de otros clientes de la misma empresa
        if (UsuarioActual.Tipo_Cuenta == "Cliente"):
            empre = UsuarioActual.Empresa.all()[0]
            Cuentas = userProfile.objects.filter(Empresa=empre)
        #    Cuentas1 = Cuentas.filter(Asociado_A_Cuenta=request.user)
            Cuentas2 = Cuentas.exclude(Tipo_Cuenta="Cliente")
            ctx = {"UsuarioActual": UsuarioActual, "mensaje": mensaje, "lista": Cuentas2, "empre":empre }
            return render(request, 'usuarios/ClientesGeneral.html', ctx)
        elif (UsuarioActual.Tipo_Cuenta == "Admin"):
                lista = userProfile.objects.all()
                ctx = {"lista": lista, "UsuarioActual": UsuarioActual, "mensaje": mensaje }
                return render(request, 'usuarios/ClientesGeneral.html', ctx)
        else:
            mensaje = "Este usuario no posee permisos para acceder a esta seccion"
            ctx = {"UsuarioActual": UsuarioActual, "mensaje": mensaje }
            return render(request, 'usuarios/ClientesGeneral.html', ctx)
    else:
        return HttpResponseRedirect('/')


def AsociarCuentas_view(request, id_user):
    if request.user.is_authenticated():
        mensaje = "."
        UsuarioActual = userProfile.objects.get(id=id_user)
        UsuarioEnSesion = userProfile.objects.get(user=request.user) #usuario con la sesion abierta
        if ((UsuarioEnSesion.Tipo_Cuenta == "Admin") or ((UsuarioEnSesion.Tipo_Cuenta == "Cliente") and (UsuarioEnSesion.Empresa.all()[0] == UsuarioActual.Empresa.all()[0]))):
            if request.method == 'POST': #recupero los datos de quienes se asocian
                lista = request.POST.getlist("checkbox") #recupero los datos marcados en los box
                nombre = UsuarioActual.user.username #usuario al cual asociamos
                cliente = userProfile.objects.get(user=request.user) #usuario cliente que tiene las cuentas
                empre = UsuarioActual.Empresa.all()[0]
                Cuentas = userProfile.objects.filter(Empresa=empre)
                Cuentas2 = Cuentas.exclude(Tipo_Cuenta="Cliente") #cuentas del cliente

                if (len(lista) == 0): #si nomarca ninguno todos vuelven a ser solo del cliente
                    for y in Cuentas2:
                        usuarioAsociar = y
                        if (usuarioAsociar.Asociado_A_Cuenta == nombre):
                            usuarioAsociar.Asociado_A_Cuenta = cliente.user.username
                            usuarioAsociar.save()
                            usuarioAsociar = ""
                else:
                    for y in Cuentas2:
                        usuarioAsociar = y #para chequiar cada cuenta se van asignado aca
                        f = int(usuarioAsociar.id)
                        for x in lista: #asocia las cuentas
                            x = int(x)
                            if (f  == x ): #asigna las considencias a la cuenta de chequeo
                                usuarioAsociar.Asociado_A_Cuenta = nombre #el break es para que cuando encuentra la considencia corte de buscar
                                break
                            else: #devuelve los no marcados al cliente
                                if (usuarioAsociar.Asociado_A_Cuenta == nombre):
                                    usuarioAsociar.Asociado_A_Cuenta = cliente.user.username
                        usuarioAsociar.save()
                        usuarioAsociar = ""

                ctx = {"lista": Cuentas2}
                return render(request,  'usuarios/ClientesGeneral.html', ctx)
            else:
                #solo deja si el usuario puede tener cuentas asociadas y lista las cuentas posibles de asociar
                if ((UsuarioActual.Tipo_Cuenta == "Cliente") or (UsuarioActual.Tipo_Cuenta == "Chequeo")):
                    empre = UsuarioActual.Empresa.all()[0]
                    Cuentas = userProfile.objects.filter(Empresa=empre)
                    Cuentas1 = Cuentas.filter(Tipo_Cuenta="Individual")
                    ctx = {"UsuarioActual": UsuarioActual, "mensaje": mensaje, "lista": Cuentas1, "empre":empre }
                    return render(request, 'usuarios/AsociarRastreoAdmin.html', ctx)
                elif (UsuarioActual.Tipo_Cuenta == "Admin"):
                    return HttpResponseRedirect('/')
                else:
                    mensaje = "No puede asociar cuentas a este usuario"
                    ctx = {"mensaje": mensaje}
                    return render(request, 'usuarios/AsociarRastreoAdmin.html', ctx)
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')



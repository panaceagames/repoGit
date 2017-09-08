#from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User
# Create your models here.

"""_empresas = (
        (u'AirForceOne', u'AirForceOne'),
        (u'Pedorro', u'Pedorro'),
        (u'Aero 1', u'Aero 1'),
        (u'Pizza pepe', u'Pizza pepe'),
        )"""

class _empresas(models.Model):
    nombre = models.CharField(max_length=30)

    def __unicode__(self):
        return self.nombre

    def __str__(self):
        return self.nombre

#cuenta individual es para hacer el trastreo, chequeo es para poder ver las individuales que se le asigne
#cliente puede crear cuentas de chequeo y asignar las individuales
_TipoCuenta = (
        (u'Admin', u'Admin'),
        (u'Cliente', u'Cliente'),
        (u'Chequeo', u'Chequeo'),
        (u'Individual', u'Individual'),
        )

class Cuentas(models.Model):
    nombre = models.CharField(max_length=40, blank=True, null=True)
    empresa = models.CharField(max_length=30, blank=True, null=True)

    def __unicode__(self):
        return self.nombre

    def __str__(self):
        return self.nombre

class userProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    Empresa = models.ManyToManyField(_empresas)
    Rubro = models.CharField(max_length=40, blank=True, null=True)
    #al registrar pide mail y con eso controla que no se registren repetidos los users.
  #  Email = models.EmailField(max_length=60, blank=True, null=True)
    Email_Alternativo_de_Contacto = models.EmailField(max_length=60, blank=True, null=True)
    Direccion = models.CharField(max_length=60, blank=True, null=True)
    Telefono = models.CharField(max_length=15, blank=True, null=True)
    Telefono_Contacto = models.CharField(max_length=15, blank=True, null=True)
    Nombre_Contacto = models.CharField(max_length=30, blank=True, null=True)
    Abonos = models.CharField(max_length=4, blank=True, null=True)
    Descripcion_corta = models.TextField(max_length=500, null=True, blank=True)
    Tipo_Cuenta = models.CharField(max_length=30, choices=_TipoCuenta, blank=True, null=True)
   # Cuentas_Asociadas = models.ManyToManyField(Cuentas, blank=True, null=True)
    Asociado_A_Cuenta = models.CharField(max_length=30, null=True, blank=True)
    creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Cuenta_Activa = models.BooleanField(default=False)


    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.user.username

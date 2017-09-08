from django.contrib import admin

# Register your models here.
from .models import userProfile, _empresas, Cuentas

# Register your models here.
admin.site.register(userProfile)
admin.site.register(_empresas)
admin.site.register(Cuentas)
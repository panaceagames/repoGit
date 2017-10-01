#from django.db import models

# Create your models here.
# Notice that we are importing the gis models here
from django.contrib.gis.db import models

#modelo para guardar y extraer los datos
class Location(models.Model):

    name = models.CharField(max_length=50) #numero de telefono si lo envia el sim
    InicioRecorrido = models.CharField(max_length=10, null=True)
    FinRecorrido = models.CharField(max_length=10, null=True)
   # Geo Django field to store a point
    point = models.PointField(srid=4326, help_text='Represented as (longitude, latitude)', null=True)
    bearing = models.FloatField(null=True)
    altitud = models.FloatField(null=True)
    speed = models.FloatField(null=True)
    accuracy = models.FloatField(null=True)
    email = models.EmailField(max_length=60, blank=True, null=True)
    fecha2 = models.DateTimeField(blank=True, null=True)
    imei = models.CharField(max_length=30, null=True)
   # You MUST use GeoManager to make Geo Queries
    objects = models.GeoManager()

   # Geo Django field to store a polygon
 ##   area = models.PolygonField()

    def __unicode__(self):
        return '%s %s %s' % (self.name, self.point.x, self.point.y)



from django.db import models
from django.conf import settings

# Create your models here.
class ImageNasa(models.Model):
    id = models.AutoField(primary_key=True)
    img_src = models.URLField(max_length=1000)
    rover_name = models.CharField(max_length=100)
    camera_name = models.CharField(max_length=100)
    earth_date = models.DateField()
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    imageNasa = models.ForeignKey('links.ImageNasa', related_name='votes', on_delete=models.CASCADE)

from django.db import models
from django.conf import settings

class usersearch(models.Model):
    search = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    keywords = models.CharField(max_length=255)
    article = models.TextField()
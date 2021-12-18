from django.db import models

# Create your models here.
from core.models import AppURLModel


class ClickEventManager(models.Manager):
    def create_event(self, appurlInstance):
        if isinstance(appurlInstance, AppURLModel):
            obj, created = self.get_or_create(appurl_url=appurlInstance)
            obj.count += 1
            obj.save()
            return obj.count
        return None

class ClickEvent(models.Model): 
    appurl_url  = models.ForeignKey('core.AppURLModel', on_delete=models.CASCADE) 
    count       = models.IntegerField(default=0)
    updated     = models.DateTimeField(auto_now=True) 
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects = ClickEventManager()

    def __str__(self):
        return "{i}".format(i=self.count)
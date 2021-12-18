from django.conf import settings
from django.db import models

#from django.core.urlresolvers import reverse
from django_hosts.resolvers import reverse
# Create your models here.
from .utils import code_generator, create_shortcode
from .validators import validate_url, validate_dot_com

SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX", 15)

class AppURLModelManager(models.Manager):
    def all(self, *args, **kwargs):
        qs_main = super(AppURLModelManager, self).all(*args, **kwargs)
        qs = qs_main.filter(is_active=True)
        print(qs)
        return qs

    def refresh_shortcodes(self, items=None):
        qs = AppURLModel.objects.filter(id__gte=1)
        if items and isinstance(items, int):
            qs = qs.order_by("-id")[:items]

        new_code_count = 0
        for q in qs:
            q.shorcode = create_shortcode(q)
            new_code_count += 1
            q.save()
            print("ID: {0} ==> {1}".format(q.id, q.shorcode))
        return "New codes made: {0}".format(new_code_count)


class AppURLModel(models.Model):
    url = models.CharField(max_length=255)
    shortcode = models.CharField(max_length=SHORTCODE_MAX, unique=True, blank=True, null=False)
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = AppURLModelManager()

    def save(self, *args, **kwargs):
        if self.shortcode is None or self.shortcode == "": 
            self.shortcode = create_shortcode(self)
        super(AppURLModel, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.url)

    def __unicode__(self):
        return str(self.url)

    def get_short_url(self):
        url_path = reverse("scode", kwargs={'shortcode': self.shortcode}, host='www', scheme='http')
        return url_path

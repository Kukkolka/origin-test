from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.utils.encoding import smart_text as smart_unicode
from django.utils.translation import ugettext_lazy as _
import requests

class Bonds(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    isin = models.CharField(max_length = 30, null = False)
    size = models.IntegerField(default = 100000)
    currency= models.CharField(max_length = 5)
    maturity = models.DateField(_("Date Created"), auto_now_add=True)
    legal_name = models.CharField(max_length=30, null = False)
    lei = models.CharField(max_length = 30, null = False)

    def save(self, *args, **kwargs):
        if self.legal_name is None:
            self.apply_legal_name()
        super().save(*args, **kwargs)

    def apply_legal_name(self):
        url = "{}{}".format(settings.GLEIFAPI, '?lei=')
        r = requests.get(url = url, params = {'lei': self.lei})
        data=r.json()
        self.legal_name = data[0]['Entity']['LegalName']['$']

    def __unicode__(self):
        return "{} ({})".format(self.legal_name, self.isin)

    class Meta:
        verbose_name = _("Bond")
        verbose_name_plural = _("Bonds")

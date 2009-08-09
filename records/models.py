from django.db import models
from django.contrib.auth.models import User

class Records(models.Model):
    user = models.ForeignKey(User, unique=True, primary_key=True)
    text = models.TextField(blank=True)

    def __unicode__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = "Records"

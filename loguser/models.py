from django.db import models

class Ip(models.Model):
    user = models.CharField(default="", max_length=200)
    ip = models.CharField(max_length=200, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add = False, auto_now=True)

    def __str__(self):
        return self.user




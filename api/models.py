# models crea il contenitore delle informazioni di ogni classe, deve essere importato nella seione admin, model e views
from django.db import models
from django.contrib.auth.models import User
from api.utils import sendTransaction
import hashlib
# ------------------------------------------#


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(default="", max_length=200)
    datetime = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    hash = models.CharField(max_length=66, default=None, null=True, blank=True)
    txId = models.CharField(max_length=66, default=None, null=True, blank=True)

    def writeOnChain(self):
        self.hash = hashlib.sha256(self.content.encode('utf-8')).hexdigest()
        self.txId = sendTransaction(self.hash)
        self.save()

    def publish(self):
        self.save()

    def __str__(self):
        return self.title

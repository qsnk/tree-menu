from django.db import models
from django.urls import reverse

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True, null=True)
    named_url = models.CharField(max_length=200, blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children_set', on_delete=models.CASCADE)
    menu_name = models.CharField(max_length=100)

    def get_url(self):
        if self.url:
            return self.url
        elif self.named_url:
            return reverse(self.named_url)
        return '#'

    def __str__(self):
        return self.name
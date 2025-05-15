from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, related_name='items', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200, blank=True)
    named_url = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order']

    def get_url(self):
        from django.urls import reverse
        if self.named_url:
            return reverse(self.named_url)
        return self.url

    def __str__(self):
        return self.title
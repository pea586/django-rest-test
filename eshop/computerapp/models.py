from django.db import models

# Create your models here.



from django.utils.six import python_2_unicode_compatible

from django.conf import settings



@python_2_unicode_compatible
class Category(models.Model):
    """商品类别:笔记本，平板电脑，一体机，台式机、服务器"""
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



@python_2_unicode_compatible
class Manufacturer(models.Model):
    """生产厂商"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    logo = models.ImageField(blank=True, null=True, max_length=200, upload_to='manufacturer/upload/%Y/%m/%d')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


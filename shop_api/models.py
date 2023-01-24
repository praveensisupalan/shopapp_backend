from django.db import models

# Create your models here.

class shop(models.Model):
    shop_name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    image = models.ImageField(upload_to="images", blank=False,null=False)

    def __str__(self):
        return self.shop_name
from django.db import models

# Create your models here.
class Photo(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='photos/%Y/%m/%d')


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    text = models.TextField()
    pic = models.ForeignKey(Photo)



class Ingredient(models.Model):
    name = models.CharField(max_length=255)

CONVERSIONS= ((0,"gramas"),
              (1,"kilos"),
              (3,"celcious")  
            )

class Unit(models.Model):
    metric = models.CharField(max_length=255)
    imperial = models.CharField(max_length=255)
    conversion = models.IntegerField(choices=CONVERSIONS)

    def get_metric(self):
        pass
    
    def get_imperial(self):
        pass

class Measurement(models.Model):
    post = models.ForeignKey(Post)
    ingredient = models.ForeignKey(Ingredient)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.ForeignKey(Unit)
    order = models.IntegerField()

    

    

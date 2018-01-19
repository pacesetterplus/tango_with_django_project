from django.db import models

# Create your models here.

#class represent a category
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    #similar to java toString method
    def __str__(self):
        return self.name

#class represent a page
class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    #similar to java toString method
    def _str_(self):
        return self.title


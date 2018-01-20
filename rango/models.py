from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.

# class represent a category
# class represents table
# variables represent field
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category,self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    #similar to java toString method
    def __str__(self):
        return self.name

# class represent a page
# class represents table
# variables represent field
class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    #similar to java toString method
    def __str__(self):
        return self.title


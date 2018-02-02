from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

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
        if (self.views < 0):
            self.views = 0;
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
    #first_visit = models.TimeField()
    #last_visit = models.TimeField()

    #similar to java toString method
    def __str__(self):
        return self.title


class UserProfile(models.Model):
    #this is reqd. link userprofile to a usermodel instance.
    user = models.OneToOneField(User)

    #additional attributes we wish to includes
    website = models.URLField(blank = True)
    picture = models.ImageField(upload_to='profile_images', blank = True)
    #toString equivalent
    def __str__(self):
        return self.user.name





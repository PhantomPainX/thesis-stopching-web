from django.db import models
from django.utils.translation import gettext_lazy as _
from main_app.webp import WEBPField
from django.contrib.auth.models import User

class AINewsClassification(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class UserNewsClassification(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class NewsCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

def new_webp(instance, filename):
    #Revisar cantidad de archivos en la carpeta portadas
    from django.conf import settings
    import os
    import glob
    cant_archivos = len(glob.glob(os.path.join(settings.MEDIA_ROOT, 'images/news/front/*')))
    #cambiar el nombre de la imagen
    nombre = str(cant_archivos+1)
    filename = "images/news/front/{}.webp".format(nombre)
    return filename

class New(models.Model):
    title = models.CharField(max_length=512)
    author = models.CharField(max_length=256, null=True, blank=True)
    new_date = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = WEBPField(
        verbose_name=_('Image'),
        upload_to=new_webp,
        default='images/news/front/default.webp',
    )
    remote_image = models.URLField(null=True, blank=True)
    category = models.ForeignKey(NewsCategory, null=False, default=1, on_delete=models.SET_DEFAULT)
    detection_accuracy = models.FloatField(null=True, blank=True)
    ai_classification = models.ForeignKey(AINewsClassification, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

class UsersClassification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    new = models.ForeignKey(New, on_delete=models.CASCADE)
    classification = models.ForeignKey(UserNewsClassification, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.new.title + " - " + self.classification.name

class Comment(models.Model):
    new = models.ForeignKey(New, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    in_response_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.new.title + " - " + self.user.username

class NewSection(models.Model):
    new = models.ForeignKey(New, on_delete=models.CASCADE)
    title = models.CharField(max_length=512)
    content = models.TextField()
    position = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.new.title + " - " + self.title

def new_body_webp(instance, filename):
    #Revisar cantidad de archivos en la carpeta portadas
    from django.conf import settings
    import os
    import glob
    cant_archivos = len(glob.glob(os.path.join(settings.MEDIA_ROOT, 'images/news/body/*')))
    #cambiar el nombre de la imagen
    nombre = str(cant_archivos+1)
    filename = "images/news/body/{}.webp".format(nombre)
    return filename

class NewsImage(models.Model):

    new = models.ForeignKey(New, on_delete=models.CASCADE)
    image = WEBPField(
        verbose_name=_('Image'),
        upload_to=new_body_webp,
        default='images/news/body/default.webp',
    )
    position = models.IntegerField(default=1)
    remote_image = models.URLField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.new.title

class UserExtra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prefered_categories = models.ManyToManyField(NewsCategory, through='UserCategory', blank=True)

    def __str__(self):
        return self.user.username

class UserCategory(models.Model):
    user_extra = models.ForeignKey(UserExtra, on_delete=models.CASCADE)
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " - " + self.category.name

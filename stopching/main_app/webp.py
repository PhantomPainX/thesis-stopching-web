import io
from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.db.models.fields.files import ImageFieldFile
 
 
class WEBPFieldFile(ImageFieldFile):
 
    def save(self, name, content, save=True):
        content.file.seek(0)
        image = Image.open(content.file)
        image_bytes = io.BytesIO()
        image.save(fp=image_bytes, format="webp", optimize = True, quality = 80)
        image_content_file = ContentFile(content=image_bytes.getvalue())
        print("image_content_file: ", image_content_file)
        super().save(name, image_content_file, save)
 
 
class WEBPField(models.ImageField):
    attr_class = WEBPFieldFile
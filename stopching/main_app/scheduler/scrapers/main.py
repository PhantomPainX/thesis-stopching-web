from main_app.models import *
import os, requests
from django.conf import settings

class Scraper:

    def __init__(self):
        self.front_images_folder = settings.MEDIA_ROOT + '/images/news/front/'
        self.body_images_folder = settings.MEDIA_ROOT + '/images/news/body/'

    def check_if_new_exists(self, title):
        return New.objects.filter(title=title).exists()

    def get_folder_total_files(self, folder_path):
        totalFiles = 0
        if os.path.exists(folder_path):
            for base, dirs, files in os.walk(folder_path):
                for Files in files:
                    totalFiles += 1
        else:
            print("No existe la carpeta de portadas")

        return totalFiles

    def download_image(self, img_url, img_number, folder_path):
        try:
            request_image = requests.get(img_url)
            image_folder_path = open(folder_path+"{}".format(img_number)+".webp", 'wb')
            image_folder_path.write(request_image.content)
            image_folder_path.close()
        except:
            return False

        if os.path.exists(folder_path+"{}".format(img_number)+".webp"):
            return True
        else:
            return False
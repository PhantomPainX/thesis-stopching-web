# Scraper de la BBC
from bs4 import BeautifulSoup
import requests, time
from main_app.models import *
from django.conf import settings
from main_app.scheduler.categories import Categories
from main_app.scheduler.scrapers.main import Scraper

# Aqui se definen las categorias que aceptaran los scrapers
categories = Categories()

# Estas son las urls que pertececen a las categorias que hay en la BD
bbc_categories = [
    {
        "name": categories.america_latina,
        "url": "https://www.bbc.com/mundo/topics/c7zp57yyz25t"
    },
    {
        "name": categories.coronavirus,
        "url": "https://www.bbc.com/mundo/topics/c67q9nnn8z7t"
    },
    {
        "name": categories.economia,
        "url": "https://www.bbc.com/mundo/topics/c06gq9v4xp3t"
    },
    {
        "name": categories.ciencia,
        "url": "https://www.bbc.com/mundo/topics/ckdxnw959n7t"
    },
    {
        "name": categories.salud,
        "url": "https://www.bbc.com/mundo/topics/cpzd498zkxgt"
    },
    {
        "name": categories.cultura,
        "url": "https://www.bbc.com/mundo/topics/c2dwq9zyv4yt"
    },
    {
        "name": categories.tecnologia,
        "url": "https://www.bbc.com/mundo/topics/cyx5krnw38vt"
    }
]

class BBCScraper(Scraper):

    def __init__(self):
        self.front_images_folder = settings.MEDIA_ROOT + '/images/news/front/'
        self.body_images_folder = settings.MEDIA_ROOT + '/images/news/body/'

    # Obtiene las noticias y las guarda en la base de datos
    # Noticias, secciones de las noticias e imagenes
    def get_news(self, url_to_scrape, category_name):

        downloaded_news = 0

        # Se obtiene el html de la página
        page = requests.get(url_to_scrape)
        soup = BeautifulSoup(page.content, 'html.parser')
        # ----------------------------

        # Se seleccionan todas los articulos de la página y se declara una lista donde 
        # ira la url, titulo e imagen de cada articulo
        news_li = soup.find_all('li', class_='bbc-v8cf3q')
        news_urls = []
        # ----------------------------

        # Se recorre cada articulo y se obtiene la url, titulo e imagen
        for new_li in news_li:
            news_urls.append({
                "url": new_li.find('a')['href'],
                "title": new_li.find('a', class_='bbc-uk8dsi e1d658bg0').text,
                "image": new_li.find('img')['src']
            })
        # ----------------------------

        # Por cada noticia en el arreglo de noticias
        for new in news_urls:

            # Se verifica si la noticia ya existe en la base de datos, si existe se salta a la siguiente iteración
            if self.check_if_new_exists(new['title']):
                continue
            
            # Se obtiene el html de la noticia
            page = requests.get(new['url'])
            soup = BeautifulSoup(page.content, 'html.parser')
            # ----------------------------

            # Se obtienen los metadatos de la noticia, si alguno de ellos no existe se controla el error
            try:
                title = soup.find('h1', class_='bbc-14gqcmb e1p3vdyi0').text
                print(new['title'])
            except AttributeError:
                print("No se pudo obtener el titulo de la noticia, saltando...")
                continue

            try:
                author = soup.find('li', class_='bbc-1a3w4ok euvj3t11').text
            except AttributeError:
                author = ""

            try:
                new_date = soup.find('time', class_='bbc-1dafq0j e1mklfmt0').text
            except AttributeError:
                new_date = ""
            # ----------------------------
            
            # Se obtienen el numero total de imagenes que tiene la carpeta de imagenes front
            # Luego se descarga la imagen de la noticia y se le asigna el nombre de un numero
            new_image = new['image']
            totalFiles = self.get_folder_total_files(self.front_images_folder)
            img_is_downloaded = self.download_image(new_image, totalFiles+1, self.front_images_folder)
            # ----------------------------

            # Si la imagen se descargo correctamente se crea la noticia en la base de datos con la imagen
            if img_is_downloaded:
                image_path = "images/news/front/{}.webp" .format(totalFiles+1)
                #get or create category
                new_category = NewsCategory.objects.get_or_create(name=category_name)[0]

                new_object = New.objects.create(
                    title=new['title'],
                    author=author,
                    new_date=new_date,
                    image=image_path,
                    remote_image=new_image,
                    category=new_category
                )
            # Si no se descargo la imagen se crea la noticia en la base de datos sin imagen
            else:
                new_object = New.objects.create(
                    title=new['title'],
                    author=author,
                    new_date=new_date,
                    remote_image=new_image,
                    category=new_category
                )
            downloaded_news += 1 # Se suma al contador la noticia descargada
            # ----------------------------

            new_object_id = new_object.id

            # Se obtienen las secciones de la noticia, cada uno podria contener un titulo y parrafos
            new_sections = soup.find_all('div', class_='bbc-19j92fr ebmt73l0')
            # Se obtienen los bloques que contienen las imagenes de la noticia
            new_images = soup.find_all('div', class_='bbc-1ka88fa ebmt73l0')

            # section_id sera el que controle cuando se debe crear una seccion nueva
            # si es -1, entonces se debe crear una nueva seccion
            section_id = -1
            # Contador para el orden de las secciones de la noticia
            section_number = 0
            # Aqui iran los parrafos de la seccion separados en \n\n
            paragraphs = ""
            for section in new_sections:

                section_title = ""

                # Si la seccion tiene un titulo, se obtiene, se resetean los parrafos y se asigna -1 a section_id
                # Si la section_id no era -1, o sea que habia una seccion anterior, se actualiza la seccion con los parrafos
                # Esto se hace ya que la seccion actual terminara y empezara una nueva
                if section.find('h2'):

                    if section_id != -1:
                        NewSection.objects.filter(id=section_id).update(
                            content=paragraphs
                        )

                    section_title = section.find('h2').text
                    section_id = -1
                    paragraphs = ""

                # Si la section_id es -1, se crea una nueva seccion con el titulo, la noticia y la posicion
                if section_id == -1:
                    section_number += 1
                    NewSection.objects.create(
                        new=new_object,
                        title=section_title,
                        position=section_number
                    )
                    section_id = NewSection.objects.get(title=section_title, new=new_object).id

                # Si la seccion no tiene titulo y es parrafo, entonces se concadenan los parrafos
                if section.find('p'):
                    if paragraphs == "":
                        paragraphs = section.find('p').text
                    else:
                        paragraphs += "\n\n"+section.find('p').text

            # Si es la ultima seccion, se actualiza la seccion actual con los parrafos al salir del ciclo
            if section_id != -1:
                if paragraphs != "":
                    NewSection.objects.filter(id=section_id).update(
                        content=paragraphs
                    )
            
            # Aqui solo se descargaran las imagenes de la noticia en orden, de arriba hacia abajo
            body_image_position = 0
            for image in new_images:
                note = ""
                if image.find('img'):
                    body_img = image.find('img')['src']
                    bodytotalFiles = self.get_folder_total_files(self.body_images_folder)
                    body_img_is_downloaded = self.download_image(body_img, bodytotalFiles+1, self.body_images_folder)

                    if body_img_is_downloaded:
                        body_image_path = "images/news/body/{}.webp" .format(bodytotalFiles+1)
                        body_image_position += 1

                        if image.find('figcaption', class_='bbc-rhuvwm e6i104o0'):
                            note = image.find('figcaption', class_='bbc-rhuvwm e6i104o0').find('p').text
                            
                        NewsImage.objects.create(
                            new=new_object,
                            image=body_image_path,
                            position=body_image_position,
                            remote_image=body_img,
                            note=note
                        )

            time.sleep(1)

        return downloaded_news

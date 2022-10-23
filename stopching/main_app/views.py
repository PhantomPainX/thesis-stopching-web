from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'index.html')

def scrape(request):
    #bbc_scraper = BBCScraper('https://www.bbc.com/mundo/topics/c7zp57yyz25t')
    #downloaded_news = bbc_scraper.get_news()
    return HttpResponse("No se descargaron noticias")
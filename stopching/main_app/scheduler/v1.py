# Aqui ira la instancia del bot automatico que iniciara una tarea cada cierto lapso de tiempo
from apscheduler.schedulers.background import BackgroundScheduler
from main_app.scheduler.scrapers.scraper_bbc import BBCScraper, bbc_categories

def scrapingTasks():
    print("Starting Scraping Tasks...")
    downloaded_news = 0
    for category in bbc_categories:
        print("Scraping bbc category: " + category['name'])
        bbc_scraper = BBCScraper()
        downloaded_news += bbc_scraper.get_news(category['url'], category['name'])

    print("Se descargaron {} noticias" .format(downloaded_news))


def startAutomaticTasks():
    scrapingTasks()
    print("Starting Automatic Tasks...")
    scheduler = BackgroundScheduler(timezone='America/Argentina/Buenos_Aires')
    scheduler.add_job(scrapingTasks, 'interval', hours=5, id="scrapingTasks", replace_existing=True)
    scheduler.start()
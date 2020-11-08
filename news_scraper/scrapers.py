import requests
import bs4
from .models import Newspaper,Author,Article
import dateparser
from django.utils import timezone

def get_soup(website):
    
    res = requests.get(website).text
    
    soup = bs4.BeautifulSoup(markup=res,features="html.parser")

    return soup

def remove_prefix(text, prefix) -> str:
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def create_article(newspaper,headline,category,author,pub_day,link):
    
    try:
        Article.objects.get(newspaper= newspaper,headline= headline)
    except Article.DoesNotExist:
        Article.objects.create(
            newspaper = newspaper,
            headline = headline,
            category = category,
            author=author,
            pub_day = pub_day,
            link = link
        )
    
def initialize_newspapers():
    Newspaper.objects.get_or_create(newspaper_name="Clarín")
    Newspaper.objects.get_or_create(newspaper_name="La Nación")
    Newspaper.objects.get_or_create(newspaper_name="Ámbito Financiero")
    Newspaper.objects.get_or_create(newspaper_name="Página 12")

def scrape_everything():
    scrape_clarin()
    scrape_lanacion()
    scrape_ambito()
    scrape_pagina_12()

def scrape_clarin():

    #Initialize the Newspaper instance for this scraper
    newspaper = Newspaper.objects.get(newspaper_name="Clarín")
    
    #List of newspaper subsections, collected by hand
    subsections = {"https://www.clarin.com/politica/",
                    "https://www.clarin.com/economia/",
                    "https://www.clarin.com/sociedad/",
                    "https://www.clarin.com/mundo/"
                    }

    for subsection in subsections:

        soup = get_soup(subsection)
        section = soup.find(attrs={"class":"section-name-sub"}).text.strip()
        articles = soup.find(attrs={"class":"box-notas"}).contents

        for box in articles:

            #If the current obj is not an article box, skip it.
            if type(box) is not bs4.element.Tag:
                continue
            if "des-adv" in box["class"]:
                continue

            #Retrieve the article from within the box
            article = box.article
            
            #Scrape the main data (headline, author, link, publication date)
            headline = article.find(["h1","h2","h3"]).text.strip()
            author = article.find(attrs={"class":"data-txt"})
            pub_day = article.find(attrs={"class":"fecha"}).text.strip()
            pub_day = dateparser.parse(pub_day)

            link = "https://www.clarin.com" + article.a["href"]

            if author is not None:
                author,created = Author.objects.get_or_create(
                    name=author.text
                )
            
            create_article(
                newspaper = newspaper,
                headline = headline,
                category = section,
                author=author,
                pub_day = pub_day,
                link = link
            )

def scrape_lanacion():

    #Initialize the Newspaper instance for this scraper
    newspaper = Newspaper.objects.get(newspaper_name="La Nación")

    subsections = {"https://www.lanacion.com.ar/politica",
                "https://www.lanacion.com.ar/seguridad",
                "https://www.lanacion.com.ar/el-mundo",
                "https://www.lanacion.com.ar/salud",
                "https://www.lanacion.com.ar/educacion",
                "https://www.lanacion.com.ar/ciencia",
                }

    for subsection in subsections:

        soup = get_soup(subsection)
        section = soup.find(attrs={"class":"categoria"}).text.strip()
        articles = soup.find("section",attrs={"class":["listado"]}).contents

        for article in articles:

            #If the current obj is not an article, skip it.
            if type(article) is not bs4.element.Tag:
                continue
            if article.name != "article":
                continue
            
            #Scrape the main data (headline, author, link, publication date)
            headline = article.h2.text.strip()
            if "autor" in article["class"] and article.span.a != None:
                    author = article.span.a.text
                    author,created = Author.objects.get_or_create(
                        name=author
                        )
            else:
                author = None

            pub_day = article.find(attrs={"class":"fecha"}).text
            pub_day = dateparser.parse(pub_day)

            link = "https://www.lanacion.com.ar" + article.h2.a["href"]

            create_article(
                newspaper = newspaper,
                headline = headline,
                category = section,
                author= author,
                pub_day = pub_day,
                link = link
            )

def scrape_ambito():
    
    #Initialize the Newspaper instance for this scraper
    newspaper = Newspaper.objects.get(newspaper_name="Ámbito Financiero")

    subsections = {"https://www.ambito.com/contenidos/economia.html",
                    "https://www.ambito.com/contenidos/finanzas.html",
                    "https://www.ambito.com/contenidos/politica.html",
                    "https://www.ambito.com/contenidos/negocios.html"
                    }
    
    for subsection in subsections:

        soup = get_soup(subsection)
        section = soup.find("h1",attrs={"class":"obj-title"}).text.strip()
        articles = soup.find_all("article",attrs={"data-type":"article"})

        for article in articles:
            
            #Scrape the main data (headline, author, link, publication date)
            headline = article.find(attrs={"class":"title"}).text.strip()
            link = article.find(attrs={"class":"title"}).a["href"]
            pub_day = soup.find("time").text

            pub_day = dateparser.parse(pub_day)

            create_article(
                    newspaper = newspaper,
                    headline = headline,
                    category = section,
                    author=None,
                    pub_day = pub_day,
                    link = link
                )

def scrape_pagina_12():
    
    #Initialize the Newspaper instance for this scraper
    newspaper = Newspaper.objects.get(newspaper_name="Página 12")

    subsections = {"https://www.pagina12.com.ar/secciones/el-pais",
                    "https://www.pagina12.com.ar/secciones/economia",
                    "https://www.pagina12.com.ar/secciones/sociedad",
                    "https://www.pagina12.com.ar/secciones/el-mundo"
                    }

    for subsection in subsections:

        soup = get_soup(subsection)
        section = soup.find(attrs={"class":"text-section-header"}).text.strip()
        articles = soup.find_all("article")

        for article in articles:
            
            #Scrape the main data (headline, author, link, publication date)
            headline = article.find(attrs={"class":"title-list"}).text.strip()
            author = article.find(attrs={"class":"author"})
            pub_day = article.find(attrs={"class":"date"}).text
            link = article.find(attrs={"class":"title-list"}).a["href"]

            if author is not None:
                author = author.a.text
                author,created = Author.objects.get_or_create(
                name=author
                )

            pub_day = dateparser.parse(pub_day)

            create_article(
                newspaper = newspaper,
                headline = headline,
                category = section,
                author=author,
                pub_day = pub_day,
                link = link
            )

def scrape_infobae():

    #Initialize the Newspaper instance for this scraper
    infobae = Newspaper("Infobae")

    subsections = {"https://www.infobae.com/politica/",
                    "https://www.infobae.com/sociedad/",
                    "https://www.infobae.com/tecno/",
                    "https://www.infobae.com/educacion/",
                    "https://www.infobae.com/campo/",
                    "https://www.infobae.com/ultimas-noticias/"
                    }

    for subsection in subsections:

        
        soup = get_soup(subsection)
        section = soup.find(attrs={"class":"section_title"}).text.strip()
        articles = soup.find_all(attrs={"class":"card-container"})

        for article in articles:

            #Scrape the main data (headline, author, link, publication date)
            headline = article.find(attrs={"class":"headline"}).h2.text.strip()
            link = article.find(attrs={"class":"headline"}).a["href"]
            link = "https://www.infobae.com" + link

            infobae.add_article(section,Article(headline,link=link))

def scrape_perfil():
       
    #Initialize the Newspaper instance for this scraper
    newspaper = Newspaper.objects.get(newspaper_name="Diario Perfil")

    subsections = {"https://www.perfil.com/seccion/politica/",
                    "https://www.perfil.com/seccion/economia/",
                    "https://www.perfil.com/seccion/sociedad/",
                    "https://www.perfil.com/seccion/internacional",
                    "https://www.perfil.com/ultimo-momento/"}

    for subsection in subsections:

        soup = get_soup(subsection)
        section = soup.find(attrs={"class":"tituloCanal"}).text.strip()
        articles = soup.find_all("article")

        for article in articles:
            
            #Check if we have an article
            if "bannerEntreNotas" in article["class"]:
                continue
            
            #Scrape the main data (headline, author, link, publication date)
            headline = article.h2.a.text.strip()
            pub_day = article.find(attrs={"class":"dateTime"})
            link = remove_prefix(article.a["href"],"https://www.perfil.com")
            link = "https://www.perfil.com" + link

            if pub_day is not None:
                pub_day = pub_day.text.strip()
                pub_day = dateparser.parse(pub_day)
            else:
                pub_day = timezone.now()
            
            create_article(
                newspaper = newspaper,
                headline = headline,
                category = section,
                author=None,
                pub_day = pub_day,
                link = link
            )




from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import time
import re



def scrape():
    #browser start
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)



    #nasa info
    urlnasa = 'https://mars.nasa.gov/news/'

    browser.visit(urlnasa)
    htmlnasa = bs(browser.html, "html.parser")
    time.sleep(8)


    newssummary = htmlnasa.find('div', class_='article_teaser_body')
    newsp = newssummary.get_text()

    newstitle = newssummary.previous_sibling.get_text()



    # nasa picture
    urlpicture = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(urlpicture)
    browser.find_by_id('full_image').click()



    # getting img url
    time.sleep(5)
    imgsoup = bs(browser.html, "html.parser")

    imgtag = imgsoup.find('img', class_='fancybox-image')

    imgsource = imgtag.get('src')

    imgsourcefinal = 'https://www.jpl.nasa.gov/' + imgsource




    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    weather_soup = bs(html, "html.parser")
    pattern = re.compile(r'sol')
    mars_weather = weather_soup.find('span', text=pattern).text



    spacefacts = "https://space-facts.com/mars/"
    tables = pd.read_html(spacefacts)
    facts = tables[1]
    facts_html = facts.to_html()


    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    time.sleep(6)



    html_hemispheres = browser.html

    soup = bs(html_hemispheres, 'html.parser')

    hemispheres = soup.find_all('div', class_='item')

    hemispheresbase = 'https://astrogeology.usgs.gov'

    hemisphereimgs = []

    for hem in hemispheres: 
        title = hem.find('h3').text
        
        partial_img_url = hem.find('a', class_='itemLink product-item')['href']
        
        browser.visit(hemispheresbase + partial_img_url)
        
        partial_img_html = browser.html
        
        soup = bs( partial_img_html, 'html.parser')
        
        img_url = hemispheresbase + soup.find('img', class_='wide-image')['src']
        
        hemisphereimgs.append({"title" : title, "img_url" : img_url})
        

    browser.quit()

    output = {'mars_news_title' : newstitle, 'mars_news_info' : newsp, 'mars_Image' : imgsourcefinal, 
        'mars_weather' : mars_weather, 'mars_facts' : facts_html, 'hemisphere_images' : hemisphereimgs}


    return output


# print(newstitle, newssummary, imgsourcefinal, mars_weather, facts, hemisphereimgs)





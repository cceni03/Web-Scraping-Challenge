from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Mars News URL of page to be Scraped
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    # Retrieve News Title and Paragraph
    news_title = news_soup.find_all('div', class_='content_title')[1].text
    news_p = news_soup.find_all('div', class_='article_teaser_body')[0].text

    # Mars Image to be scraped
    jpl_nasa_url = 'https://www.jpl.nasa.gov'
    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url)
    html = browser.html
    images_soup = BeautifulSoup(html, 'html.parser')

    # Retrieve JPL Featured Space Image
    relative_image_path = images_soup.find_all('img')[3]["src"]
    featured_image_url = jpl_nasa_url + relative_image_path

    # Mars Facts
    mars_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_url)
    mars_df = tables[0]
    mars_df.rename(columns = {0:'Fact Heading', 1:'Fact Data'}, inplace = True)
    mars_df.set_index('Fact Heading', inplace = True)
    mars_df
    
    # Mars Hemisphere
    usgs_url = 'https://astrogeology.usgs.gov'
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    hemispheres_soup = BeautifulSoup(hemispheres_html, 'html.parser')
    
    # Mars Hemispheres Data
    all_mars_hemispheres = hemispheres_soup.find('div', class_='collapsible results')
    mars_hemispheres = all_mars_hemispheres.find_all('div', class_='item')
    hemisphere_image_urls = []

    # Iterate through Hemisphere Data
    for i in mars_hemispheres:
        # Collect Title
        hemisphere = i.find('div', class_="description")
        title = hemisphere.h3.text    

        # Collect Image Link
        hemisphere_link = hemisphere.a["href"]    
        browser.visit(usgs_url + hemisphere_link)        
        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')        
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']

        # Create Dictionary 
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url        
        hemisphere_image_urls.append(image_dict)

    # Mars Dictionary
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_html_table": str(mars_html_table),
        "hemisphere_images": hemisphere_image_urls
    }

    return mars_dict
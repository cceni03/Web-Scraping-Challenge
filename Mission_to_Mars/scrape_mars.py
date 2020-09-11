import os
from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd
import requests
import pymongo
import time

def initial_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_url():
    browser = initial_browser()

    # URL to scrape
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(2)

    # Mars Image to be Scraped
    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve JPL Featured Space Image
    jpl_nasa_url = 'https://www.jpl.nasa.gov'
    relativeimage_path = soup.find_all('img')[3]["src"]
    featuredimage_url = jpl_nasa_url + relativeimage_path
    print(featuredimage_url)

    # Full Image Button
    image_box = soup.find('a', class_='button fancybox')
    print(image_box)
    try:
        browser.click_link_by_id('full_image')
    except:
        print("Cannot find FULL IMAGE button")

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    try:
        Button_Link = browser.links.find_by_partial_href('spaceimages/details')
        print(Button_Link['href'])
        Button_Link.click()
        
    except:
        print("Cannot find FULL IMAGE button")

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    targetmars_url = soup.find('figure', class_='lede').a['href']
    print(targetmars_url)

    base_url = 'https://www.jpl.nasa.gov'
    featuredmars_imageurl = base_url + targetmars_url
    featuredmars_imageurl

    # Mars Facts
    mars_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_url)
    mars_df = tables[0]
    mars_df.rename(columns = {0:'Fact Heading', 1:'Fact Data'}, inplace = True)
    mars_df.set_index('Fact Heading', inplace = True)
    mars_df

    # Converting Mars DataFrame into HTML Table
    mars_html = mars_df.to_html(index=False)
    mars_html

    # Mars Hemisphere
    base_url = "https://astrogeology.usgs.gov/"
    marshemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(marshemisphere_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Hemisphere Images
    hemisphereimage_list = soup.find_all('div', id='product-section')
    print(hemisphereimage_list)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    marshemisphere_list = []
    hemisphereimage_list = []

    hemisphere_titles = hemisphereimage_list = soup.find_all('h3')

    for hemisphere_title in hemisphere_titles:
        marshemisphere_list.append(hemisphere_title.text)
    print(marshemisphere_list)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('div', class_='item')

    mars_hemisphere_image_url =[]

    for article in articles:
        image = article.find('img')['src']
        image_url = ('https://astrogeology.usgs.gov' + image)
        t = article.find('div', class_='description')
        title = t.find('h3').text
        mars_hemisphere_image_url.append({"title": title, "image_url": image_url})

    mars_hemisphere_image_url


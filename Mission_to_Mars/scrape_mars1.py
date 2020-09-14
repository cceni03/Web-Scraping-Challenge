import os
from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd
import requests
import pymongo
import time

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_url():
    browser = initial_browser()
    mars_dict ={}

    # URL to be scraped
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find_all('div', class_="content_title")
    marslatest_text = news.a.text

    # Mars Image to be Scraped
    jpl_nasa_url = 'https://www.jpl.nasa.gov'
    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    relativeimage_path = soup.find_all('img')[3]["src"]
    featuredimage_url = jpl_nasa_url + relativeimage_path

    # Mars Facts to be Scraped
    mars_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_url)
    mars_df = tables[0]
    mars_df.rename(columns = {0:'Fact Heading', 1:'Fact Data'}, inplace = True)
    mars_df.set_index('Fact Heading', inplace = True)
    mars_df
    mars_html = mars_df.to_html(index=False)
    mars_html

    # Mars Hemisphere to be Scraped
    base_url = "https://astrogeology.usgs.gov/"
    marshemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(marshemisphere_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemisphereimage_list = soup.find_all('div', id='product-section')

    # Mars Hemisphere Images

    





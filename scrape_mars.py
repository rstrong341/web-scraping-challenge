#!/usr/bin/env python
# coding: utf-8



#Import tools
from bs4 import BeautifulSoup
import requests
import pymongo
import os
import time
import pandas as pd

from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    #Executable_path
    executable_path = { "executable_path": ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    title, subheader = mars_news(browser) 

    data = {
     "title": title,
     "subheader": subheader,
     "featured_image": featured_image(browser),
     "facts": mars_facts(),
     "hemispheres": hemispheres(browser)
    }
    browser.quit()
    return data

def mars_news(browser):
    
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve all elements that contain book information
    
    try:
        results = soup.select_one("ul.item_list li.slide")

        results.find('div',class_='content_title')
        title = results.find("div", class_="content_title").get_text()
        subheader = results.find("div", class_="article_teaser_body").get_text()
        print(title)
        print(subheader)
    except:
        return None, None
    
    return title, subheader

def featured_image(browser):
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)
 
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve all elements that contain book information
    
    try:
        images = soup.find("img", class_="headerimage fade-in")
        img = images["src"]
    except:
        None, None
    
    image_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img}'

    return image_url
    
def mars_facts():
    df = pd.read_html('https://space-facts.com/mars/')[0]
    df.columns = ["Description", "Mars"]
    df.set_index("Description", inplace=True)
    
    return df.to_html(classes="table table-striped")
    
def hemispheres(browser):
    # # # Hemisphere 
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)


    urls = []

    # First get a list of all the hemisphere
    links = browser.find_by_css("a.product-item h3")

    for index in range(len(links)):
        hemisphere = {}

        browser.find_by_css("a.product-item h3")[index].click()

        # Next is find the sample image anchor tag and extract the href 
        try: 
            sample_element = browser.links.find_by_text("Sample").first
            title = browser.find_by_css("h2.title").text
            link = sample_element["href"]

            hemisphere["title"] = title
            hemisphere["link"] = link

            urls.append(hemisphere)
            browser.back()
        except:
            return None

        

    return urls



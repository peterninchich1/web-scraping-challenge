import pymongo
import time
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
import numpy as np

def app_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

def scrape():

    browser = app_browser()
    data = {}
    
    # Title and Paragraph Analysis
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    list = soup.find('div', class_='four-grid')
    first = list.find('div', class_='row')
    headline = first.find('div', class_='row-link').text
    paragraph = first.find('div', class_='article_teaser_body').text
    data["headline"] = headline
    data["paragraph"] = paragraph

    #Image Analysis
    url_2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_2)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    path = "https://www.jpl.nasa.gov/spaceimages/images/wallpaper/PIA23488-640x350.jpg"
    data["image_analysisfeatured_image_url"] = path

    # Twitter Analysis
    url_3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_3)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    tweet = soup.find('ol', class_='stream-items')
    mars_weather = tweet.find('p', class_="tweet-text").text
    data["twitter"] = mars_weather
 
    #Mars Facts in Pandas Dataframe
    url_4 = "https://space-facts.com/mars/"
    facts_table = pd.read_html(url_4)
    facts_table = facts_table[1]
    facts_table.columns = ["Stat","Value"]
    facts_table

    #Convert Mars Facts Pandas Dataframe to HTML
    facts_html = facts_table.to_html()
    facts_html = facts_html.replace("\n","")
    data["facts"] = facts_html

    #Mars Hemispheres
    url_5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_5)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_all = []

    searches = soup.find("div", class_ = "result-list" )
    hemispheres = searches.find_all("div", class_="item")

    for hemisphere in hemispheres:
        heading = hemisphere.find("h3").text
        heading = heading.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_all.append({"title": title, "img_url": image_url})
    data['hemisphere'] = mars_all

    browser.quit()

    return data
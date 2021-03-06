#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time

from pprint import pprint

def scrape():

    #Set up browser
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #Initialize dictionary for all scraped data
    mars_data = {}


    #Browse to Mars News web page
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(3)

    #Find the news headlines and paragraphs
    html = browser.html
    soup = bs(html, 'lxml')

    headline = soup.find('div', class_ = 'list_text')

    div = headline.find('div', class_ = 'content_title')
    news_title = div.find('a').text.strip()
    mars_data['news_title'] = news_title
    news_paragraph = headline.find('div', class_ = 'article_teaser_body').text.strip()
    mars_data['news_paragraph'] = news_paragraph


    #Browse to Mars featured image web page
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)
    time.sleep(3)


    #Find the full image
    html = browser.html
    soup = bs(html, 'html.parser')

    browser.links.find_by_partial_text('FULL IMAGE').click()
    featured_image_url = soup.find('div', class_ = 'img').img['src']

    mars_data['featured_image_url'] = 'https://www.jpl.nasa.gov' + featured_image_url


    #Browse to Mars Weather in Twitter
    tweet_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(tweet_url)
    time.sleep(3)


    #Find the tweet about Mars' weather
    html = browser.html
    soup = bs(html, 'html.parser')

    mars_weather = soup.find_all('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')[27].get_text()

    mars_data['mars_weather'] = mars_weather


    #Browse to the Mars Facts web page
    fact_url = 'https://space-facts.com/mars/'

    #Use Pandas to read table
    tables = pd.read_html(fact_url)[0]
    tables.columns = ["description", "value"]
    tables.set_index("description", inplace=True)

    mars_data['table'] = tables.to_html()


    #Browse to the Mars hemispheres full images
    astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(astro_url)
    time.sleep(3)


    #Find the hemisphere links and put into an array
    html_code = []
    links = []
    hemisphere_image_urls = []

    html = browser.html
    soup = bs(html, 'lxml')


    links_div = soup.find('div', class_ = 'collapsible results')
    html_code = links_div.find_all('a')


    for x in html_code:
        if x:
            links.append(x['href'])

    #Find each full image by navigating to the web pages   
    for link in links:
        
        browser.visit('https://astrogeology.usgs.gov' + link) 
        browser.links.find_by_partial_href('open').click()   
            
        html = browser.html
        soup = bs(html, 'lxml')
        
        div = soup.find('div', class_ = 'container')
        image = div.find('img', class_ = 'wide-image')
        image_source = image['src']
        
        div = soup.body.find('div', class_ = 'container')
        title = div.find('h2', class_ = 'title').text.strip()
    
        hemisphere_image_urls.append({'img_url': 'https://astrogeology.usgs.gov' + image_source})
        hemisphere_image_urls.append({'title':title})
        browser.back()
        
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls 

    #Return results
    return mars_data
    


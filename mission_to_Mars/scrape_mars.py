#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Import dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser

from pprint import pprint

def scrape():
    # In[ ]:

    mars_data = {}

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[ ]:


    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)


    # In[ ]:


    #Find the news headlines and paragraphs
    html = browser.html
    soup = bs(html, 'html.parser')



    headlines = soup.find_all('div', class_ = 'list_text')

    for headline in headlines:
        div = headline.find('div', class_ = 'content_title')
        news_title = div.find('a').text.strip()
        news_paragraph = headline.find('div', class_ = 'article_teaser_body').text.strip()
        
        mars_data['news_title'] = news_title
        mars_data['news_paragraph'] = neww_paragraph

    # In[ ]:


    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)


    # In[ ]:


    #Find the full image
    html = browser.html
    soup = bs(html, 'html.parser')

    browser.links.find_by_partial_text('FULL IMAGE').click()
    featured_image_url = soup.find('div', class_ = 'img').img['src']

    mars_data['featured_image'] = featured_image_url


    # In[ ]:


    tweet_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(tweet_url)


    # In[ ]:


    html = browser.html
    soup = bs(html, 'html.parser')

    mars_weather = soup.find('div', class_ = 'css-901oao r-hkyrab r-1qd0xha r-1b43r93 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0').text
    
    mars_data['weather'] = mars_weather    ]


    # In[ ]:


    fact_url = 'https://space-facts.com/mars/'

    tables = pd.read_html(fact_url)
    tables

    mars_weather['fact_table'] = tables

    # In[ ]:


    astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(astro_url)


    # In[ ]:


    html_code = []
    links = []
    hemisphere_image_urls = []

    html = browser.html
    soup = bs(html, 'html.parser')


    links_div = soup.find('div', class_ = 'collapsible results')
    html_code = links_div.find_all('a')


    for x in html_code:
        if x:
            links.append(x['href'])
            

    for link in links:
        
        browser.visit('https://astrogeology.usgs.gov' + link)
        
        browser.links.find_by_partial_href('open').click()
        
        image = soup.find('div', class_ = 'wide-image-wrapper').img['src']
        #div2 = div.find('div', class_= 'wrapper')
        #image = div2.find('img', class_ = 'wide-image')
        
        title = soup.body.find('div', class_ = 'content').h2.text.strip()
        #title = div.find('div', class_ = 'content')
        #title = div3.find('h2', class_ = 'title')
    
        hemisphere_image_urls.append({'img_url': image})
        hemisphere_image_urls.append({'title':title})
        browser.back()
        

    return mars_data  

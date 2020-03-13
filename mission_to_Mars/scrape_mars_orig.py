#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import json

from pprint import pprint

def scrape():

    # In[2]:


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[3]:


    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(3)


    # In[34]:


    mars_data = {}


    # In[6]:


    #Find the news headlines and paragraphs
    html = browser.html
    soup = bs(html, 'lxml')

    headline = soup.find('div', class_ = 'list_text')
    div = headline.find('div', class_ = 'content_title')
    news_title = div.find('a').text.strip()
    pprint('news_title is shown here...........................................')
    pprint(news_title)

    mars_data['news_title'] = news_title

    news_paragraph = headline.find('div', class_ = 'article_teaser_body').text.strip()

    mars_data['news_paragraph'] = news_paragraph


    # In[ ]:


    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)
    time.sleep(3)


    # In[ ]:


    #Find the full image
    html = browser.html
    soup = bs(html, 'html.parser')

    browser.links.find_by_partial_text('FULL IMAGE').click()
    featured_image_url = soup.find('div', class_ = 'img').img['src']

    mars_data['featured_image_url'] = featured_image_url


    # In[ ]:


    tweet_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(tweet_url)
    time.sleep(3)


    # In[ ]:


    html = browser.html
    soup = bs(html, 'lxml')

    # div = soup.find('div', class_ = 'css-1dbjc4n')
    # # pprint(div)
    # div2 = div.find('div', class_ = 'css-901oao r-hkyrab r-1qd0xha r-1blvdjr r-16dba41 r-ad9z0x r-bcqeeo r-19yat4t r-bnwqim r-qvutc0')
    # pprint(div2)
    # mars_weather = div2.find('span', class_ = 'css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0').text
    mars_weather = soup.find_all('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')[0].get_text()
    pprint('span should be printed here >>>>>>')
    pprint(mars_weather)
    mars_data['mars_weather'] = mars_weather


    # In[ ]:


    fact_url = 'https://space-facts.com/mars/'

    tables = pd.read_html(fact_url)[0]
    tables.columns = ["description", "value"]
    tables.set_index("description", inplace=True)
    
    mars_data['table'] = tables.to_html()


    # In[7]:


    astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(astro_url)
    time.sleep(3)


    # In[35]:


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
            

    for link in links:
        
        browser.visit('https://astrogeology.usgs.gov' + link) 
        browser.links.find_by_partial_href('open').click()   
            
        html = browser.html
        soup = bs(html, 'lxml')
        
        div = soup.find('div', class_ = 'container')
        #div2 = div.find('div', id_ = 'wide-image', class_ = 'wide-image-wrapper')
        #div2 = div.find('div', class_= 'wrapper')
        image = div.find('img', class_ = 'wide-image')
        image_source = image['src']
        
        div = soup.body.find('div', class_ = 'container')
        title = div.find('h2', class_ = 'title').text.strip()
        #title = div2.find('h2', class_ = 'block metadata').h2.text.strip()
    
        hemisphere_image_urls.append({'img_url': image_source})
        hemisphere_image_urls.append({'title':title})
        browser.back()
        
    #mars_data = {'hemisphere_image_urls':hemisphere_image_urls}  
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    #Return results
    return mars_data

#!/usr/bin/env python
# coding: utf-8

# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pymongo



# In[51]:


#Configure chrome driver for clicking through pages o/w we could just use requests and get 
#Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False) #** unpacks values and opens browser




# In[68]:


def mars_news():
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html #html source code to parse
    soup = BeautifulSoup(html, "html.parser")
    article_container = soup.find('ul', class_='item_list') #scope down the soup object

    news_date = article_container.find("div", class_="list_date").text
    news_p = article_container.find("div", class_="article_teaser_body").text
    news_title = article_container.find("div", class_="content_title").find('a').text
    
    return news_date, news_p, news_title


# In[82]:


def mars_img():
    
    base_url = 'https://www.jpl.nasa.gov'
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html #html source code to parse
    image_soup = BeautifulSoup(html, "html.parser")

    #METHOD 1: parsing through the style attribute in the article tag
    try:
        img_elem = image_soup.find('article', class_="carousel_item")['style']
        img_rel_url = img_elem.replace("background-image: url('", "")
        img_rel_url = img_rel_url.replace("');", "")
        print(img_rel_url) #relative URL to append to base URL

    except Exception as e:
        print(e)

    #METHOD 2
#     full_img_elem = browser.find_by_id('full_image')[0]
#     full_img_elem.click()

#     html = browser.html #html source code to parse for NEW PAGE
#     image_soup = BeautifulSoup(html, "html.parser")

#     img_rel_url = image_soup.find('img', class_ = "fancybox-image")['src']
#     print(img_rel_url)

    featured_img_url = f'{base_url}{img_rel_url2}'
    return featured_img_url


# In[70]:


def mars_facts():
    url = "https://space-facts.com/mars/"
    browser.visit(url)

    mars_facts_df = pd.read_html(url)
    mars_facts_df = mars_facts_df[0] #pick first table
    mars_facts_df.columns = ['Description', 'Mars']
    mars_facts_html = mars_facts_df.to_html(border = 0, classes = 'table table-striped')

    return mars_facts_html


# In[66]:


url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url)


# In[75]:


def scrape_all():
    #populate variables from functions
    news_date, news_p, news_title = mars_news()
    featured_img_url = mars_img()
    mars_facts_html = mars_facts()

    #assemble document to insert into database
    nasa_document = {
        'news_title': news_title,
        'news_paragraph': news_p,
        'featured_img_url': featured_img_url,
        'mars_facts_html': mars_facts_html
    }

    #consider closing browser here
    return nasa_document


#RUN SCRIPT
#flask can run on multiple threads. main is the primary thread
#run this if a user initiate it to run instead of supporting threads

if __name__ == '__main__':
    scrape_all()

    
    
    


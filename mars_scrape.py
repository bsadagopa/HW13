#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 17:57:45 2018

@author: SKB
"""

# Mission to Mars
## Step 1 - Scraping
### Initializing splinter & Beautiful Soup
import pandas as pd
import datetime as dt
import requests 
import pprint

from splinter import Browser
from bs4 import BeautifulSoup

#-----------------Main Method-scrape()------------------------------------
# Path to chromedriver
#!which chromedriver

### Web Scraping
# hitting mars nasa news site
# Initialize the scrape () function 
# return Python Dictionary 
def scrape():
    executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
    #browser = Browser('chrome')
    browser = Browser('chrome', **executable_path)
    # test browse
    # browser.visit('http://google.com')
    top_title, top_title_news = mars_top_news(browser)
    
    mars_data_dict = {
        "Top_Mars_Title": top_title,
        "Top_Mars_Title_News": top_title_news,
        "Top_Mars_Image": mars_top_image(browser),
        "Mars_Weather": mars_weather(browser),
        "Mars_Facts": mars_facts(),
        "Mars_Hemispheres": mars_hemispheres(browser),
        "As_of_Date":dt.datetime.now()
    }
    
        
    browser.quit()
    return mars_data_dict
#--------------------END Main Method-screape()-----------------------------

#--------------------mars_top_news()---------------------------------------
def mars_top_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    # Convert html to a soup object and then quit the browser
    html = browser.html
    bs = BeautifulSoup(html, 'html.parser')
    
    slide_elem = bs.select_one('ul.item_list li.slide')
    slide_elem.find("div", class_='content_title')
    
    # Use the parent element to find the first a tag 
    try:
        top_title = slide_elem.find("div", class_='content_title').get_text()
        print(f"Mars Top News Title: {top_title}")
        
        # Use the parent element to find the paragraph text
        top_title_news = slide_elem.find('div', class_="article_teaser_body").get_text()
        print(f"Mars Top News : {top_title_news}")
    except AttributeError:
        print(f"mars_top_news::Exception Occured, {AttributeError}")
        return None, None
    
    
    return top_title, top_title_news   
   
#----------------------END mars_top_news()---------------------------------   

#----------------------mars_top_image()------------------------------------
# JPL Space Images Featured Image
# Visit the url for JPL's Featured Space Image here.
# Use splinter to navigate the site and find the image url for the current Featured Mars Image and 
# assign the url string to a variable called featured_image_url.
# Make sure to find the image url to the full size .jpg image.
# Make sure to save a complete url string for this image
# hit for pics
def mars_top_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()
    
    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()
    
    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    
    # find the relative image url
    try:
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
        print(f"{img_url_rel}")
    except AttributeError:
        print(f"mars_top_image::Exception Occured, {AttributeError}")
        return None
    
    # Use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
        
    return img_url 
#------------------------END mars_top_image()-------------------------------

#------------------------mars_weather()-------------------------------------

def mars_weather(browser):
    ### Mars Weather

    ###### Visit the Mars Weather twitter account here and scrape the 
    ###### latest Mars weather tweet from the page. 
    ###### Save the tweet text for the weather report as a variable called mars_weather.
    # URL of the page to be scraped
    Mars_Twitter_URL = 'https://twitter.com/marswxreport?lang=en'
    # Initiate the splinter browser function to visit the Mars Twitter URL
    browser.visit(Mars_Twitter_URL)
    
    # Creating a simple for loop to scrape the first tweet
    for text in browser.find_by_css('.tweet-text'): # Searching for all the tweets
        if text.text.partition(' ')[0] == 'Sol': # Selecting the 'first' tweet in the web page
            marsWeather = text.text # storing the tweet in a variable
            break
    print(marsWeather) # printing the text format of the tweet
    
    return marsWeather
#------------------------END mars_weather()---------------------------------

#------------------------mars_facts()-------------------------------
### Mars Facts
##### Visit the Mars Facts webpage here and 
##### use Pandas to scrape the table containing facts 
##### about the planet including Diameter, Mass, etc.
# URL of the page to be scraped
def mars_facts():
    
    Mars_Facts_URL = 'http://space-facts.com/mars/'
    # Creating Dataframe with the read HTML functionality
    try:
        mars_df =  pd.read_html (Mars_Facts_URL, attrs = {'id': 'tablepress-mars'})[0]
    except:
        print(f"mars_facts::Exception Occured, {AttributeError}")
        return None
    # Renaming the columns of the dataframe 
    mars_df.columns = ['Measurements', 'Values']
    mars_df = mars_df.set_index('Measurements') # Changing the index to Measurements
    # Displaying the dataframe
    print(mars_df)
    # Converting our Dataframe to HTML table string using .to_html() feature
    mars_facts_HTML_table_string = mars_df.to_html()
    # printing the table string for verfications
    pprint.pprint(mars_facts_HTML_table_string) 
    
    return mars_facts_HTML_table_string
#------------------------END mars_weather()-------------------------------

#------------------------mars_hemispheres()-------------------------------
### Mars Hemispheres
#Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.

#You will need to click each of the links to the hemispheres in order 
# to find the image url to the full resolution image.

# Save both the image url string for the full resolution hemipshere image, 
# and the Hemisphere title containing the hemisphere name. 
# Use a Python dictionary to store the data using the keys img_url and title.

# Append the dictionary with the image url string and 
# the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
# Store the URL in a variable
def mars_hemispheres(browser):
    mars_astro_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    
    #Initiate the splinter browser function to visit the Mars Astro URL
    browser.visit(mars_astro_url)
    astro_response = requests.get(mars_astro_url) # Storing the response variable, Retrieve page with the requests module
    
    #Create BeautifulSoup object; parse with 'HTML'
    astro_bs = BeautifulSoup(astro_response.text, 'html.parser') # Storing the beautiful soup variable for parsing our HTML
    
    # Retrieve the parent div tags (<a> </a>) for all articles
    hemispheres_list = astro_bs.find_all('a', class_="itemLink product-item") # find all the <a> </a> elements
    # print (Hemispheres_List) # print the list just for verifications
    # Initialize array to store all the results - this will be an array of dictionaries
    hemisphere_image_urls = []
    
    # Loop through results to retrieve article image URL and Title
    
    for image in hemispheres_list: # start the for loop, hemispheres_list was defined in the prior cell above
        image_title = image.find('h3').text # Image titles are in <h3> </h3> tags, found via inspecting the page
        image_link = "https://astrogeology.usgs.gov/" + image['href'] # appending the image link with leading URL and <href> tags
        
        # This function will request the links to be clicked to in order to find the image url to the full resolution image.
        image_request = requests.get(image_link) 
        # Storing the beautiful soup variable for parsing our HTML as we go to a new page
        soup = BeautifulSoup(image_request.text, 'html.parser')
        # Storing image tag variable by finding div in class 'downloads' -> this is found by inspecting the image URL
        image_tag = soup.find('div', class_='downloads')
        # Storing image URL variable loacated in <a> href </a> portion -> this is found by inspecting the image URL
        image_url = image_tag.find('a')['href']
        # Appending all the information in our array of dictionaries, as asked for in the homework    
        hemisphere_image_urls.append({"Title": image_title, "Image_URL": image_url})
        
    # Printing the dictionary
    pprint.pprint(hemisphere_image_urls)
    
    return hemisphere_image_urls
#------------------------END mars_hemisphere()-------------------------------

if __name__ == "__main__":
    print(scrape())
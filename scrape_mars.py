# import dependencies 
from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser
import time

#%%
#browser function
def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

#%%
#scrape function 
def scrape():
    browser = init_browser()
    mars_dict = {}
    
    # NASA News Website Scraping
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    paragraph = soup.find("div", class_="article_teaser_body").text
    title = soup.find("div", class_="content_title").text
    print("Title:",title)
    print("-------")
    print("Paragraph:",paragraph)
    
    # JPL Featured Mars Image 
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html_image = browser.html
    soup = BeautifulSoup(html_image, "html.parser")
    image = soup.find("img")
    src = image.get("src")
    featured_image_url = image_url + src
    print(featured_image_url)

    # Scrape Mars Twitter Account for latest weather report
    weather_url = "https://twitter.com/marswxreport"
    browser.visit(weather_url)
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    tweet = soup.find_all("span", class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
    for i in range(0,len(tweet)):
        try:
            if "InSight sol" in tweet[i].text:
                top_tweet = tweet[i].text
                break
        except:
            pass
    print(top_tweet)

    # Scrape Mars Facts and convert them to a table 
    facts_url = "https://space-facts.com/mars/"
    facts = pd.read_html(facts_url)
    facts_df = facts[0]
    facts_df.columns = ["Fact", "Value"]
    facts_df.set_index(["Fact"])
    facts_df.head(10)
    html_facts = facts_df.to_html()
    print(html_facts)
    
    # Scrape Mars' hemispheres images and URLs
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemisphere_list=[]
    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        hemispheres = soup.find("img", class_="wide-image")["src"]
        title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ hemispheres
        dictionary={"title":title,"img_url":img_url}
        hemisphere_list.append(dictionary)
        browser.back()
    print(hemisphere_list)

    return(mars_dict)
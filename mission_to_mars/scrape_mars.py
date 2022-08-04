# Automated browser actions
from splinter import Browser

# Parses the HTML
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

# For scraping with Chrome
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

     # Create a empty dictionary to store the data
    mars_data = {}

#####################################################################
    # The url we want to scrape
    url_news = 'https://redplanetscience.com'    
     
    # Call visit on our browser and pass the url we want to scrape
    browser.visit(url_news)
    
   # 1 second time delay for error purposes    
    time.sleep(1)

    # Scrape page into soup and create a soup object from the html
    html = browser.html
    soup = bs(html, "html.parser")

    # Scrape for Title and Paragraph Text
    title = soup.find_all('div', class_='content_title')[0].text
    paragraph = soup.find_all('div', class_='article_teaser_body')[0].text


#####################################################################    
    # The url we want to scrape
    url_image = 'https://spaceimages-mars.com/'
    
    # Call visit on our browser and pass the url we want to scrape
    browser.visit(url_image)
    
    # 1 second time delay for error purposes    
    time.sleep(1)   

    # Scrape page into soup and create a soup object from the html
    html = browser.html
    images_soup = bs(html, "html.parser")
   
    # Scrape the Featured Mars Image
    relative_image_path = images_soup.find_all('img')[0]["src"]
    featured_image_url = url_image + relative_image_path
    
    
 #####################################################################   
    # The url we want to scrape
    url_facts = 'https://galaxyfacts-mars.com'
    
    # Use Panda's `read_html` to parse the url and scrape all tabular data from page
    tables = pd.read_html(url_facts)

    # Scrape the table containing facts about Mars
    mars_facts_df = tables[1]
   

    # Rename columns and reset index to match example
    mars_facts_df.columns = ["Description", "Value"]
    mars_facts_df.set_index('Description', inplace=True)
    # Use Pandas to convert the data to a HTML table string.
    mars_html= mars_facts_df.to_html()

#####################################################################
    # The url we want to scrape
    url_hemi = 'https://marshemispheres.com/'
    
    #Call visit on our browser and pass the url we want to scrape
    browser.visit(url_hemi)
    # 1 second time delay for error purposes    
    time.sleep(1)

    # Scrape page into soup and create a soup object from the html
    html = browser.html
    soup = bs(html, "html.parser")
    
    # Scrape the Mars Hemispheres Site
    results = soup.find_all('div', class_='item')

    # Create empty list for hemisphere title and image results
    hemisphere_image_urls=[]

    # Retrieve each list item
    
    for result in results:
        title = result.find('h3').get_text()
        img_url = result.find('img', class_='thumb')['src']
        img_url = url_hemi + img_url
        hemisphere_image_urls.append({'title': title,'img_url':img_url})


#####################################################################
    # Save all the above data in the empty dict
    mars_data = {'title': title,
    'paragraph': paragraph,
    'featured_image': featured_image_url,
    'mars_table': mars_html,
    'hemisphere_images': hemisphere_image_urls
    }
#####################################################################
    # Quit the browser
    browser.quit()
    return mars_data
# # Mission to Mars Multiple Web Scrapes - Refactored Again - Connect the Code to the Database
# reference https://courses.bootcampspot.com/courses/676/pages/10-dot-5-2-update-the-code?module_item_id=190951

#Import Dependencies: Splinter, BeautifulSoup, and Pandas
import pandas as pd
import datetime as dt
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

#######################################################################################################################################
# Code Updated Here at the top to Connect to Database

def scrape_all():

    # Set up the Splinter - initiate headless driver for deployment to not see the code in action opening sites to scrape 
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

#######################################################################################################################################
# ## Scrape Mars News (NASA) - 1 of 3
# reference: https://courses.bootcampspot.com/courses/676/pages/10-dot-3-3-scrape-mars-data-the-news?module_item_id=190909

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    # Return the function mars_news()
    return news_title, news_p

##########################################################################################################################################
# ## Scrape Mars Featured Images (JPL) - 2 of 3
# reference: https://courses.bootcampspot.com/courses/676/pages/10-dot-3-4-scrape-mars-data-featured-image?module_item_id=190916

def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button. Index [0] = 1st button, [1] = 2nd, [2] = 3rd
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url. 
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    # Return the function featured_image()
    return img_url

##########################################################################################################################################
# ## Mars Facts - 3 of 3
# reference: https://courses.bootcampspot.com/courses/676/pages/10-dot-3-5-scrape-mars-data-mars-facts?module_item_id=190922

def mars_facts(browser):

    try:
        #Use 'read_html' to scrape the facts table into a dataframe  
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    #Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

#########################################################################################################################################
#This last block of code tells Flask that our script is complete and ready for action. 
# The print statement will print out the results of our scraping to our terminal after executing the code.

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


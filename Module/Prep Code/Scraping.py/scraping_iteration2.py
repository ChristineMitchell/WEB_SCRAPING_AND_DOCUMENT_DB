# # Mission to Mars Multiple Web Scrapes - Refactored - Insert it into a function!
# reference https://courses.bootcampspot.com/courses/676/pages/10-dot-5-2-update-the-code?module_item_id=190951


#Import Dependencies: Splinter, BeautifulSoup, and Pandas
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

#Set up the Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

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

    #Convert our DataFrame back to an HTML-ready code
    return df.to_html()

#End the automated browsing session
browser.quit()


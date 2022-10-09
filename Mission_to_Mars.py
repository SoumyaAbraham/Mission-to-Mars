# Import dependencies:

from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome',  **executable_path, headless= False)

# Visit the website:

url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading page:

browser.is_element_present_by_css('div.list_text', wait_time=1)

# Parse the HTML:

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


### Featured Title

slide_elem.find('div', class_='content_title')

# Use parent element to retreive only the text for title:

news_title = slide_elem.find('div', class_= 'content_title').get_text()
news_title

### Featured Summary
# Get only text for summary:
# While there are 15 instances of "article_teaser_body", since we only want 
# the most recent one (), which is always at the top, we can still use it since
# the top-most news is the most recent:

news_p = slide_elem.find('div', class_= 'article_teaser_body').get_text()
news_p

### Featured Image

# Visit the website:

url = 'https://spaceimages-mars.com/'
browser.visit(url)

# Get image:

full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup:

html = browser.html
img_soup = soup(html, 'html.parser')

# Find the realtive image url:
# We want to make sure we don't use the href for only the first image. We want
# to get all the images.

image_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
image_url_rel

# Use base URL to create an absolute URL:

img_url = f'https://spaceimages-mars.com/{image_url_rel}'
img_url

### Adding facts about Mars (as a table)

df= pd.read_html('https://galaxyfacts-mars.com/')[0]
df.columns = ['description', 'Mars', 'Earth']
df.set_index('description', inplace = True)
df

df.to_html()

browser.quit()
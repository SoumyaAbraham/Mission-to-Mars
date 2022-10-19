from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver

    executable_path = {'executable_path': ChromeDriveManager().install()}
    browser=Browser('chrome', executable_path="chromedriver", headless = True)

    news_title, news_paragraph = mars_news(browser)

# Run all scraping fns and sore results in dictionary

    data= {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser), 
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser), 
        "last_modified": dt.datetime.now()

    }

    # Stop webdriver and return data

    browser.quit()
    return data

def mars_news(browser):

    # Visit the Mars NASA news site:

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page

    browser.is_element_present_by_css("ul.item_list li.slide", wait_time =1)

    # Convert the browser html to a soup object and then quit the browser

    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except fro error handling

    try: 
        slide_elem = news_soup.select_one('ul.item_li.slide')

        # USe the parent element to find the first 'a' tags in the news title
        news_title = slide_elem.find("div", class_= "content_title").get_text()

        # Use the parent element to find the paragraph text
        news_p =  slide_elem.find('div', class_ = 'article_teaser_body').get_text()

    except AttributeError:
            return None, None
    
    return news_title, news_p

    ## JPL Space Images Featured Image

def featured_image(browser):

    # Visit URL

    url =  'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button

    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting HTML with soup

    html = browser.html
    img_soup= soup(html, 'html.parser')

    # Add try/except for error handling

    try: 

        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL

    img_url=  f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    return img_url

## Mars Facts

def mars_facts():
    #Add try/except for error handling

    try: 
        df= pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns = ['Description', 'Mars']
    df.set_index('Description', inplace= 'True')

    # Convert df into HTML format, add bootstrap

    return df.to_html(classes= "table table-striped")

def hemispheres(browser):

    # Visit URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Parse the resulting HTML with soup
    hemi_soup = browser.html
    hemi_soup = soup(hemi_html, 'html.parser')

    # Retrieve all items for hemisphere info:
    items =  hemi_soup.find_all('div', class_ = 'item')

    # Create a list ot hold info

    hemisphere_image_urls= []

    # Retrieve the image and titles from each hemisphere

    main_url=  "https://astrogeology.usgs.gov/"

    # Create a loop to scrape through all the hemispheres
    
    for item in items:
        hemisphere = {}
        titles= item.find('h3').text

        # Create link for full image
        link_ref = item.find('a', class_ = 'itemLink product-item')['href']

        # Use the nase URL to create an absolute URL and browser visit
        browser.visit(main_url + link_ref)

        #Parse the data
        image_html = browser.html
        image_soup = soup (image_html, 'html.parser')
        download = image_soup.find('div', class_= 'downloads')
        img_url = download.find('a')['href']

        print (titles)
        print(img_url)

        # Append the list

        hemisphere ['img_url']=img_url
        hemisphere['title']= titles
        hemisphere_image_urls.append(hemisphere)
        browser.back()

        # Print the list of image urls with titles

    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data

    print(scrape_all())

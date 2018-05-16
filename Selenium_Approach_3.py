
import time
import datetime
import csv
import multiprocessing
import math

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

__all__ = [
    "initialize_driver",
    "run_thru_pages",
    "burney_scraper"
]

def initialize_driver(page, y,m,d, *searchterms, driver_name="Chrome"):
    print(searchterms)
    print(y,m,d)
    options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    name = multiprocessing.current_process().name
    print(name, "initializing driver")
    driver = getattr(webdriver, driver_name)(chrome_options=options)
    driver.implicitly_wait(10)
    driver.get("http://find.galegroup.com/bncn/dispAdvSearch.do?prodId=BBCN&userGroupName=new64731")
    driver.find_element_by_xpath('//*[@id="la_dynamicLimiterField"]/option[3]').click()
    time.sleep(5)
    searchterm_count = 0
    for searchterm in searchterms:
        searchterm_count +=1
        search_field = driver.find_elements_by_css_selector('#inputFieldValue')[searchterm_count]
        search_field.click()
        search_field.send_keys(searchterm)
    select = Select(driver.find_element_by_name('operator(1)'))
    select.select_by_visible_text("Or")
    select = Select(driver.find_element_by_name('operator(2)'))
    select.select_by_visible_text("Or")
    date_buttons = (driver.find_elements_by_xpath('//*[@id="dateMode"]'))
    driver.execute_script("arguments[0].click();", date_buttons[3])

    #value from 1604 - 1804
    year = driver.find_element_by_xpath('//*[@id="year1"]')
    driver.execute_script("arguments[0].click();", year)
    year.find_element_by_xpath("//*[contains(text(), {})]".format(y)).click()

    month = driver.find_element_by_xpath('//*[@id="month1"]')
    driver.execute_script("arguments[0].click();", month)
    month.find_element_by_xpath('//*[contains(text(), {})]'.format(m)).click()

    day = driver.find_element_by_xpath('//*[@id="day1"]')
    driver.execute_script("arguments[0].click();", day)
    day.find_element_by_xpath('//*[contains(text(), {})]'.format(d)).click()

    advanced_search = driver.find_element_by_name("inputFieldValue(0)")
    advanced_search.send_keys(Keys.RETURN)
    print(name, ' initialized')

    #wait for the website to load, then click on "Page"
    print(name, 'waiting for elements to load')

    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="content"]/table[1]/tbody/tr/td[3]/form/table[3]/tbody/tr[1]/td[2]/table/tbody/tr/td[2]/table/tbody/tr/td[2]/a[1]').click()
    time.sleep(5)
    select = Select(driver.find_element_by_xpath('//*[@id="fascimileForm"]/table/tbody/tr/td[5]/font/select'))
    select.select_by_visible_text("100%")
    time.sleep(5)


    page_selector = driver.find_element_by_xpath('//*[@id="currPosTop"]')
    page_selector.click()
    page_selector.clear()
    page_selector.send_keys(page)
    go_button = driver.find_element_by_css_selector('#go')
    driver.execute_script("arguments[0].click();", go_button)


    return driver


def run_thru_pages(page_range, increment, y,m,d, *searchterms):
    name = multiprocessing.current_process().name
    page = page_range + 1
    print(y,m,d)
    driver = initialize_driver(page, y,m,d, *searchterms)
    print(name, ' scanning pages ', page_range, " to ", page_range + increment)
    while page < page_range + increment:
        print(name, 'I am on article : ', page)
        if page != 0:
            if page % 100 == 0:
                print(name, " : Trying to not overload the server")
                time.sleep(60)

        # reset lists
        author = []
        location = []
        date = []
        sources = []
        src_links = []
        article_nm = []
        gale_number = []

        try:
            #retrieve article title
            input_element = driver.find_element_by_xpath('//*[@id="documentTable"]/tbody/tr/td[3]/hits[1]/table/tbody/tr/td/table/tbody/tr[1]/td/span/b[1]/i')
            author_date = input_element.text
            author.append(author_date)

            #retrieve city of origin
            input_element = driver.find_element_by_xpath('//*[@id="documentTable"]/tbody/tr/td[3]/hits[1]/table/tbody/tr/td/table/tbody/tr[1]/td/span').text
            location_date = input_element.split(')')
            dity = location_date[-2].split(' (')
            location.append(dity[-1])

            #retrieve date
            input_element = driver.find_element_by_xpath('//*[@id="documentTable"]/tbody/tr/td[3]/hits[1]/table/tbody/tr/td/table/tbody/tr[1]/td/span').text
            dirty = input_element.split('), ')[1]
            time_of_publishing = dirty.split('.')[0]
            date.append(time_of_publishing)

            #retrieve source of file (mostly burney)
            input_element = driver.find_element_by_xpath('//*[@id="documentTable"]/tbody/tr/td[3]/hits[1]/table/tbody/tr/td/table/tbody/tr[1]/td/span/i')
            sources.append(input_element.text)

            #retrieve img link
            image = driver.find_element_by_id("fascimileImg")
            img_src = image.get_attribute("src")
            src_links.append(img_src)

            #retrieve gale number
            input_element = driver.find_element_by_xpath('//*[@id="documentTable"]/tbody/tr/td[3]/div[2]')
            gale_number.append(input_element.text.split(': ')[1])

            time.sleep(1)
            next_button = driver.find_elements_by_xpath('//img[@src="images/b_next.gif"]')
            page += 1
            print(name, ": Moving onto article {}".format(page))
            next_button[0].click()

            #append information to a list and print it as a new row in the csv
            final_data = zip(*[author,location, date, sources, src_links, gale_number])
            with open('Srcs_Burney_{}_slave.csv'.format(str(filename_date)), 'a') as f:
                writer = csv.writer(f)
                writer.writerows(final_data)
        except:
            time.sleep(60*60)
            driver = initialize_driver(page, y,m,d, *searchterms)



def burney_scraper(Year,Month,Day,*searchterms):
    filename_date = datetime.date.today()
    author = ['origin']
    location = ['location']
    date = ['date']
    sources = ['source']
    src_links = ['image link']
    gale_number = ['gale number']

    #write initial header to a csv file and make it appendable
    final_data = zip(*[author, location, date, sources, src_links, gale_number])
    with open('Srcs_Burney_{}_slave.csv'.format(str(filename_date)), 'a') as f:
            writer = csv.writer(f)
            writer.writerows(final_data)

    slave_names = ["driver{}".format(i+1) for i in range(int(multiprocessing.cpu_count()*3/4))]
    pages = 56500
    increment = math.ceil(pages / (multiprocessing.cpu_count()*3/4))
    print(increment)

    pool = multiprocessing.Pool()
    for i in range(int(multiprocessing.cpu_count()*3/4)):
        url_range = increment * i
        new_process = multiprocessing.Process(name=slave_names[i], target=run_thru_pages, args = (url_range, increment, Year,Month,Day,*searchterms))
        new_process.start()
    pool.close()
    pool.join()

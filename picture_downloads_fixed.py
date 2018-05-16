
from multiprocessing import cpu_count
import multiprocessing
from multiprocessing import Pool
import csv
import math
import urllib.request
import pandas as pd
import os, errno
import time
import socket



# start date 1750
def send_pix(cell_range, increment):
    socket.setdefaulttimeout(9999)
    name = multiprocessing.current_process().name
    starting_pos = cell_range + 1
    page_num = 0
    page = 0
    god_damnit = 0
    iterator = 0
    print('{} scraping from {} to {}'.format(name, starting_pos, starting_pos + increment))
    df = pd.read_csv('Srcs_Burney_02_10_2018_slave3.csv')
    urls = [x for y in df.values.tolist() for x in y]
    links = urls[4::6]
    names = urls[0::6]
    location = urls[1::6]
    date = urls[2::6]
    gale = urls[5::6]
    links1 = links[starting_pos:starting_pos + increment]
    names1 = names[starting_pos:starting_pos + increment]
    location1 = location[starting_pos:starting_pos + increment]
    date1 = date[starting_pos:starting_pos + increment]
    names1 = names[starting_pos:starting_pos + increment]
    for picture in links1:
        if iterator !=0:
            if iterator % 500 == 0:
                print(name, " : Trying to not overload the server")
                time.sleep(60)
        print('{} working on page {} in article {}'.format(name, page, god_damnit))
        try:
            os.makedirs("Articles_names_abolition/{}/{}/{}".format(location1[page_num],names1[page_num], date1[page_num]))
            god_damnit += 1
            page = 1
            print('new article')
            time.sleep(1)
        except OSError as e:
            if e.errno == errno.EEXIST:
                print('same article')
                page +=1
        try:
            urllib.request.urlretrieve(picture, "Articles_names_abolition/{}/{}/{}/{}{}.tiff".format(location1[page_num],names1[page_num], date1[page_num], names1[page_num], page))
        except OSError as x:
            if x.errno == errno.EPROTOTYPE:
                page -=1
                print('that stupid error you could not fix')
                continue

        page_num = page_num + 1
        iterator += 1
        print('progress {}: {}%'.format(name, (page_num/len(names1))*100))

if __name__ == "__main__":
    df = pd.read_csv('Srcs_Burney_02_10_2018_slave3.csv')
    urls = [x for y in df.values.tolist() for x in y]
    links = urls[4::6]
    slave_names = ["driver{}".format(i+1) for i in range(multiprocessing.cpu_count()-6)]
    increment = math.ceil(len(links) / (multiprocessing.cpu_count()-6))
    print(increment)
    pool = multiprocessing.Pool()
    for i in range(multiprocessing.cpu_count()-6):
        cell_range = increment * i
        csv_file_name = "Srcs_Burney_02_10_2018_slave3.csv"
        new_process = multiprocessing.Process(name=slave_names[i], target=send_pix, args = (cell_range, increment))
        new_process.start()
    pool.close()
    pool.join()

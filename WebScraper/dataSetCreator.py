import requests
from bs4 import BeautifulSoup
import csv
import time
import math
import threading
lock = threading.Lock()
count = 1
outfile = open("out.csv", "a")
writer = csv.writer(outfile)
start_time = time.time()
def getData(urls):
    global count
    global writer
    global lock
    global start_time
    for url in urls:
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(page.content, "html.parser")
        gross_worldwide = None
        date = None
        country = None
        language = None
        movie_name = None
        imdb_rating = None
        metascore = None
        popularity = None
        date = None
        runtime = None
        coo = None
        genres = []
        directors = []
        stars = []
        companies = []
        languages = []
        try:
            results = soup.find_all("h1", class_="sc-d8941411-0")
            movie_name = results[0].text
        except: pass
        try:
            results = soup.find_all("span", class_="sc-bde20123-1")
            imdb_rating = results[0].text
        except: pass
        try:
            results = soup.find_all("span", class_="metacritic-score-label")
            metascore = results[0].text
        except: pass
        try:
            results = soup.find_all("div", class_="sc-5f7fb5b4-1")
            popularity = results[0].text
        except: pass
        try:
            results = soup.find_all("div", class_="ipc-chip-list__scroller")[0].find_all("a")
            for result in results:
                genres.append(result.text)
        except: pass
        try:
            results = soup.find_all("span", class_="ipc-metadata-list-item__label")
            for result in results:
                if result.text == "Directors" or result.text == "Director":
                    temp = result.next_sibling.find_all("a")
                    for t in temp:
                        directors.append(t.text)
                    break
        except: pass
        try:
            results = soup.find_all("a", class_="ipc-metadata-list-item__label ipc-metadata-list-item__label--link")
            for result in results:
                if result.text == "Stars" or result.text == "Star":
                    temp = result.next_sibling.find_all("a")
                    for t in temp:
                        stars.append(t.text)
                    break
        except: pass
        try:
            myul = soup.find_all("ul", class_="ipc-metadata-list ipc-metadata-list--dividers-all ipc-metadata-list--base")
            results = myul[1].find_all("li", class_="ipc-metadata-list__item ipc-metadata-list-item--link")
            for result in results:
                txt = result.find("a").text
                if txt == "Release date":
                    date = result.find_all("a")[1].text
                    break
        except: pass
        try:
            results = soup.find_all("span", class_="ipc-metadata-list-item__label")
            for result in results:
                if(result.text == "Gross worldwide"):
                    gross_worldwide = result.next_sibling.text
                    break
        except: pass
        try:
            results = soup.find_all("span", class_="ipc-metadata-list-item__label")
            for result in results:
                if(result.text == "Runtime"):
                    runtime = result.next_sibling.text
                    break
        except: pass
        try:
            results = soup.find_all("a", class_="ipc-metadata-list-item__label ipc-metadata-list-item__label--link")
            for result in results:
                if(result.text == "Production companies"):
                    temp = result.next_sibling.find_all("a")
                    for t in temp:
                        companies.append(t.text)
                    break
        except: pass
        try:
            myul = soup.find_all("ul", class_="ipc-metadata-list ipc-metadata-list--dividers-all ipc-metadata-list--base")
            results = myul[1].find_all("li", class_="ipc-metadata-list__item")
            for result in results:
                txt=result.text
                if("Country of origin" in txt):
                    coo = txt[17:]
                    break
        except: pass
        try:
            results = soup.find_all("li",class_="ipc-metadata-list__item")
            for result in results:
                if "data-testid" in result.attrs.keys():
                    if result.attrs["data-testid"] == "title-details-languages":
                        temp = result.find_all("a")
                        for t in temp:
                            languages.append(t.text)
                        break
        except: pass
        lock.acquire()
        count += 1
        end_time = time.time()
        print(f'Processed {count}/{total} movies... Estimated time left : {math.floor((total-count)*(end_time-start_time)/count)//60}m {math.floor((total-count)*(end_time-start_time)/count)%60}s.......', end='\r')
        writer.writerow([movie_name, imdb_rating, metascore, popularity, date, gross_worldwide, runtime, genres, directors, stars, companies, coo, languages])
        lock.release()


with open("data/urls.txt", "r") as f:
    start_time = time.time()
    lines = f.readlines()
    total = len(lines)
    threads = []
    num_of_threads = int(input("Enter number of threads : "))
    diff = total//num_of_threads
    for i in range(num_of_threads-1):
        l = [x for x in lines[i*diff:(i+1)*diff]]
        t = threading.Thread(target=getData, args = (l,))
        threads.append(t)
        t.start()
    l = [x for x in lines[(num_of_threads-1)*diff:]]
    t = threading.Thread(target=getData, args = (l,))
    threads.append(t)
    t.start()
    for t in threads:
        t.join()
    end_time = time.time()
        # writer.writerow([movie_name, imdb_rating, popularity, date, gross_worldwide, runtime, genres, directors, stars, companies])

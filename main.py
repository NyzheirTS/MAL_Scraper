
from bs4 import BeautifulSoup
import requests
import time
import csv

id = 1



def id_name_Pair():
    global id
    global name
    global data

    # URL to website
    url = f"https://myanimelist.net/anime/{id}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/116.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

    page = requests.get(url, headers=headers)

    # In case of rate limiting
    if page.status_code == 403 | page.status_code == 405:
        time.sleep(600) # 10 mins
        print("WTF DATA LIMIT OMG !!!!!!")
    else:
        soup = BeautifulSoup(page.content, "html.parser")

        soup2 = BeautifulSoup(soup.prettify(), "html.parser")
        try:  # Search for english title first
            if soup2.find(class_='title-english title-inherit'):
                eng_name = soup2.find(class_='title-english title-inherit').get_text().strip()
                print(id, eng_name)
                data = [id, eng_name]
            else:  # If no english title look for generic title
                name = soup2.find(class_='title-name h1_bold_none').get_text().strip()
                print(id, name)
                data = [id, name]
        except:  # Handles 404 errors
            print(id, None)
            data = [id, 'None']
        id += 1

        # Save to csv file.
        with open('MAL_ID_Data.csv', 'a+', newline='', encoding='UTF8') as f:
            write = csv.writer(f)
            write.writerow(data)


anime_limit = 56501
while id <= anime_limit:
    id_name_Pair()
    time.sleep(3)

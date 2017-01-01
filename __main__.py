import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
from time import sleep
import os
import tldextract

user_agent = {'User-agent': 'Mozilla/5.0'}


def scrape_posts(Base_Url):
    links = []
    months = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

    r = requests.get(Base_Url+"archive", headers=user_agent, allow_redirects=False)
    content = r.text
    soup = BeautifulSoup(content, "html.parser")
    years = [time.text for time in soup.find("header", {"class": "year_navigation"}) if len(time.text) > 1]
    print("scraping... \n")
    for year in years:
        for month in months:
            time = month+"/"+year
            print("Scraping posts from ", time, end='\r')
            r = requests.get(Base_Url+"archive/"+year+'/'+month, headers=user_agent, allow_redirects=False)
            content = r.text
            soup = BeautifulSoup(content, "html.parser")
            for link in soup.select('div.post_glass.post_micro_glass'):
                for image in link.findAll('a'):
                    link = image.get('href')
                    if "http" in link:
                        links.append(link)
    return links


def get_pics(thing):
    pics = []
    r = requests.get(thing, headers=user_agent, allow_redirects=False)
    content = r.text
    pattern = re.compile(r'(photo).*')
    soup = BeautifulSoup(content, 'html.parser')
    for info in soup.findAll("div", {'class': pattern}):
        for pic in info.findAll('img'):
            if 'jpg' in pic.get('src'):
                pics.append(pic.get('src'))
    return pics


def download_photos(photo_link, main_url):
    res = requests.get(photo_link)
    domain = tldextract.extract(main_url)
    sub_domain = domain.subdomain
    os.makedirs("Tumblr_pics", exist_ok=True)
    pic_folder = os.path.join("Tumblr_pics", sub_domain)
    os.makedirs(pic_folder, exist_ok=True)
    with open(os.path.join(pic_folder, os.path.basename(photo_link)), "wb") as f:
        for chunk in res.iter_content(100000):
            f.write(chunk)
    f.close()
    print(os.path.basename(photo_link)+" Saved!")


def scrape_tumblr(main_url):
    pics = []
    links = scrape_posts(main_url)
    print("Getting picture's from all posts ")
    for link, i in zip(links, tqdm(range(len(links)))):
        pic = get_pics(link)
        pics.append(pic)
    return pics


def main():
    url = input("\n \n"+"What Tumblr would you like to scrape for photos: ")
    print("Okay! Here we go ")
    pics_links = scrape_tumblr(url)
    print('\n')
    print("Scraping complete!")
    sleep(1)
    print("\n \n"+"What do you want to do with the links? ")
    print("---------------------------------------------------------------------- \n")
    sleep(0.5)
    print("Save links")
    sleep(0.5)
    print("Show all links")
    sleep(0.5)
    print("Download all pictures")
    print('\n')
    choice = input('Enter your choice here: ').lower()
    if "download" in choice:
        print("Okay currently downloading!")
        for link in pics_links:
            for photo in link:
                if photo:
                    download_photos(photo, url)
        print("All photos downloaded!")
    if "show" in choice:
        print("Okay currently printing links!")
        for link in pics_links:
            print(link)
        print("\n All photos links printed!")


if __name__ == "__main__":
    main()











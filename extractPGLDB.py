from sys import argv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import *    #URLの要求
from urllib.parse import *  #URLのパース   
from bs4 import BeautifulSoup   #HTMLの解析
from time import *
import chardet, sys

def open_html(url):
    sleep(1)   #クローリングの礼儀として1秒スリープ
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
    except :
        print("Can't reading HTML. URL : ", url)
        sys.exit()
    #styleなどの情報を削除
    return html

def html_link_getter(pkmn_name, url):
    html = open_html(url)
    #BeautifulSoup(HTML解析モジュール)に読み込み
    try:
        code = chardet.detect(html)
        html = html.decode(code["encoding"])
        soup = BeautifulSoup(html, 'lxml')
    except:
        print("Decode or BeautifulSoup Error")
        sys.exit()
    
    links = soup.select("a")   #aタグ(リンクの取得)
    extract_result = []
    # href属性を取り出し、リンクを絶対パスに変換 --- (※4)
    for i, a in enumerate(links):
        if pkmn_name in a.text:
            href = a.attrs['href']
            url = urljoin("http://pgl-db.net/", href)
            result = [a.text, url]
            print(result)
            extract_result.append(result)
    return extract_result

def open_browser(urlList):
    """Open pages by Browser"""
    if not urlList :
        print("No data")
        sys.exit()
    for url in urlList:
        options = Options()
        options.add_argument('--headless')

        #driver = webdriver.Chrome('/Users/Ryotaro/Desktop/ExtractPkmnData/chromedriver')
        driver = webdriver.Chrome('/Users/Ryotaro/Desktop/ExtractPkmnData/chromedriver', chrome_options=options)
        driver.get(url[1])
    sleep(30)
    driver.close()

def extract_pkmn_data(pkmn_name, format):
    
    """Extract Pokemon battle data"""
    url = "http://pgl-db.net/season-pokemon/?battle="+str(format)
    links_pkmn = html_link_getter(pkmn_name, url)
    open_browser(links_pkmn)

def main():
    """Main Method"""
    #SSL認証
    #ssl._create_default_https_context = ssl._create_unverified_context
    pkmn_name = argv[1]
    #battle format
    battle_formats = ["all", "single", "double", "triple", "rotation", "special", "wcs"]
    for i, format in enumerate(battle_formats):
        if argv[2] == format :
            extract_pkmn_data(pkmn_name, i)
    

if __name__ == '__main__':
    main()


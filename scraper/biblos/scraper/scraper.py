from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from bs4 import BeautifulSoup
from ..article import Article
import platform

# TODO:SINGLETON??

def get_articles_by_person(name):
    
    match platform.system():
        case 'Darwin':
            driver = webdriver.Chrome('./drivers_111/chrome_mac_arm')
        case 'Windows':
            driver = webdriver.Chrome('./drivers_111/chrome_win.exe')
        case 'Linux':
            driver = webdriver.Chrome('./drivers_111/chrome_linux')
    
    try:
        raw_data = ""
        
        driver.get("https://suw.biblos.pk.edu.pl/")
        input_element = driver.find_element("name", "query").send_keys(name)
        submit_button = driver.find_element("xpath", "/html/body/form/table/tbody/tr[3]/td[2]/center/table/tbody/tr[1]/td[2]/input")
        driver.execute_script("arguments[0].click();", submit_button);
        
        # WebDriverWait(driver, 25).until(EC.presence_of_element_located(("xpath", "//*[starts-with(@id, 'resultsDiv']")))
        element = WebDriverWait(driver, 25).until(EC.presence_of_element_located(("xpath", '//*[@id="resultsDiv_16453"]/center/center/table[2]')))

        for row in driver.find_elements('xpath',"//*[starts-with(@id, 'resourceItemTable')]"):
            record = row.get_attribute('innerHTML')
            raw_data+=record
        
        return raw_data
        
    finally:
        driver.delete_all_cookies()
        driver.quit()
        
        
def prettify(value):
    return ' '.join(value.split())

def parse_html_data(articles_html):
    articles_soup = BeautifulSoup(articles_html,'html.parser')
    
    articles = []

    documents = articles_soup.find_all('html')

    for document in documents:
        soup_title = document.find_all('b')[0] 
        soup_authors = document.find_all('a', {'title' : 'Profil w BPP'})
        soup_ext_authors = document.find_all('a', {'title' : 'Pokaż prace tego autora'})
        
        authors = [author.text for author in soup_authors]
        ext_authors = [author.text for author in soup_ext_authors]
        title = prettify(soup_title.text)
            
        try:
            typ = document.find(string=re.compile("Typ:")).find_next('b').text
        except:
            typ = ""
        try:
            series = document.find(string=re.compile("Seria/Czasopismo:")).find_next('b').text
        except:
            series = ""
        try:
            release_date = document.find(string=re.compile("Data wydania:")).find_next('b').text
        except:
            release_date = ""
        try:
            impact = document.find(string=re.compile("Impact Factor:")).find_next('b').text
        except:
            impact = ""
        try:
            mnisw_list = document.find(string=re.compile("Lista MNiSW/MEiN:")).find_next('b').text

        except:
            mnisw_list = ""
        try:
            points = document.find(string=re.compile("Punktacja czasopisma:")).find_next('b').text
        except:
            points = 0
            
               
        art = Article()
        art.add_authors(authors)
        art.add_ext_authors(ext_authors)
        art.add_title(title)
        art.add_typ(typ)
        art.add_points(points)
        art.add_series(series)
        art.add_release_date(release_date)
        art.add_impact(impact)
        art.add_mnisw_list(mnisw_list)
        
        articles.append(art)
                    
    return articles


def extract_data(raw_data):
    articles = []
    
    documents = BeautifulSoup(raw_data, features="html.parser").find_all('tbody')

    for document in documents:
        soup_title = document.find_all('b')[0]    
        soup_authors = document.find_all('a', {'title' : 'Profil w BPP'})
        soup_ext_authors = document.find_all('a', {'title' : 'Pokaż prace tego autora'})
        
        title = prettify(soup_title.text)
        
        authors = [author.text for author in soup_authors]
        ext_authors = [author.text for author in soup_ext_authors]
        if not authors:
            continue
            
        try:
            typ = document.find(string=re.compile("Typ:")).find_next('b').text
        except:
            typ = ""
        try:
            series = document.find(string=re.compile("Seria/Czasopismo:")).find_next('b').text
        except:
            series = ""
        try:
            release_date = document.find(string=re.compile("Data wydania:")).find_next('b').text
        except:
            release_date = ""
        try:
            impact = document.find(string=re.compile("Impact Factor:")).find_next('b').text
        except:
            impact = ""
        try:
            mnisw_list = document.find(string=re.compile("Lista MNiSW/MEiN:")).find_next('b').text
        except:
            mnisw_list = ""
        try:
            points = document.find(string=re.compile("Punktacja czasopisma:")).find_next('b').text
        except:
            points = 0
            
        article = Article()
        article.add_authors(authors)
        article.add_ext_authors(ext_authors)
        article.add_title(title)
        article.add_series(series)
        article.add_typ(typ)
        article.add_points(points)
        article.add_mnisw_list(mnisw_list)
        article.add_impact(impact)
        article.add_release_date(release_date)
        
        articles.append(article)
                    
    return articles
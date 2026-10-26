import requests
from bs4 import BeautifulSoup
from json import dump


def quotes_parser(soup,url):            #Парсинг для цитат
    tags_all=soup.find_all("div", class_="tags")
    tags=[]

    for tags_one in tags_all:
        tags_one_text=[tag.text for tag in tags_one.find_all("a", class_="tag")]
        tags.append(tags_one_text)

    authors=[]
    authors_all=soup.find_all("small", class_="author")
    for author in authors_all:  #знаходимо відносний шлях до кожного автору і збраємо в абсолютний
        author_rel_url=author.find_next("a")["href"]    
        author_request=requests.get(url+author_rel_url)
        author_soup=BeautifulSoup(author_request.text, "lxml")
        authors.append(author_soup.find("h3", class_="author-title").text)
    quotes=[quote.text for quote in soup.find_all("span", class_="text")]
    quotes_json=[{"tags":t, "author": a, "quote": q} for t,a,q in zip(tags, authors, quotes)]
    return(quotes_json)

def quotes(url):        #Переходи на іншу сторнінку та збирання усіх цитат в одн список
    quotes_json=[]
    next_url=url

    while True:
        request = requests.get(next_url)
        soup = BeautifulSoup(request.text, "lxml")
        quotes_json.extend(quotes_parser(soup,url))
        try:
            next=soup.find("li", class_="next").find_next("a")["href"]
            next_url=url+next
        except AttributeError:
            break

    return quotes_json

def authors_parser(soup, cache):        #парсинг авторів
    fullname=soup.find("h3", class_="author-title").text
    born_date=soup.find("span", class_="author-born-date").text
    born_location=soup.find("span", class_="author-born-location").text
    description=soup.find("div", class_="author-description").text.strip() #Для опису робимо максимум 50 символів, заради оптимізації
    author_json={"fullname": fullname,"born_date": born_date, "born_location": born_location, "description": description }

    return author_json

def authors(url):
    authors_json=[]
    author_cache=[]         #Зберігаємо імена авторів, які уже були
    next_url=url
    
    while True:
        request=requests.get(next_url)
        soup=BeautifulSoup(request.text, "lxml")
        authors_all=soup.find_all("small", class_="author")

        for author in authors_all:  #знаходимо відносний шлях до кожного автору і збраємо в абсолютний
            if author.text in author_cache:
                pass
            else:
                author_cache.append(author.text)
                author_rel_url=author.find_next("a")["href"]    
                author_request=requests.get(url+author_rel_url)
                author_soup=BeautifulSoup(author_request.text, "lxml")
                author_json=authors_parser(author_soup, author_cache)
                authors_json.append(author_json)
        try:            #перехід на наступну сторінку
            next=soup.find("li", class_="next").find_next("a")["href"]
            next_url=url+next
        except AttributeError:
            break        

    return(authors_json)

def in_json(filename, data): # Функція для створення json файлу
    with open(filename, "w", encoding="utf-8") as file:
        dump(data, file,ensure_ascii=False, indent=4)



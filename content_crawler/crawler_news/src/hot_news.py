from requests_html import HTMLSession
import mysql.connector
from flask import Flask,Blueprint


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="news"
)

mycursor = mydb.cursor()

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS hot_news ( 
        title VARCHAR(255) PRIMARY KEY,
        link VARCHAR(255),
        image VARCHAR(255),
        description text
    )
""")
 
session = HTMLSession()

#tuoitre
url='https://tuoitre.vn/tin-moi-nhat.htm'
r = session.get(url)
r.html.render(sleep=1,scrolldown=5)
articles = r.html.find('.box-category-item')
newslist = []
for item in articles:
    try:
       newsitem = item.find('a',first=True)
       image =  item.find('img', first=True)
       description = item.find('.box-category-sapo', first=True).text if item.find('.box-category-sapo', first=True) else None  # Lấy mô tả (description) (nếu có)
       
       newsarticle = {
         'title' : newsitem.attrs['title'] if image else None ,
         'link': list(newsitem.absolute_links)[0] if newsitem.absolute_links else None,  
         'image': image.attrs['src'] if image else None , 
         'description': description 
       }
       newslist.append(newsarticle)
    except Exception as e:
        print(f"An error occurred: {e}")

print(newslist)

for news in newslist:
    add_news = ("INSERT IGNORE INTO hot_news "
                "(title, link, image,description) "
                "VALUES (%s, %s, %s, %s)"
              )
    data_news = (news['title'], news['link'], news['image'], news['description'])

    mycursor.execute(add_news, data_news)



#vietnamnet

base_url ='https://vietnamnet.vn/tin-tuc-24h-page' 
pages_to_scrape = 5  
newslist = []

for page_num in range(1, pages_to_scrape + 1):
    url = f'{base_url}{page_num}'
    r = session.get(url)
    r.html.render(sleep=1, scrolldown=5)

    articles = r.html.find('.horizontalPost')

    for item in articles:
        try:
            newsitem = item.find('h3 a', first=True)
            image = item.find('img', first=True)
            description_element = item.find('.horizontalPost__main-desc', first=True)

            description = description_element.text if description_element else None
            newsarticle = {
                'title': newsitem.attrs['title'] if newsitem else None,
                'link': list(newsitem.absolute_links)[0] if (newsitem and newsitem.absolute_links) else None,
                'image': image.attrs['data-srcset'] if (image and 'data-srcset' in image.attrs) else (image.attrs['src'] if image else None),
                'description': description
            }
            newslist.append(newsarticle)
        except Exception as e:
            print(f"An error occurred: {e}")

print(newslist)
for news in newslist:
    add_news = ("INSERT IGNORE INTO hot_news "
                "(title, link, image,description) "
                "VALUES (%s, %s, %s, %s)"
              )
    data_news = (news['title'], news['link'], news['image'], news['description'])

    mycursor.execute(add_news, data_news)



#vnexpress
base_url ='https://vnexpress.net/tin-tuc-24h-p'

pages_to_scrape = 1 

newslist = []
for page_num in range(1, pages_to_scrape + 1):
    url = f'{base_url}{page_num}'
    r = session.get(url)
    r.html.render(sleep=1, scrolldown=5, timeout=10) 

    articles = r.html.find('article')

    for item in articles:
        try:
            newsitem = item.find('h3', first=True)
            picture = item.find('picture', first=True)
            image = picture.find('img', first=True) if picture else None
            description_element = item.find('.description', first=True)

            description = description_element.text if description_element else None

            newsarticle = {
                'title': newsitem.text,
                'link': list(newsitem.absolute_links)[0] if newsitem.absolute_links else None,
                'image': image.attrs['src'] if image else None,
                'description': description
            }
            newslist.append(newsarticle)
        except Exception as e:
            print(f"An error occurred: {e}")

print(newslist)
for news in newslist:
    add_news = ("INSERT IGNORE INTO hot_news "
                "(title, link, image,description) "
                "VALUES (%s, %s, %s, %s)"
              )
    data_news = (news['title'], news['link'], news['image'], news['description'])

    mycursor.execute(add_news, data_news)



#dantri
url = 'https://dantri.com.vn/tin-moi-nhat.htm'
r = session.get(url)
r.html.render(sleep=1,scrolldown=5)
articles = r.html.find('article')
newslist = []
for item in articles:
    try:
       newsitem = item.find('h3 a',first=True)
       image =  item.find('img', first=True)
       description = item.find('.article-excerpt', first=True).text if item.find('.article-excerpt', first=True) else None  
       newsarticle = {
         'title' : newsitem.text,
         'link': list(newsitem.absolute_links)[0] if newsitem.absolute_links else None,  
         'image': image.attrs['data-src'] if image else None , 
         'description': description 
       }
       newslist.append(newsarticle)
    except Exception as e:
        print(f"An error occurred: {e}")

print(newslist)
for news in newslist:
    add_news = ("INSERT IGNORE INTO hot_news "
                "(title, link, image,description) "
                "VALUES (%s, %s, %s, %s)"
              )
    data_news = (news['title'], news['link'], news['image'], news['description'])

    mycursor.execute(add_news, data_news)





#kenh14
url ='https://kenh14.vn/xa-hoi/nong-tren-mang.chn'
r = session.get(url)
r.html.render(sleep=1, scrolldown=5)
articles = r.html.find('li.knswli')  
newslist = []
for article in articles:
    try:
        title_element = article.find('h3 a', first=True)  
        image_element = article.find('a.kscliw-ava', first=True)  
        description_element = article.find('.knswli-sapo.sapo-need-trim', first=True)  
        title = title_element.text if title_element else None
        link = title_element.attrs['href'] if title_element and 'href' in title_element.attrs else None
        image = image_element.attrs['data-background-image'] if image_element and 'data-background-image' in image_element.attrs else None
        description = description_element.text if description_element else None
        news_article = {
            'title': title,
            'link': link,
            'image': image,
            'description': description
        }
        newslist.append(news_article)
    except Exception as e:
        print(f"An error occurred: {e}")

print(newslist)
for news in newslist:
    add_news = ("INSERT IGNORE INTO hot_news "
                "(title, link, image,description) "
                "VALUES (%s, %s, %s, %s)"
              )
    data_news = (news['title'], news['link'], news['image'], news['description'])

    mycursor.execute(add_news, data_news)



#genk
url='https://genk.vn/tin-tuc-24h.html'
r = session.get(url)
# r.html.render(sleep=1,scrolldown=5)
r.html.render(sleep=1, scrolldown=5, timeout=20) 
articles = r.html.find('.shownews')

newslist = []
for item in articles:
    try:
       newsitem = item.find('a',first=True)
       image =  item.find('img', first=True)
       description = item.find('.knswli-sapo', first=True).text if item.find('.knswli-sapo', first=True) else None  # Lấy mô tả (description) (nếu có)
       
       newsarticle = {
         'title' : newsitem.text,
         'link': list(newsitem.absolute_links)[0] if newsitem.absolute_links else None,  
         'image': image.attrs['src'] if image else None ,
         'description': description 
       }
       newslist.append(newsarticle)
    except Exception as e:
        print(f"An error occurred: {e}")
print(newslist)

for news in newslist:
    add_news = ("INSERT IGNORE INTO hot_news "
                "(title, link, image,description) "
                "VALUES (%s, %s, %s, %s)"
              )
    data_news = (news['title'], news['link'], news['image'], news['description'])

    mycursor.execute(add_news, data_news)


mydb.commit()

mycursor.close()
mydb.close()

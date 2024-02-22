
from requests_html import HTMLSession
import mysql.connector
from flask import Flask,Blueprint

host = "localhost"
user = "root"
password = ""
database = "news"
port = 3306


mydb = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    port=port
)
mycursor = mydb.cursor()

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS youtube ( 
        title VARCHAR(255) PRIMARY KEY,
        link VARCHAR(255),
        image VARCHAR(255)
    )
""")

session = HTMLSession()
url='https://www.youtube.com/feed/trending'
r = session.get(url)
r.html.render(sleep=1, scrolldown=5, timeout=30) 
articles = r.html.find('.style-scope .ytd-video-renderer')

newslist = []
for item in articles:
    try:
       newsitem = item.find('h3 a ',first=True)
       image =  item.find('img', first=True)
       newsarticle = {
         'title' : newsitem.attrs['title'],
         'link': list(newsitem.absolute_links)[0] if newsitem.absolute_links else None,  
         'image': image.attrs['src'] if image else None 
       }
       newslist.append(newsarticle)
    except Exception as e:
        print(f"An error occurred: {e}")

print(newslist)

for news in newslist:
    add_news = ("INSERT IGNORE INTO youtube "
                "(title, link, image) "
                "VALUES (%s, %s, %s)"
              )
    data_news = (news['title'], news['link'], news['image'])

    mycursor.execute(add_news, data_news)


mydb.commit()

mycursor.close()
mydb.close()


# from requests_html import HTMLSession
# import mysql.connector

# host = "localhost"
# user = "root"
# password = ""
# database = "news"
# port = 3306

# mydb = mysql.connector.connect(
#     host=host,
#     user=user,
#     password=password,
#     database=database,
#     port=port
# )
# mycursor = mydb.cursor()

# mycursor.execute("""
#     CREATE TABLE IF NOT EXISTS youtube ( 
#         title VARCHAR(255) PRIMARY KEY,
#         link VARCHAR(255),
#         image TEXT
#     )
# """)

# session = HTMLSession()
# url = 'https://www.youtube.com/feed/trending'
# r = session.get(url)
# r.html.render(sleep=1, scrolldown=5, timeout=30)
# articles = r.html.find('.style-scope .ytd-video-renderer')

# newslist = []
# for item in articles:
#     try:
#         newsitem = item.find('h3 a', first=True)
#         image = item.find('img', first=True)

#         image_src = None
#         if image:
#             if 'data:image/gif;base64' in image.attrs['src']:
#                 # Xử lý hình ảnh mã hóa base64
#                 image_src = 'base64_image'
#             else:
#                 # Xử lý hình ảnh thông thường
#                 image_src = image.attrs.get('src') or image.attrs.get('data-thumb')

#         newsarticle = {
#             'title': newsitem.attrs['title'],
#             'link': list(newsitem.absolute_links)[0] if newsitem.absolute_links else None,
#             'image': image_src
#         }
#         newslist.append(newsarticle)
#     except Exception as e:
#         print(f"Có lỗi xảy ra: {e}")

# print(newslist)

# for news in newslist:
#     add_news = ("INSERT IGNORE INTO youtube "
#                 "(title, link, image) "
#                 "VALUES (%s, %s, %s)"
#     )
#     data_news = (news['title'], news['link'], news['image'])

#     mycursor.execute(add_news, data_news)

# mydb.commit()

# mycursor.close()
# mydb.close()

from requests_html import HTMLSession
from pymongo import MongoClient
import re
import mysql.connector

host = "localhost"
user = "root"
password = ""
database = "news"
port = 3306

# Kết nối đến MySQL
mydb = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    port=port
)
mycursor = mydb.cursor()

# Tạo bảng nếu chưa tồn tại
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS shazam ( 
        title VARCHAR(255) PRIMARY KEY,
        link text,
        image text,
        artist text
    )
""")

# client = MongoClient('mongodb://localhost:27017/')
# db = client['news']
# collection = db['shazam']

session = HTMLSession()
url='https://www.shazam.com/charts/top-200/vietnam'
r = session.get(url)
r.html.render(sleep=1, scrolldown=5, timeout=20) 
articles = r.html.find('.track ')

newslist = []

for item in articles:
    try:
        newsitem = item.find('a', first=True)
        image = item.find('span.album-art', first=True)
        link = item.find('article', first=True)
        artist = item.find('.artist', first=True)

        # Extracting the image URL correctly from the 'style' attribute
        image_url = None
        if image and 'style' in image.attrs:
            style = image.attrs['style']
            matches = re.search(r'url\("([^"]*)"\)', style)
            if matches:
                image_url = matches.group(1)

        newsarticle = {
            'title': newsitem.text if newsitem else None,
            'link': link.attrs['data-shz-audio-url'] if link and 'data-shz-audio-url' in link.attrs else None,
            'image': image_url,
            'artist': artist.text if artist else None
        }
        newslist.append(newsarticle)
    except Exception as e:
        print(f"An error occurred: {e}")

print(newslist)

for news in newslist:
    add_news = ("INSERT IGNORE INTO shazam "
                "(title, link, image,artist) "
                "VALUES (%s, %s, %s, %s)"
              )
    data_news = (news['title'], news['link'], news['image'], news['artist'])

    mycursor.execute(add_news, data_news)


mydb.commit()



mycursor.close()
mydb.close()


# collection.insert_many(newslist)
# client.close()


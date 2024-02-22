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

# Tạo bảng nếu chưa tồn tại
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS kenh14 ( 
        title VARCHAR(255) PRIMARY KEY,
        link VARCHAR(255),
        image VARCHAR(255),
        description text
    )
""")
 
session = HTMLSession()
# url = 'https://kenh14.vn/'
# url = 'https://kenh14.vn/star/tv-show.chn'
# url = 'https://kenh14.vn/cine/hoa-ngu-han-quoc.chn'
# url ='https://kenh14.vn/musik/hip-hop-neva-die.chn'
# url ='https://kenh14.vn/bf-studio.html'
# url ='https://kenh14.vn/tet-dieu-ky.html'
# url ='https://kenh14.vn/money-z.chn'
# url ='https://kenh14.vn/the-gioi-do-day/di.chn'
# url ='https://kenh14.vn/sport/esports.chn'
#url ='https://kenh14.vn/hoc-duong/ban-tin-46.chn'
# url ='https://kenh14.vn/xem-mua-luon/dep.chn'
# url ='https://video.kenh14.vn/new.chn'
url ='https://kenh14.vn/koc-vietnam-2023.html'
r = session.get(url)
r.html.render(sleep=1, scrolldown=5)


articles = r.html.find('li.knswli')  # Tìm tất cả các mục tin tức

newslist = []
for article in articles:
    try:
        title_element = article.find('h3 a', first=True)  # Trích xuất tiêu đề và link
        image_element = article.find('a.kscliw-ava', first=True)  # Trích xuất ảnh
        description_element = article.find('.knswli-sapo.sapo-need-trim', first=True)  # Trích xuất mô tả

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
    add_news = ("INSERT IGNORE INTO kenh14 "
                "(title, link, image,description) "
                "VALUES (%s, %s, %s, %s)"
              )
    data_news = (news['title'], news['link'], news['image'], news['description'])

    mycursor.execute(add_news, data_news)


mydb.commit()

mycursor.close()
mydb.close()
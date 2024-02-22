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
    CREATE TABLE IF NOT EXISTS zing ( 
        title VARCHAR(255) PRIMARY KEY,
        link VARCHAR(255),
        image VARCHAR(255),
        description text
    )
""")

session = HTMLSession()
url = 'https://znews.vn/cpi-nam-2023-tang-3-25-post1451653.html'
r = session.get(url)
r.html.render(sleep=1,scrolldown=5)

articles = r.html.find('article')


newslist = []
for item in articles:
    try:
       newsitem = item.find('.article-title a', first=True)
       image =  item.find('img', first=True)
       description_element = item.find('.article-summary', first=True)  
       description = description_element.text if description_element else None
       newsarticle = {
         'title': newsitem.text,
         'link': list(newsitem.absolute_links)[0] if newsitem.absolute_links else None,
         'image': image.attrs['data-src'] if image and 'data-src' in image.attrs else (image.attrs['src'] if image else None),
         'description': description , # Thêm mô tả vào từng tin tức
       }
       newslist.append(newsarticle)
    except Exception as e:
        print(f"An error occurred: {e}")


print(newslist)

# Lặp qua danh sách tin tức và chèn dữ liệu vào MySQL

# Duyệt qua danh sách tin tức
for news in newslist:
    # Tạo câu lệnh SQL để chèn dữ liệu
    add_news = ("INSERT IGNORE INTO zing "
                "(title, link, image,description) "
                "VALUES (%s, %s, %s, %s)"
              )
    data_news = (news['title'], news['link'], news['image'], news['description'])

    mycursor.execute(add_news, data_news)


mydb.commit()

mycursor.close()
mydb.close()
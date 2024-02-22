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
    CREATE TABLE IF NOT EXISTS dantri ( 
        title VARCHAR(255) PRIMARY KEY,
        link VARCHAR(255),
        image VARCHAR(255),
        description text
    )
""")
 
session = HTMLSession()
# url ='https://dantri.com.vn/xa-hoi/trang-30.htm'
# url ='https://dantri.com.vn/'
url='https://dansinh.dantri.com.vn/'
# url='https://dantri.com.vn/kinh-doanh/thanh-toan-thong-minh.htm'
# url = 'https://dantri.com.vn/bat-dong-san/noi-that.htm'
# url = 'https://dantri.com.vn/the-thao/lich-thi-dau.htm'
# url='https://dantri.com.vn/lao-dong-viec-lam/nhan-luc-moi.htm'
# url = 'https://dantri.com.vn/tam-long-nhan-ai/hoan-canh.htm'
# url = 'https://dantri.com.vn/suc-khoe/ung-thu/video.htm'
r = session.get(url)
r.html.render(sleep=1,scrolldown=5)

articles = r.html.find('article')


newslist = []
for item in articles:
    try:
       newsitem = item.find('h3 a',first=True)
       image =  item.find('img', first=True)
       description = item.find('.article-excerpt', first=True).text if item.find('.article-excerpt', first=True) else None  # Lấy mô tả (description) (nếu có)
       
       newsarticle = {
         'title' : newsitem.text,
         'link': list(newsitem.absolute_links)[0] if newsitem.absolute_links else None,  # Sửa ở đây
         'image': image.attrs['data-src'] if image else None , # Lấy link ảnh (nếu có)
         'description': description 
       }
       newslist.append(newsarticle)
    except Exception as e:
        print(f"An error occurred: {e}")

print(newslist)

for news in newslist:
    add_news = ("INSERT IGNORE INTO dantri "
                "(title, link, image,description) "
                "VALUES (%s, %s, %s, %s)"
               )
    data_news = (news['title'], news['link'], news['image'], news['description'])

    mycursor.execute(add_news, data_news)


mydb.commit()

mycursor.close()
mydb.close()
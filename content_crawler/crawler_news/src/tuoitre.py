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
    CREATE TABLE IF NOT EXISTS tuoitre ( 
        title VARCHAR(255) PRIMARY KEY,
        link VARCHAR(255),
        image VARCHAR(255),
        description text
    )
""")
 
session = HTMLSession()

url='https://tuoitre.vn/'
r = session.get(url)
r.html.render(sleep=1,scrolldown=5)

articles = r.html.find('.box-category-item')

#danh sách sẽ chứa các bài báo sau khi được xử lý
newslist = []
# duyệt qua từng phần tử trong danh sách
for item in articles:
    try:
       newsitem = item.find('a',first=True)
       image =  item.find('img', first=True)
       description = item.find('.box-category-sapo', first=True).text if item.find('.box-category-sapo', first=True) else None  # Lấy mô tả (description) (nếu có)
       
       newsarticle = {
         'title' : newsitem.attrs['title'] if image else None ,
         'link': list(newsitem.absolute_links)[0] if newsitem.absolute_links else None,  # Sửa ở đây
         'image': image.attrs['src'] if image else None , # Lấy link ảnh (nếu có)
         'description': description 
       }
       newslist.append(newsarticle)
    except Exception as e:
        print(f"An error occurred: {e}")

print(newslist)

for news in newslist:
    add_news = ("INSERT IGNORE INTO tuoitre "
                "(title, link, image,description) "
                "VALUES (%s, %s, %s, %s)"
              )
    data_news = (news['title'], news['link'], news['image'], news['description'])

    mycursor.execute(add_news, data_news)


mydb.commit()

mycursor.close()
mydb.close()
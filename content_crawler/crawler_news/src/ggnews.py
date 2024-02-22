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
    CREATE TABLE IF NOT EXISTS ggnews ( 
        title VARCHAR(255) PRIMARY KEY,
        link VARCHAR(255),
        image VARCHAR(255)
    )
""")

# Đoạn code crawl dữ liệu 
session = HTMLSession()
# url = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FuWnBHZ0pXVGlnQVAB?hl=vi&gl=VN&ceid=VN%3Avi'
# url = 'https://news.google.com/topics/CAAqIggKIhxDQkFTRHdvSkwyMHZNREZqY21RMUVnSjJhU2dBUAE?hl=vi&gl=VN&ceid=VN%3Avi' # viet nam
# url = 'https://news.google.com/home?hl=vi&gl=VN&ceid=VN%3Avi'  # home page
# url ='https://news.google.com/topics/CAAqHAgKIhZDQklTQ2pvSWJHOWpZV3hmZGpJb0FBUAE/sections/CAQiTkNCSVNORG9JYkc5allXeGZkakpDRUd4dlkyRnNYM1l5WDNObFkzUnBiMjV5Q2hJSUwyMHZNR2h1TkdoNkNnb0lMMjB2TUdodU5HZ29BQSowCAAqLAgKIiZDQklTRmpvSWJHOWpZV3hmZGpKNkNnb0lMMjB2TUdodU5HZ29BQVABUAE?hl=vi&gl=VN&ceid=VN%3Avi'
# url = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FuWnBHZ0pXVGlnQVAB?hl=vi&gl=VN&ceid=VN%3Avi' #doanh nghiep
# url = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNREpxYW5RU0FuWnBHZ0pXVGlnQVAB?hl=vi&gl=VN&ceid=VN%3Avi'   # giai tri
# url ='https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FuWnBHZ0pXVGlnQVAB?hl=vi&gl=VN&ceid=VN%3Avi'  #the thao
url ='https://news.google.com/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNR1p1Wm1ZU0FuWnBLQUFQAQ?hl=vi&gl=VN&ceid=VN%3Avi'
r = session.get(url)
r.html.render(sleep=1,scrolldown=5)

articles = r.html.find('article')


newslist = []
for item in articles:
    try:
       newsitem = item.find('div',first=True)
       figure = item.find('figure', first=True)  # Lấy thẻ figure đầu tiên trong article
       image = figure.find('img', first=True) if figure else None  # Lấy thẻ img trong figure (nếu có)
       newsarticle = {
         'title' : newsitem.text,
         'link': list(newsitem.absolute_links)[0] if newsitem.absolute_links else None,  # Sửa ở đây
         'image': image.attrs['src'] if image else None  # Lấy link ảnh (nếu có)
       }
       newslist.append(newsarticle)
    except Exception as e:
        print(f"An error occurred: {e}")

print(newslist)

# Lặp qua danh sách tin tức và chèn dữ liệu vào MySQL

# Duyệt qua danh sách tin tức
for news in newslist:
    # Tạo câu lệnh SQL để chèn dữ liệu
    add_news = ("INSERT IGNORE INTO ggnews "
                "(title, link, image) "
                "VALUES (%s, %s, %s)"
                # "ON DUPLICATE KEY UPDATE "
                #  "title = VALUES(title), link = VALUES(link), image = VALUES(image)"
              )
    data_news = (news['title'], news['link'], news['image'])

    # Thực thi câu lệnh SQL
    mycursor.execute(add_news, data_news)

# Đảm bảo rằng dữ liệu được commit vào database
mydb.commit()

# Đóng cursor và kết nối
mycursor.close()
mydb.close()
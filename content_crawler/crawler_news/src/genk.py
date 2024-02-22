from requests_html import HTMLSession
import mysql.connector
from flask import Flask,Blueprint

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
    CREATE TABLE IF NOT EXISTS genk ( 
        title VARCHAR(255) PRIMARY KEY,
        link VARCHAR(255),
        image VARCHAR(255),
        description text
    )
""")

 # Đoạn code crawl dữ liệu 
session = HTMLSession()
url='https://genk.vn/internet.chn'
r = session.get(url)
# r.html.render(sleep=1,scrolldown=5)
# tăng thời gian chạy lên 
r.html.render(sleep=1, scrolldown=5, timeout=20) 
# shownews là tên class một cái thumb bao phủ một bài báo tương đương 1 dòng dữ liệu
articles = r.html.find('.shownews')

newslist = []
for item in articles:
    try:
       newsitem = item.find('a',first=True)
       image =  item.find('img', first=True)
       description = item.find('.knswli-sapo', first=True).text if item.find('.knswli-sapo', first=True) else None  # Lấy mô tả (description) (nếu có)
       
       newsarticle = {
         'title' : newsitem.text,
          # absolute_links dùng để tìm đường link tuyệt đối 
         'link': list(newsitem.absolute_links)[0] if newsitem.absolute_links else None,  
         'image': image.attrs['src'] if image else None ,
         'description': description 
       }
       newslist.append(newsarticle)
    except Exception as e:
        print(f"An error occurred: {e}")

print(newslist)

for news in newslist:
    add_news = ("INSERT IGNORE INTO genk "
                "(title, link, image,description) "
                "VALUES (%s, %s, %s, %s)"
              )
    data_news = (news['title'], news['link'], news['image'], news['description'])

    mycursor.execute(add_news, data_news)


mydb.commit()

# for news in newslist:
#     add_news = ("INSERT IGNORE INTO qa_posts "
#                 "(title, link, image, content, categoryid) "
#                 "VALUES (%s, %s, %s, %s, %s)"
#                 )
#     data_news = (news['title'], news['link'], news['image'], news['content'], '2')

#     mycursor.execute(add_news, data_news)

# mydb.commit()

mycursor.close()
mydb.close()
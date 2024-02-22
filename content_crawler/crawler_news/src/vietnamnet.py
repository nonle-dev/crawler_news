
from requests_html import HTMLSession
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="news"
)

mycursor = mydb.cursor()

# Tạo bảng nếu chưa tồn tại
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS vietnamnet ( 
        title VARCHAR(255) PRIMARY KEY,
        link VARCHAR(255),
        image VARCHAR(255),
        description text
    )
""")
 

session = HTMLSession()

# base_url = 'https://vietnamnet.vn/kinh-doanh-page'  #3830 ==> đã crawl 1100 page
# base_url ='https://vietnamnet.vn/chinh-tri-page' #1030   ==> đã crawl 1030 page
# base_url ='https://vietnamnet.vn/thoi-su-page' #5588   ==> đã crawl 1000 page
# base_url ='https://vietnamnet.vn/the-thao-page' #2800 ==> đã crawl 1000 page
# base_url ='https://vietnamnet.vn/van-hoa-page' #245  ==> đã crawl 245 page
base_url ='https://vietnamnet.vn/giai-tri-page' #3264
# base_url ='https://vietnamnet.vn/the-gioi-page' #3160
# base_url ='https://vietnamnet.vn/doi-song-page' #2603
# base_url ='https://vietnamnet.vn/giao-duc-page' #1764
# base_url = 'https://vietnamnet.vn/suc-khoe-page' #1401
# base_url ='https://vietnamnet.vn/thong-tin-truyen-thong-page' #1900
# base_url ='https://vietnamnet.vn/phap-luat-page' #1440
# base_url ='https://vietnamnet.vn/oto-xe-may-page' #1100
# base_url ='https://vietnamnet.vn/bat-dong-san-page' #881
# base_url ='https://vietnamnet.vn/du-lich-page'  #261
# base_url =''

pages_to_scrape = 2  # Number of pages to scrape


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
    add_news = ("INSERT IGNORE INTO vietnamnet "
                "(title, link, image,description) "
                "VALUES (%s, %s, %s, %s)"
              )
    data_news = (news['title'], news['link'], news['image'], news['description'])

    mycursor.execute(add_news, data_news)


mydb.commit()

mycursor.close()
mydb.close()
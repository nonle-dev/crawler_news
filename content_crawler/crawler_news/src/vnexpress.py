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
    CREATE TABLE IF NOT EXISTS vnexpress ( 
        title VARCHAR(255) PRIMARY KEY,
        link VARCHAR(255),
        image VARCHAR(255),
        description TEXT
    )
""")


session = HTMLSession()

# base_url = 'https://vnexpress.net/bat-dong-san/chinh-sach-p'
# base_url ='https://vnexpress.net/thoi-su-p'
# base_url ='https://vnexpress.net/thoi-su/chinh-tri-p'
# base_url ='https://vnexpress.net/thoi-su/dan-sinh-p'
# base_url ='https://vnexpress.net/thoi-su/lao-dong-viec-lam-p'
# base_url ='https://vnexpress.net/thoi-su/giao-thong-p'
# base_url ='https://vnexpress.net/thoi-su/mekong-p'
# base_url ='https://vnexpress.net/thoi-su/quy-hy-vong-p'
# base_url ='https://vnexpress.net/thoi-su/mekong/dau-tu-p'
# base_url ='https://vnexpress.net/thoi-su/mekong/video-p'
# base_url ='https://vnexpress.net/thoi-su/mekong/nong-nghiep-p'
# base_url ='https://vnexpress.net/thoi-su/mekong/kham-pha-p'
# base_url ='https://vnexpress.net/the-gioi-p'
# base_url ='https://vnexpress.net/the-gioi/tu-lieu-p'
# base_url ='https://vnexpress.net/the-gioi/phan-tich-p'
# base_url ='https://vnexpress.net/the-gioi/nguoi-viet-5-chau-p'
# base_url ='https://vnexpress.net/the-gioi/cuoc-song-do-day-p'
# base_url ='https://vnexpress.net/the-gioi/quan-su-p'
# base_url ='https://vnexpress.net/kinh-doanh-p'
# base_url ='https://vnexpress.net/bat-dong-san-p'
# base_url ='https://vnexpress.net/khoa-hoc-p'
# base_url ='https://vnexpress.net/giai-tri-p'
# base_url ='https://vnexpress.net/the-thao-p'
# base_url ='https://vnexpress.net/phap-luat-p'
# base_url ='https://vnexpress.net/giao-duc-p'
# base_url ='https://vnexpress.net/suc-khoe-p'
# base_url ='https://vnexpress.net/doi-song-p'
# base_url ='https://vnexpress.net/du-lich-p'
# base_url ='https://vnexpress.net/so-hoa-p'
# base_url ='https://vnexpress.net/oto-xe-may-p'
# base_url ='https://vnexpress.net/y-kien-p'
# base_url ='https://vnexpress.net/thu-gian-p'
# base_url ='https://vnexpress.net/tin-tuc-24h-p'
# base_url ='https://vnexpress.net/topic/ha-noi-26482-p'
# base_url ='https://vnexpress.net/topic/tp-ho-chi-minh-26483-p'
# base_url ='https://vnexpress.net/chu-de/spotlight-5504-p'
# base_url ='https://vnexpress.net/chu-de/spotlight-5504-ap'
# base_url ='https://vnexpress.net/anh-p'
# base_url ='https://vnexpress.net/infographics-p'
base_url ='https://vnexpress.net/tin-nong'

pages_to_scrape = 20  # Number of pages to scrape

newslist = []
for page_num in range(1, pages_to_scrape + 1):
    url = f'{base_url}{page_num}'
    r = session.get(url)
    r.html.render(sleep=1, scrolldown=5)

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
# Lặp qua danh sách tin tức và chèn dữ liệu vào MySQL
for news in newslist:
    try:
        add_news = ("INSERT IGNORE INTO vnexpress "
                    "(title, link, image, description) "
                    "VALUES (%s, %s, %s, %s)"
                   )
        data_news = (news['title'], news['link'], news['image'], news['description'])
        mycursor.execute(add_news, data_news)
    except Exception as e:
        print(f"An error occurred while inserting data: {e}")

mydb.commit()

mycursor.close()
mydb.close()

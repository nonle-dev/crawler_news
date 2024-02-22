from requests_html import HTMLSession
import mysql.connector

session = HTMLSession()

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="news"
)

mycursor = mydb.cursor()

# Tạo bảng nếu chưa tồn tại
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS laodong ( 
        title VARCHAR(255) PRIMARY KEY,
        link VARCHAR(255),
        image VARCHAR(255),
        description TEXT,
        time VARCHAR(20),
        authors VARCHAR(50)
    )
""")

# base_url = 'https://laodong.vn/photo?page={}'  # 1011
# base_url ='https://laodong.vn/ban-tin?page={}'  #305
# base_url ='https://laodong.vn/video-xa-hoi?page={}'  #421
# base_url ='https://laodong.vn/video-van-hoa-giai-tri?page={}' #173
# base_url ='https://laodong.vn/video-the-thao?page={}' #14
# base_url ='https://laodong.vn/video-kinh-te?page={}' #45
# base_url ='https://laodong.vn/talkshow?page={}' #18
# base_url ='https://laodong.vn/infographic?page={}' #235
# base_url ='https://laodong.vn/emagazine?page={}' #28
# base_url ='https://laodong.vn/visual-story?page={}' #4
# base_url ='https://laodong.vn/trac-nghiem?page={}' #6
# base_url ='https://laodong.vn/podcast?page={}' #71
# base_url ='https://laodong.vn/gio-thu-9?page={}' #14
# base_url ='https://laodong.vn/podcast-tin-tuc?page={}' #36
# base_url ='https://laodong.vn/podcast-tu-van?page={}' #1
# base_url ='https://laodong.vn/podcast-cau-chuyen?page={}' #11
# base_url ='https://laodong.vn/tin-moi?page={}' #1
# base_url ='https://laodong.vn/moi-truong?page={}' #801
# base_url ='https://laodong.vn/an-ninh-hinh-su?page={}' #168
# base_url ='https://laodong.vn/tu-van-phap-luat?page={}' #323
# base_url ='https://laodong.vn/thi-truong?page={}' #539
# base_url ='https://laodong.vn/doanh-nghiep-doanh-nhan?page={}' #191
# base_url ='https://laodong.vn/dinh-duong-am-thuc?page={}' #348
# base_url ='https://laodong.vn/lam-dep?page={}' #146
# base_url ='https://laodong.vn/cac-loai-benh?page={}' #106
# base_url ='https://laodong.vn/thoi-trang?page={}' #25
base_url ='https://laodong.vn/xu-huong-xe?page={}' #36
# base_url ='https://laodong.vn/lai-xe-an-toan?page={}' #15
# base_url ='https://laodong.vn/sach-hay?page={}' #17
# base_url ='https://laodong.vn/dieu-tra-theo-thu-ban-doc?page={}' #20
# base_url ='https://laodong.vn/giai-dap-phap-luat?page={}' #81
# base_url ='https://laodong.vn/y-kien-ban-doc?page={}' #43
# base_url ='https://laodong.vn/lich-thi-dau?page={}' #149
# base_url ='https://laodong.vn/golf?page={}' #16
# base_url ='https://laodong.vn/tennis?page={}' #48
# base_url ='https://laodong.vn/su-kien-binh-luan?page={}' #401
# base_url ='https://laodong.vn/nha-dep?page={}' #24
# base_url ='https://laodong.vn/quy-hoach?page={}' #38
# base_url ='https://laodong.vn/chinh-sach-giao-duc?page={}' #73
# base_url ='https://laodong.vn/chuyen-nha-minh?page={}' #304
# base_url ='https://laodong.vn/yeu-360?page={}' #74
# base_url ='https://laodong.vn/nuoi-con?page={}' #29
# base_url ='https://laodong.vn/cong-nghe?page={}' #460
# base_url ='https://laodong.vn/the-gioi-so?page={}' #65
# base_url ='https://laodong.vn/vu-khi?page={}' #27
# base_url ='https://laodong.vn/viec-lam?page={}' #68
# base_url ='https://laodong.vn/tu-van-lao-dong' #
# base_url ='https://laodong.vn/tuyen-sinh?page={}' #205
# base_url ='https://laodong.vn/tu-lieu?page={}' #138
# base_url ='https://laodong.vn/cach-lam-hay-tu-co-so?page={}' #41
# base_url ='https://laodong.vn/vi-loi-ich-doan-vien?page={}' #56
# base_url ='https://laodong.vn/van-hoa?page={}' #706
# base_url ='https://laodong.vn/cong-doan-toan-quoc?page={}' #883
# base_url ='https://laodong.vn/xe?page={}' #502
# base_url ='https://laodong.vn/gia-dinh-hon-nhan?page={}' #566
# base_url ='https://laodong.vn/xuat-khau-lao-dong?page={}' #2
# base_url ='https://laodong.vn/tin-tuc-trong-ngay?page={}' #4
# base_url ='https://laodong.vn/viec-tim-nguoi{}' #
# base_url ='https://laodong.vn/tam-long-vang?page={}' #281
# base_url ='https://laodong.vn/tlv-canh-doi?page={}' #72
# base_url ='https://laodong.vn/tlv-cham-lo-cnvc-ld?page={}' #7
# base_url ='https://laodong.vn/tlv-tin-hoat-dong?page={}' #79
# base_url ='https://laodong.vn/tien-te-dau-tu?page={}' #811
# base_url ='https://laodong.vn/bat-dong-san?page={}' #924
# base_url ='https://laodong.vn/giao-thong?page={}' #922
# base_url ='https://laodong.vn/the-gioi?page={}' #2758
# base_url ='https://laodong.vn/the-thao?page={}' #3835
# base_url ='https://laodong.vn/bong-da?page={}' #1250
# base_url ='https://laodong.vn/bong-da-quoc-te?page={}' #1215
# base_url ='https://laodong.vn/giao-duc?page={}' #1686
# base_url ='https://laodong.vn/ban-doc?page={}' #1122
# base_url ='https://laodong.vn/cong-doan?page={}' #3183
# base_url ='https://laodong.vn/giai-tri?page={}' #1553
# base_url ='https://laodong.vn/xa-hoi?page={}' #8385
# base_url ='https://laodong.vn/thoi-su?page={}' #2037
# base_url ='https://laodong.vn/van-hoa-giai-tri?page={}' #2772
# base_url ='https://laodong.vn/phap-luat?page={}' #3243
# base_url ='https://laodong.vn/kinh-doanh?page={}' #3713
# base_url ='https://laodong.vn/suc-khoe?page={}' #1546
# base_url ='https://laodong.vn/y-te?page={}' #1144

def crawl_page(url):
    r = session.get(url)
    r.html.render(sleep=1, scrolldown=5)

    articles = r.html.find('article')

    newslist = []
    for item in articles:
        try:
            newsitem = item.find('h2', first=True)
            image = item.find('img', first=True)
            link = item.find('.link-title', first=True)
            description = item.find('.chappeau', first=True) 
            time=item.find('.time',first=True)
            authors=item.find('.authors',first=True)
            newsarticle = {
                'title': newsitem.text,
                'link': link.attrs['href'] if link else None,
                'image': image.attrs['src'] if image else None,
                'description': description.text if description else None,
                'time': time.text if time else None,
                'authors': authors.text if authors else None
            }
            newslist.append(newsarticle)
        except Exception as e:
            print(f"An error occurred: {e}")

    return newslist

all_news = []
page = 1  # Trang bắt đầu
pages_to_crawl = 191  # Số trang muốn crawl (giới hạn)

while page <= pages_to_crawl:  # Dừng khi đã crawl đủ số trang mong muốn
    url = base_url.format(page)
    news = crawl_page(url)
    if not news:
        break
    all_news.extend(news)
    page += 1

print(all_news)

# Duyệt qua danh sách tin tức
for news in all_news:
    # Tạo câu lệnh SQL để chèn dữ liệu
    add_news = ("INSERT IGNORE INTO laodong"
                "(title, link, image, description,time,authors) "
                "VALUES (%s, %s, %s, %s, %s, %s)"
              )
    data_news = (news['title'], news['link'], news['image'], news['description'], news['time'], news['authors'])

    mycursor.execute(add_news, data_news)

mydb.commit()
mycursor.close()
mydb.close()

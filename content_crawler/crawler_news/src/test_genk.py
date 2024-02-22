import asyncio
from requests_html import AsyncHTMLSession
from pymongo import MongoClient
import pymongo

client = MongoClient('mongodb://localhost:27017/')
db = client['news']
collection = db['testgenk']
collection.create_index([('title', pymongo.ASCENDING)], unique=True)
async def fetch_news(url):
    session = AsyncHTMLSession()
    r = await session.get(url)
    await asyncio.sleep(1)

    await r.html.arender(sleep=1, scrolldown=5, timeout=30) 

    articles = r.html.find('.shownews')

    newslist = []
    for item in articles:
        try:
            newsitem = item.find('h4 a', first=True)
            image = item.find('img', first=True)
            description = item.find('.knswli-sapo', first=True).text if item.find('.knswli-sapo', first=True) else None

            newsarticle = {
                'title': newsitem.text,
                'link': list(newsitem.absolute_links)[0] if newsitem.absolute_links else None,
                'image': image.attrs['src'] if image else None,
                'description': description
            }
            newslist.append(newsarticle)
        except Exception as e:
            print(f"An error occurred: {e}")
    await session.close()
    return newslist

async def main():
    urls = [
        'https://genk.vn/internet.chn',
        'https://genk.vn/internet/media.chn',
        'https://genk.vn/internet/digital-marketing.chn'
        'https://genk.vn/cong-nghe.chn',
        'https://genk.vn/mobile.chn',
        'https://genk.vn/mobile/dien-thoai.chn',
        'https://genk.vn/mobile/may-tinh-bang.chn',
        'https://genk.vn/kham-pha.chn',
        'https://genk.vn/kham-pha/lich-su.chn',

        'https://genk.vn/kham-pha/tri-thuc.chn',
        'https://genk.vn/xem-mua-luon.chn',
        'https://genk.vn/xem-mua-luon/di-dong.chn',
        'https://genk.vn/xem-mua-luon/yeu-bep.chn',
        'https://genk.vn/xem-mua-luon/phu-kien.chn',
        'https://genk.vn/xem-mua-luon/may-tinh.chn',
        'https://genk.vn/thu-thuat.chn'
        # 'https://genk.vn/apps-games.chn',
        # 'https://genk.vn/do-choi-so.chn',
        # 'https://genk.vn/do-choi-so/may-anh.chn',
        # 'https://genk.vn/do-choi-so/nghe-nhin.chn',
        # 'https://genk.vn/do-choi-so/may-tinh.chn',
        # 'https://genk.vn/gia-dung.chn',
        # 'https://genk.vn/song.chn',
        # 'https://genk.vn/nhom-chu-de/emagazine.chn'
    ]
    newslist_combined = []
    tasks = [fetch_news(url) for url in urls]
    for task in tasks:
        newslist_combined.extend(await asyncio.create_task(task))
    print(newslist_combined)
    
    collection.insert_many(newslist_combined)
    client.close()
if __name__ == "__main__":
    asyncio.run(main())

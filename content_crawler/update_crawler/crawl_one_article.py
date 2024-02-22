
import mysql.connector
from requests_html import HTMLSession
import json

def create_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="crawl"
    )

def execute_query(connection, query, data=None, fetch=False):
    cursor = connection.cursor()
    if data:
        cursor.execute(query, data)
    else:
        cursor.execute(query)

    if fetch:
        result = cursor.fetchall()
        cursor.close()
        return result
    
    connection.commit()
    cursor.close()

def crawl_and_save_to_mysql(url):
    connection = create_db_connection()

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS one_url (
        title text,
        link text PRIMARY KEY,
        description TEXT,
        images_json JSON,
        stories_json JSON,
        video text
    )
    '''
    execute_query(connection, create_table_query)

    content_data = crawl_content(url)
    print(f"Crawled Data for {url}: {content_data}")

    save_to_mysql(connection, content_data)
    connection.close()

def crawl_content(url):
    session = HTMLSession()
    r = session.get(url)
    r.html.render(timeout=60, sleep=1, scrolldown=5)

    title_selector = 'h1.title-detail' if "video.vnexpress.net" not in url else 'h1.title'
    description_selector = 'p.description' if "video.vnexpress.net" not in url else 'div.lead_detail'

    selectors = {
        'image': '.fig-picture picture img[src]',
        'image_descriptions': '.Image',
        'story': '.Normal',
        'video': 'div video[src]'
    }

    data = {'title': r.html.find(title_selector, first=True).text if r.html.find(title_selector, first=True) else '',
            'link': url,
            'description': r.html.find(description_selector, first=True).text if r.html.find(description_selector, first=True) else '',
            'images_json': json.dumps({'urls': [img.attrs['src'] for img in r.html.find(selectors['image'])] if r.html.find(selectors['image']) else [],
                                       'image_descriptions': [desc.text for desc in r.html.find(selectors['image_descriptions'])]}, ensure_ascii=False),
            'stories_json': json.dumps([story.text for story in r.html.find(selectors['story'])] if r.html.find(selectors['story']) else [], ensure_ascii=False),
            'video': r.html.find(selectors['video'], first=True).attrs['src'] if r.html.find(selectors['video'], first=True) else ''}

    return data
def save_to_mysql(connection, data):
    try:
        query = '''
        INSERT INTO one_url (title, link, description, images_json, stories_json, video)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        title = VALUES(title),
        description = VALUES(description),
        images_json = VALUES(images_json),
        stories_json = VALUES(stories_json),
        video = VALUES(video)
        '''
        data_tuple = (data['title'], data['link'], data['description'], data['images_json'], data['stories_json'], data['video'])
        execute_query(connection, query, data_tuple)

        print(f"Data inserted successfully into MySQL for {data['link']}")
    except Exception as err:
        print(f"MySQL Error: {err}")

specific_url = 'https://vnexpress.net/de-xuat-phat-hanh-trai-phieu-lam-duong-sat-do-thi-o-ha-noi-va-tp-hcm-4701997.html'
crawl_and_save_to_mysql(specific_url)

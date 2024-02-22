import csv
import json
from requests_html import HTMLSession
import mysql.connector

def create_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="crawl"
    )
connection = create_db_connection()
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

def save_to_txt(data, txt_file_path):
    try:
        with open(txt_file_path, 'a', encoding='utf-8') as txtfile:
            txtfile.write(f"Title: {data['title']}\n")
            txtfile.write(f"Link: {data['link']}\n")
            txtfile.write(f"Description: {data['description']}\n")
            txtfile.write(f"Images JSON: {data['images_json']}\n")
            txtfile.write(f"Stories JSON: {data['stories_json']}\n")
            txtfile.write(f"Video: {data['video']}\n")
            txtfile.write("\n")
            print(f"Data inserted successfully into TXT for {data['link']}")
    except Exception as err:
        print(f"TXT Error: {err}")

def crawl_subpages_to_txt(txt_file_path):
    subpages_urls = [url[0] for url in execute_query(connection, 'SELECT url FROM subpages WHERE check_row = "N"', fetch=True)]
    
    for url in subpages_urls:
        content_data = crawl_content(url)
        print(f"Crawled Data for {url}: {content_data}")
        save_to_txt(content_data, txt_file_path)
        execute_query(connection, 'UPDATE subpages SET check_row = "Y" WHERE url = %s', (url,))

# Đặt đường dẫn của file TXT mà bạn muốn sử dụng
txt_file_path = 'data.txt'

# Thực hiện crawl và lưu dữ liệu vào TXT
crawl_subpages_to_txt(txt_file_path)
connection.close()

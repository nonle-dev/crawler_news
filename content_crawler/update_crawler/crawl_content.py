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
        INSERT INTO content (title, link, description, images_json, stories_json, video)
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

def crawl_subpages_to_mysql():
    connection = create_db_connection()
    execute_query(connection, '''
        CREATE TABLE IF NOT EXISTS content (
            title text,
            link text PRIMARY KEY,
            description TEXT,
            images_json JSON,
            stories_json JSON,
            video text
        )
    ''')

    subpages_urls = [url[0] for url in execute_query(connection, 'SELECT url FROM subpages WHERE check_row = "N"', fetch=True)]
    for url in subpages_urls:
        content_data = crawl_content(url)
        print(f"Crawled Data for {url}: {content_data}")
        save_to_mysql(connection, content_data)
        execute_query(connection, 'UPDATE subpages SET check_row = "Y" WHERE url = %s', (url,))
    connection.close()

crawl_subpages_to_mysql()





# import mysql.connector
# from requests_html import HTMLSession
# import json

# # Function to create a connection to the MySQL database
# def create_db_connection():
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="",
#         database="crawl"
#     )

# # Function to execute a query on the MySQL database
# def execute_query(connection, query, data=None):
#     cursor = connection.cursor()
#     if data:
#         cursor.execute(query, data)
#     else:
#         cursor.execute(query)
#     connection.commit()
#     cursor.close()

# # Function to crawl subpages and save them to MySQL
# def crawl_subpages_to_mysql():
#     # Create a connection to the MySQL database
#     connection = create_db_connection()

#     # Create the 'content' table if it doesn't exist
#     create_table_query = '''
#     CREATE TABLE IF NOT EXISTS content (
#         title text,
#         link text PRIMARY KEY,
#         description TEXT,
#         images_json JSON,
#         stories_json JSON,
#         video text,
#         PRIMARY KEY (link(2000))
#     )
#     '''
#     execute_query(connection, create_table_query)

#     # Select all URLs from the 'subpages' table where check_row is 1
#     select_query = 'SELECT url FROM subpages WHERE check_row = "N"'
#     cursor = connection.cursor()
#     cursor.execute(select_query)
#     subpages_urls = [row[0] for row in cursor.fetchall()]
#     cursor.close()

#     # Crawl and save subpages to MySQL
#     for url in subpages_urls:
#         content_data = crawl_content(url)
#         print(f"Crawled Data for {url}: {content_data}")

#         save_to_mysql(connection, content_data)
       
#         # Update 'check_row' to mark the URL as processed
#         update_query = 'UPDATE subpages SET check_row = "Y" WHERE url = %s'
#         execute_query(connection, update_query, (url,))

#     # Close the database connection
#     connection.close()

# # Function to crawl content from a URL
# def crawl_content(url):
#     session = HTMLSession()
#     r = session.get(url)
#     r.html.render(timeout=60, sleep=1, scrolldown=5)

#     if "video.vnexpress.net" in url:
#         return crawl_video_content(r)

#     title_selector = 'h1.title-detail'
#     description_selector = 'p.description'
#     image_selector = '.fig-picture picture img[src]'
#     image_descriptions_selector = '.Image'
#     story_selector = '.Normal'
#     video_selector = 'div video[src]'

#     title_element = r.html.find(title_selector, first=True)
#     description_element = r.html.find(description_selector, first=True)
#     image_elements = r.html.find(image_selector)
#     image_descriptions_elements = r.html.find(image_descriptions_selector)
#     story_elements = r.html.find(story_selector)
#     video_element = r.html.find(video_selector, first=True)

#     title = title_element.text if title_element else ''
#     description = description_element.text if description_element else ''
#     images = [img.attrs['src'] for img in image_elements] if image_elements else []
#     image_descriptions = [desc.text for desc in image_descriptions_elements]
#     stories = [story.text for story in story_elements] if story_elements else []
#     video = video_element.attrs['src'] if video_element else ''

#     images_json = json.dumps({
#         'urls': images,
#         'image_descriptions': image_descriptions
#     }, ensure_ascii=False)

#     stories_json = json.dumps(stories, ensure_ascii=False)

#     return {
#         'title': title,
#         'link': url,
#         'description': description,
#         'images_json': images_json,
#         'stories_json': stories_json,
#         'video': video
#     }

# # Function to crawl video content from a URL
# def crawl_video_content(r):
#     title_selector = 'h1.title'
#     description_selector = 'div.lead_detail'
#     image_selector = '.fig-picture picture img[src]'
#     image_descriptions_selector = '.Image'
#     story_selector = '.Normal'
#     video_selector = 'div video[src]'

#     title_element = r.html.find(title_selector, first=True)
#     description_element = r.html.find(description_selector, first=True)
#     image_elements = r.html.find(image_selector)
#     image_descriptions_elements = r.html.find(image_descriptions_selector)
#     story_elements = r.html.find(story_selector)
#     video_element = r.html.find(video_selector, first=True)

#     title = title_element.text if title_element else ''
#     description = description_element.text if description_element else ''
#     images = [img.attrs['src'] for img in image_elements] if image_elements else []
#     image_descriptions = [desc.text for desc in image_descriptions_elements]
#     stories = [story.text for story in story_elements] if story_elements else []
#     video = video_element.attrs['src'] if video_element else ''

#     images_json = json.dumps({
#         'urls': images,
#         'image_descriptions': image_descriptions
#     }, ensure_ascii=False)

#     stories_json = json.dumps(stories, ensure_ascii=False)

#     return {
#         'title': title,
#         'link': r.url,
#         'description': description,
#         'images_json': images_json,
#         'stories_json': stories_json,
#         'video': video
#     }
# # Function to save content to MySQL
# def save_to_mysql(connection, data):
#     try:
#         # Insert or update data in 'content' table
#         query = '''
#         INSERT INTO content (title, link, description, images_json, stories_json, video)
#         VALUES (%s, %s, %s, %s, %s, %s)
#         ON DUPLICATE KEY UPDATE
#         title = VALUES(title),
#         description = VALUES(description),
#         images_json = VALUES(images_json),
#         stories_json = VALUES(stories_json),
#         video = VALUES(video)
#         '''
#         data_tuple = (data['title'], data['link'], data['description'], data['images_json'], data['stories_json'], data['video'])
#         execute_query(connection, query, data_tuple)

#         print(f"Data inserted successfully into MySQL for {data['link']}")
#     except Exception as err:
#         print(f"MySQL Error: {err}")

# # Call the crawl and save to MySQL function
# crawl_subpages_to_mysql()



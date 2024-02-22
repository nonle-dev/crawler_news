from requests_html import HTMLSession
import csv
import mysql.connector

def create_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="crawl"
    )

def execute_query(connection, query, data=None):
    cursor = connection.cursor()
    if data:
        cursor.execute(query, data)
    else:
        cursor.execute(query)
    connection.commit()
    cursor.close()

# Function to crawl subpages and save them to MySQL
def crawl_subpages_to_mysql(csv_file, batch_size):
    # Read the URLs from the CSV file
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        subcategories_urls = [row[0] for row in reader]
    connection = create_db_connection()

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS subpages (
        url TEXT,
        check_row VARCHAR(5),
        PRIMARY KEY (url(2000))  
    )
    '''
    execute_query(connection, create_table_query)

    for i in range(0, len(subcategories_urls), batch_size):
        current_batch = subcategories_urls[i:i+batch_size]
        crawl_and_save_to_mysql(current_batch, connection)
    connection.close()

def crawl_and_save_to_mysql(url_batch, connection):
    session = HTMLSession()

    for url in url_batch:
        try:
            r = session.get(url)
            r.html.render(timeout=30, sleep=1, scrolldown=5)
            link_selector = 'h3 > a'
            links = r.html.find(link_selector)

            for link in links:
                subpage_url = link.attrs['href']
                if not subpage_url.startswith("http"):
                    subpage_url = url + subpage_url

                # Use INSERT IGNORE to skip duplicates
                query = "INSERT IGNORE INTO subpages (url, check_row) VALUES (%s, %s)"
                data = (subpage_url, "N")
                execute_query(connection, query, data)
                print(subpage_url)
        except Exception as e:
            print(f"Error crawling {url}: {str(e)}")

input_csv_file = 'subcategories_urls.csv'
batch_size = 10

crawl_subpages_to_mysql(input_csv_file, batch_size)

import requests
from bs4 import BeautifulSoup
import re
from pymongo import MongoClient

max_urls = 1000  

def crawl_emails(url, keyword, max_depth=5):
    urls = [url]
    crawled_urls = set()
    emails = set()

    try:
        for depth in range(max_depth + 1):
            current_urls = urls[:]
            urls = []

            for url in current_urls:
                if url in crawled_urls or len(urls) >= max_urls:
                    continue

                crawled_urls.add(url)
                print(f"Processing {url}")

                try:
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching {url}: {e}")
                    continue

                soup = BeautifulSoup(response.text, 'html.parser')

                new_emails = set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", response.text))
                emails.update(new_emails)

                for anchor in soup.find_all('a', href=True):
                    link = anchor['href']
                    if link.startswith('http') or link.startswith('https'):
                        urls.append(link)

            if not urls:
                break

    except KeyboardInterrupt:
        print("\nCrawling interrupted by user.")

    return emails

def save_to_mongodb(emails, keyword):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['email']
    collection = db['crawled_emails']

    for email in emails:
        existing_email = collection.find_one({'email': email, 'keyword': keyword})

        if existing_email is None:
            data = {
                'email': email,
                'keyword': keyword
            }
            collection.insert_one(data)
            print(f"Inserted email: {email}")
        else:
            print(f"Skipped existing email: {email}")
def main():
    target_url = input("Enter the target URL to crawl: ")

    keyword = input("Enter the keyword: ")

    crawled_emails = crawl_emails(target_url, keyword)

    print("\nCrawled emails related to the keyword:")
    for email in crawled_emails:
        print(email)

    save_to_mongodb(crawled_emails, keyword)

if __name__ == "__main__":
    main()

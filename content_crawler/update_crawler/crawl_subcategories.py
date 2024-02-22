# file crawl url cha

from requests_html import HTMLSession
import csv

def crawl_subcategories(url):
    session = HTMLSession()
    r = session.get(url)
    r.html.render(timeout=30, sleep=1, scrolldown=5)
    subcategories_list = []
    subcategories_elements = r.html.find('.sub > li > a')
    for subcategory_element in subcategories_elements:
        try:
            subcategory_url = subcategory_element.attrs['href']
            subcategories_list.append(subcategory_url)
        except Exception as e:
            print(f"An error occurred: {e}")
    
    # Save URLs to CSV file
    with open('subcategories_urls.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['URL'])
        for url in subcategories_list:
            writer.writerow([url])
    
    return subcategories_list

# Specify the main section URL
web_url = 'https://vnexpress.net'
subcategories = crawl_subcategories(web_url)

# Print the crawled subcategories
for subcategory_url in subcategories:
    print(subcategory_url)

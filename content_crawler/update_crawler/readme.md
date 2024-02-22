
file crawl_subcategories.py ==> crawl các url cha về file subcategories_urls.csv(1)
file url_mysql.py ==> crawl các url con dựa vào file (1) ==> truyền vào bảng subpages
file crawl_content ==> crawl nội dung các bài viết dựa vào bảng subpages ==> truyền vào bảng content
file crawl_url_article.py ==> crawl nội dung 1 bài viết truyền cứng vào để test truyền vào bảng one_url



#tạo database
CREATE DATABASE crawl CHARACTER SET utf8mb4 COLLATE utf8mb4_vietnamese_ci;




#lệnh sửa cột check_row thành giá trị N
UPDATE subpages SET check_row = 'N';

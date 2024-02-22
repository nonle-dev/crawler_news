from flask import Flask, Blueprint, render_template, jsonify, request
from pymongo import MongoClient
from bson import ObjectId  # Thêm thư viện để chuyển đổi ObjectId

ggnews = Blueprint("ggnews", __name__, template_folder='../view/templates')

# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['news']  # Chọn database 'news'
collection = db['genk']  # Chọn collection 'genk'

@ggnews.route('/', methods=['GET'])
def home():
    return render_template('index.html') 

# Route để lấy tất cả dữ liệu
@ggnews.route('/get_genk', methods=['GET'])
def get_genk():
    news = list(collection.find({}))
    # Chuyển đổi ObjectId thành chuỗi
    for news_item in news:
        news_item['_id'] = str(news_item['_id'])
    return jsonify(news)

# Route để lấy dữ liệu theo ID
@ggnews.route('/get_genk_by_id/<id>', methods=['GET'])
def get_genk_by_id(id):
    news = collection.find_one({"_id": ObjectId(id)})  # Chuyển đổi id thành ObjectId
    if news:
        news['_id'] = str(news['_id'])  # Chuyển đổi ObjectId thành chuỗi
        return jsonify(news)
    else:
        return jsonify({"message": "No news found with that id"}), 404
# Route để thêm dữ liệu
@ggnews.route('/add_genk', methods=['POST'])
def add_news():
    try:
        data = request.get_json()
        result = collection.insert_one(data)
        return jsonify({'message': 'Data added successfully', 'inserted_id': str(result.inserted_id)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route để cập nhật dữ liệu
@ggnews.route('/update_genk/<id>', methods=['PUT'])
def update_genk(id):
    try:
        data = request.get_json()
        result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if result.modified_count > 0:
            return jsonify({'message': 'Data updated successfully'})
        else:
            return jsonify({"message": "No news found with that id"}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route để xóa dữ liệu
@ggnews.route('/delete_genk/<id>', methods=['DELETE'])
def delete_genk(id):
    try:
        result = collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count > 0:
            return jsonify({'message': 'Data deleted successfully'})
        else:
            return jsonify({"message": "No news found with that id"}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# # Route để tìm kiếm gần đúng theo title trong MongoDB
   
@ggnews.route('/search_genk', methods=['GET'])
def search_genk():
    try:
        search_query = request.args.get('query')  # Lấy tham số truy vấn từ URL

        # Thực hiện truy vấn MongoDB để tìm kiếm dữ liệu trong collection 'genk' với điều kiện title chứa từ khóa tìm kiếm
        results = collection.find({"title": {"$regex": search_query, "$options": "i"}})

        # Lọc và tạo danh sách kết quả chỉ chứa các trường mong muốn, loại bỏ trường ObjectId
        news_list = []
        for news in results:
            # Loại bỏ trường ObjectId trong mỗi document
            del news['_id']  # Đây là trường ObjectId trong MongoDB
            news_list.append(news)

        if news_list:
            # Trả về danh sách các documents có kết quả tìm kiếm dưới dạng JSON
            return jsonify(news_list)
        else:
            return jsonify({"message": "No matching news found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



# # Kết nối tới MongoDB
# client = MongoClient('mongodb://localhost:27017/')
# db = client['news']  # Chọn database 'news'
# collection = db['dantri']  # Chọn collection 'dantri'

# # Route để lấy tất cả dữ liệu
# @ggnews.route('/get_dantri', methods=['GET'])
# def get_dantri():
#     news = list(collection.find({}))
#     # Chuyển đổi ObjectId thành chuỗi
#     for news_item in news:
#         news_item['_id'] = str(news_item['_id'])
#     return jsonify(news)

# # Route để lấy dữ liệu theo ID
# @ggnews.route('/get_dantri_by_id/<id>', methods=['GET'])
# def get_dantri_by_id(id):
#     news = collection.find_one({"_id": ObjectId(id)})  # Chuyển đổi id thành ObjectId
#     if news:
#         news['_id'] = str(news['_id'])  # Chuyển đổi ObjectId thành chuỗi
#         return jsonify(news)
#     else:
#         return jsonify({"message": "No news found with that id"}), 404
# # Route để thêm dữ liệu
# @ggnews.route('/add_dantri', methods=['POST'])
# def add_dantri():
#     try:
#         data = request.get_json()
#         result = collection.insert_one(data)
#         return jsonify({'message': 'Data added successfully', 'inserted_id': str(result.inserted_id)})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# # Route để cập nhật dữ liệu
# @ggnews.route('/update_dantri/<id>', methods=['PUT'])
# def update_dantri(id):
#     try:
#         data = request.get_json()
#         result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
#         if result.modified_count > 0:
#             return jsonify({'message': 'Data updated successfully'})
#         else:
#             return jsonify({"message": "No news found with that id"}), 404
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# # Route để xóa dữ liệu
# @ggnews.route('/delete_dantri/<id>', methods=['DELETE'])
# def delete_dantri(id):
#     try:
#         result = collection.delete_one({"_id": ObjectId(id)})
#         if result.deleted_count > 0:
#             return jsonify({'message': 'Data deleted successfully'})
#         else:
#             return jsonify({"message": "No news found with that id"}), 404
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# # # Route để tìm kiếm gần đúng theo title trong MongoDB
   
# @ggnews.route('/search_dantri', methods=['GET'])
# def search_dantri():
#     try:
#         search_query = request.args.get('query')  # Lấy tham số truy vấn từ URL

#         # Thực hiện truy vấn MongoDB để tìm kiếm dữ liệu trong collection 'dantri' với điều kiện title chứa từ khóa tìm kiếm
#         results = collection.find({"title": {"$regex": search_query, "$options": "i"}})

#         # Lọc và tạo danh sách kết quả chỉ chứa các trường mong muốn, loại bỏ trường ObjectId
#         news_list = []
#         for news in results:
#             # Loại bỏ trường ObjectId trong mỗi document
#             del news['_id']  # Đây là trường ObjectId trong MongoDB
#             news_list.append(news)

#         if news_list:
#             # Trả về danh sách các documents có kết quả tìm kiếm dưới dạng JSON
#             return jsonify(news_list)
#         else:
#             return jsonify({"message": "No matching news found"}), 404
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app = Flask(__name__)
    app.register_blueprint(ggnews)
    app.run(debug=True)




# from flask import Flask, Blueprint, render_template, jsonify,request
# import mysql.connector

# # ggnews = Blueprint("ggnews", name)
# ggnews = Blueprint("ggnews", __name__, template_folder='../view/templates') 
# # Kết nối cơ sở dữ liệu
# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="",
#     database="tintuc"
# )

# mycursor = mydb.cursor()

# @ggnews.route('/', methods=['GET'])
# def home():
#     return render_template('index.html') 


# @ggnews.route('/get_genk', methods=['GET'])
# def get_genk():
#     mycursor = mydb.cursor(dictionary=True)
#     mycursor.execute("SELECT * FROM genk")
#     news = mycursor.fetchall()
#     mycursor.close()
#     return jsonify(news)

# @ggnews.route('/get_genk_by_id/<int:id>', methods=['GET'])
# def get_genk_by_id(id):
#     try:
#         sql = "SELECT * FROM genk WHERE id = %s"
#         val = (id,)
#         mycursor.execute(sql, val)
#         result = mycursor.fetchone()

#         if result:
#             news = {
#                 'id': result[0],
#                 'title': result[1],
#                 'image': result[2],
#                 'link': result[3],
#                 'description': result[4]
#             }
#             return jsonify(news)
#         else:
#             return jsonify({"message": "No news found with that id"}), 404
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
# # Endpoint để thêm dữ liệu
# @ggnews.route('/add_genk', methods=['POST'])
# def add_news():
#     try:
#         data = request.get_json()
#         title = data['title']
#         image = data['image']
#         link = data['link']
#         description= data['description']

#         sql = "INSERT INTO genk (title, image, link,description) VALUES (%s, %s, %s, %s)"
#         val = (title, image, link,description)
        
#         mycursor.execute(sql, val)
#         mydb.commit()

#         return jsonify({'message': 'Data added successfully'})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# # Endpoint để cập nhật dữ liệu
# @ggnews.route('/update_genk/<int:id>', methods=['PUT'])
# def update_genk(id):
#     try:
#         data = request.get_json()
#         new_title = data['title']
#         new_image = data['image']
#         new_link = data['link']
#         new_description = data['description'] 
#         sql = "UPDATE genk SET title = %s, image = %s, link = %s, description = %s  WHERE id = %s"
#         val = (new_title, new_image, new_link,  new_description,id)
       
#         mycursor.execute(sql, val)
#         mydb.commit()

#         return jsonify({'message': 'Data updated successfully'})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# # Endpoint để xoá dữ liệu
# @ggnews.route('/delete_genk/<int:id>', methods=['DELETE'])
# def delete_genk(id):
#     try:
#         sql = "DELETE FROM genk WHERE id = %s"
#         val = (id,)
       
#         mycursor.execute(sql, val)
#         mydb.commit()

#         return jsonify({'message': 'Data deleted successfully'})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# # Endpoint để tìm kiếm gần đúng theo title
# @ggnews.route('/search_genk', methods=['GET'])
# def search_genk():
#     try:
#         search_query = request.args.get('query')  # Lấy tham số truy vấn từ URL

#         sql = "SELECT * FROM genk WHERE title LIKE %s"
#         val = ("%" + search_query + "%",)

#         mycursor.execute(sql, val)
#         results = mycursor.fetchall()

#         if results:
#             news_list = []
#             for result in results:
#                 news = {
#                     'id': result[0],
#                     'title': result[1],
#                     'image': result[2],
#                     'link': result[3],
#                     'description': result[4]
#                 }
#                 news_list.append(news)
            
#             return jsonify(news_list)
#         else:
#             return jsonify({"message": "No matching news found"}), 404
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app = Flask(__name__)
#     app.register_blueprint(ggnews)
#     app.run(debug=True)


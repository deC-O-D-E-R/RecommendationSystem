from flask import Flask, jsonify, request
from flask_cors import CORS 
from config import Config
from models import db, User, Media
import os
# from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db.init_app(app)

with app.app_context():
  db.create_all()

#   new_user = User(
#     userName = 'BdeioqeofeE',
#     email = 'sefiewjff@gmail.com',
#     phone = '939efnw384',
#     password = 'xdfjyz',
#     age = '23'
#   )
#   db.session.add(new_user)
#   db.session.commit()

@app.route('/')
def index():
  return 'hey'

# @app.route('/api', methods=['GET'])
# def get_data():
#     return jsonify([
#   { "id": 1, "title": "Dune", "type": "movie", "genre": "sci fi", "rating": "5", "img": "" },
#   { "id": 2, "title": "Neuromancer", "type": "novel", "genre": "sci fi", "rating": "5", "img": "" },
#   { "id": 3, "title": "The Witcher 3", "type": "game", "genre": "action", "rating": "5", "img": "" },
#   { "id": 4, "title": "Stranger Things", "type": "tv show", "genre": "sci fi", "rating": "5", "img": "" },
#   { "id": 5, "title": "The Martian", "type": "movie", "genre": "sci fi", "rating": "4", "img": "" },
#   { "id": 6, "title": "Star Wars: Episode IV", "type": "movie", "genre": "sci fi", "rating": "5", "img": "" },
#   { "id": 7, "title": "Altered Carbon", "type": "tv show", "genre": "sci fi", "rating": "4", "img": "" },
#   { "id": 8, "title": "Blade Runner 2049", "type": "movie", "genre": "sci fi", "rating": "4", "img": "" },
#   { "id": 9, "title": "Doom Eternal", "type": "game", "genre": "action", "rating": "5", "img": "" },
#   { "id": 10, "title": "The Hitchhiker's Guide to the Galaxy", "type": "novel", "genre": "sci fi", "rating": "4", "img": "" },
#   { "id": 11, "title": "Inception", "type": "movie", "genre": "sci fi", "rating": "5", "img": "incept" },
#   { "id": 12, "title": "Ready Player One", "type": "movie", "genre": "sci fi", "rating": "4", "img": "" },
#   { "id": 13, "title": "Gravity", "type": "movie", "genre": "sci fi", "rating": "4", "img": "" },
#   { "id": 14, "title": "The Fifth Element", "type": "movie", "genre": "sci fi", "rating": "4", "img": "" },
#   { "id": 15, "title": "Fallout 4", "type": "game", "genre": "action", "rating": "5", "img": "" },
#   { "id": 16, "title": "Black Mirror", "type": "tv show", "genre": "sci fi", "rating": "5", "img": "" },
#   { "id": 17, "title": "Star Trek: The Next Generation", "type": "tv show", "genre": "sci fi", "rating": "4", "img": "" },
#   { "id": 18, "title": "Titanic", "type": "movie", "genre": "romance", "rating": "5", "img": "" },
#   { "id": 19, "title": "Pride and Prejudice", "type": "novel", "genre": "romance", "rating": "4", "img": "" },
#   { "id": 20, "title": "The Notebook", "type": "movie", "genre": "romance", "rating": "5", "img": "" },
#   { "id": 21, "title": "The Office", "type": "tv show", "genre": "comedy", "rating": "5", "img": "" },
#   { "id": 22, "title": "Superbad", "type": "movie", "genre": "comedy", "rating": "4", "img": "" },
#   { "id": 23, "title": "Scott Pilgrim vs. The World", "type": "movie", "genre": "comedy", "rating": "5", "img": "" },
#   { "id": 24, "title": "The Princess Bride", "type": "movie", "genre": "fantasy", "rating": "5", "img": "" },
#   { "id": 25, "title": "Harry Potter and the Sorcerer's Stone", "type": "novel", "genre": "fantasy", "rating": "5", "img": "" },
#   { "id": 26, "title": "The Hobbit", "type": "novel", "genre": "fantasy", "rating": "4", "img": "" }
# ])

@app.route('/api', methods=['GET'])
def get_data():

    media_items = Media.query.all()
    
    media_list = [
        {
            "id": item.id,
            "title": item.title,
            "type": item.type,
            "genre": item.genre,
            "rating": item.rating,
            "img": item.img
        }
        for item in media_items
    ]
    
    return jsonify(media_list)


@app.route('/register', methods=['POST'])
def register():
    data = request.json

    required_fields = ['name', 'email', 'mobile', 'password', 'age']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    new_user = User(
        userName=data.get('name'),
        email=data.get('email'),
        phone=data.get('mobile'),
        # password=generate_password_hash(data.get('password')),
        password = data.get('password'),
        age=data.get('age') 
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Registration successful!"}), 201
    except Exception as e:
        db.session.rollback()  
        print("Error during registration:", e) 
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    print(data)  

    if not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required."}), 400

    user = User.query.filter_by(email=data['email']).first()

    if user and user.password == data['password']:  
        return jsonify({"message": "Login successful"}), 200  
    else:
        return jsonify({"error": "Invalid email or password."}), 401


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=2000)

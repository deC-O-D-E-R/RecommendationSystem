from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    age = db.Column(db.String(3), nullable=False)

    def __repr__(self):
        return f'<User {self.userName}>'

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False)   
    genre = db.Column(db.String(50), nullable=False) 
    rating = db.Column(db.String(10), nullable=False) 
    img = db.Column(db.String(255), nullable=True)    

    def __repr__(self):
        return f'<Media {self.title}>'

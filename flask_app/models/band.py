from flask_app.config.mysqlconnection import connectToMySQL
import re # regex
from flask_app.models import user
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash


class Band:
    db = "band_schema"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.genre = data['genre']
        self.city = data['city']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO bands (name, genre, city, user_id) VALUES (%(name)s, %(genre)s, %(city)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = """SELECT * FROM bands
                JOIN users ON bands.user_id =
                users.id""";
        results = connectToMySQL(cls.db).query_db(query)
        all_bands = []
        for row in results:
            band_row = cls(row)
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            user1 = user.User(user_data)
            band_row.creator = user1
            all_bands.append(band_row)
        return all_bands

    @classmethod
    def get_user_bands(cls,data):
        query = """SELECT * FROM bands
                JOIN users ON bands.user_id =
                users.id
                WHERE bands.user_id = %(id)s""";
        results = connectToMySQL(cls.db).query_db(query,data)
        all_bands = []
        for row in results:
            band_row = cls(row)
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            user1 = user.User(user_data)
            band_row.creator = user1
            all_bands.append(band_row)
        return all_bands

    
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM bands WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls( results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE bands SET name=%(name)s, genre=%(genre)s, city=%(city)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM bands WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validate_bands(band):
        is_valid = True
        if len(band['band_name']) < 2:
            is_valid = False
            flash("name must be at least 2 characters", "bands")
        if len(band['band_genre']) < 2:
            is_valid = False
            flash("genre must be at least 2 characters", "bands")
        if len(band['home_city']) < 3:
            is_valid = False
            flash("city must be at least 2 characters", "bands")
        return is_valid
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL 


class User:
    DB = 'user_author'
    def __init__(self,data):
        self.id = data.get('id')
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')

    @classmethod
    def save (cls, data):
      query = """INSERT into user (first_name, last_name, email, password, created_at, updated_at ) 
    VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(),NOW());"""
      results = connectToMySQL('user_author').query_db(query, data)
      return results 

    @classmethod
    def get_user_by_id(cls, id):
      query = """SELECT id, first_name, last_name, email, password, created_at, updated_at FROM user WHERE id=%(id)s;"""
      results = connectToMySQL('user_author').query_db(query, {"id": id})
      if isinstance(results, bool) or len(results) == 0:
        return None
      return User(results[0])

    @classmethod
    def get_user_by_email (cls, email):
      query = """SELECT id, first_name, last_name, email, password, created_at, updated_at FROM user WHERE email=%(email)s;"""
      results = connectToMySQL('user_author').query_db(query, {"email": email})
      if isinstance(results, bool) or len(results) == 0:
        return None
      return User(results[0])

    @staticmethod
    def hash_password(password):
      return bcrypt.generate_password_hash(password)

    @staticmethod
    def verify_password(user, password):
      return bcrypt.check_password_hash(user.password, password)

    @staticmethod
    def validate(data):
        errors = []


        required_fields = ('first_name', 'last_name', 'email', 'password')
        for required_field in required_fields:
          if required_field not in data:
            errors.append(f"Missing required field '{required_field}'!")

          value = data[required_field]
          if not isinstance(value, str):
            errors.append(f"Expected '{required_field}' to be a string!")


        if len(data["first_name"]) < 2:
          errors.append("First name must contain atleast 2 characters.")

        if len(data["last_name"]) < 2:
          errors.append("Last name must contain atleast 2 characters!")

        if len(data["password"]) < 8:
          errors.append("Password must contain atleast 8 characters.")


        if not data["first_name"].isalpha():
          errors.append("First name must contain only letters.")

        if not data["last_name"].isalpha():
          errors.append("Last name must contain only letters.")


        if User.get_user_by_email(data["email"]) is not None:
          errors.append("User with that email already exists!")

        is_valid = len(errors) == 0
        return is_valid, errors
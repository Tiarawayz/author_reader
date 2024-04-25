from flask_app.config.mysqlconnection import connectToMySQL


class Author:
  DB = 'user_author'

  def __init__(self, data):
    self.id = data['id']
    self.user_id = data['user_id']
    self.title = data['title']
    self.author = data['author']
    self.description = data['description']
    self.created_at = data.get('created_at')
    self.updated_at = data.get('updated_at')

  @classmethod
  def save (cls, data):
    query = """INSERT into author (title, author, description, user_id, created_at, updated_at) 
VALUES (%(user_id)s, %(title)s, %(author)s, %(description)s, NOW(),NOW());"""
    results = connectToMySQL('user_author').query_db(query, data)
    return results

  @classmethod
  def get_recipe_by_id(cls, id):
    query = """SELECT author.id as id, title, author, description, author.created_at, movies.updated_at, user_id, first_name AS posted_by FROM
    movies JOIN user ON user.id = author.user_id WHERE user.id = %(id)s;"""
    results = connectToMySQL('user_author').query_db(query, {"id": id})
    return cls(results[0])

  @classmethod
  def get_all(cls):
    query = """SELECT author.id as id, title, author, description, author.created_at, movies.updated_at, user_id, first_name AS posted_by FROM
    author JOIN user ON user.id = author.user_id;"""
    results = connectToMySQL('user_author').query_db(query)
    if not results:
      return []
    return [cls(row) for row in results]

  @classmethod
  def edit_recipe(cls, data):
    query = """UPDATE movie SET title=%(title)s, author=%(author)s, description=%(description)s, WHERE author.id = %(id)s;"""
    results = connectToMySQL('user_author').query_db(query, data)
    return results

  @classmethod
  def delete_recipe_by_id(cls, id):
    query = """DELETE FROM author WHERE id = %(id)s;"""
    results = connectToMySQL('user_author').query_db(query, {"id": id})
    return results

  @staticmethod
  def validate(data):
      errors = []

      required_fields = ('title', 'author', 'description')
      for required_field in required_fields:
        if required_field not in data:
          errors.append(f"Missing required field '{required_field}'!")


      if len(data["name"]) < 2:
        errors.append("Name must contain atleast 2 characters.")

      if len(data["instructions"]) < 3:
        errors.append("Instructions must contain atleast 8 characters.")

      if len(data["description"]) < 3:
        errors.append("Description must contain atleast 8 characters.")

      is_valid = len(errors) == 0
      return is_valid, errors
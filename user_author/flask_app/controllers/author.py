from flask_app import app
from flask import render_template, request, flash, redirect, session
from flask_app.models.user import User
from flask_app.models.author import Author

@app.route('/dashboard')
def author_home():
  return render_template ('dashboard.html')
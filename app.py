import sqlite3
import logging
import sys
from datetime import datetime

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

# Connection counter
conn_count = 0

# Function that makes log messages with the timestamp included
def log_with_time(log_text):
    now = datetime.now()
    log_time = now.strftime('%d/%m/%Y, %H:%M:%S')
    app.logger.info(f'{log_time}, {log_text}')

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global conn_count
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    conn_count += 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      not_found = f'404: Article {post_id} not found'
      log_with_time(not_found)
      return render_template('404.html'), 404
    else:
      art_found = f'Article {post_id} found, render'
      log_with_time(art_found)
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    about_access = 'About Us page accessed'
    log_with_time(about_access)
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()

            app.logger.info(f'New post created: {title}')

            return redirect(url_for('index'))

    return render_template('create.html')

# Function to count number of posts using post -> id
# Dont use the get_db_connection() to avoid skewed connection count
# fetchone returns tuple so select first element

def post_counter():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    post_count = connection.execute('SELECT COUNT(id) FROM posts').fetchone()
    connection.close()
    return post_count[0]    

# Define a healthz endpoint
@app.route('/healthz')
def healthz():
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    return response

# Define a metrics endpoint
@app.route('/metrics')
def metrics():
    response = app.response_class(
            response=json.dumps({"db_connection_count":conn_count,"post_count":post_counter()}),
            status=200,
            mimetype='application/json'
    )
    return response

# start the application on port 3111
if __name__ == "__main__":
    # make two stream handlers to allow output to both stdout and stderr
    sh_out = logging.StreamHandler(sys.stdout)
    sh_err = logging.StreamHandler(sys.stderr)
    logging.basicConfig(handlers = [sh_out, sh_err],level=logging.DEBUG)
    #logging.basicConfig(filename='app.log',level=logging.DEBUG)
    app.run(host='0.0.0.0', port='3111')

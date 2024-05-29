from flask import Flask,flash
import sqlite3
import jwt
import openai
from datetime import datetime, timedelta
from passlib.hash import sha256_crypt
from flask import Flask, render_template, request, redirect, url_for, make_response, session
from tools import DatabaseWorker,checkHash,encrypt,logged
import os
from numba import cuda
import numpy as np
app = Flask(__name__)
app.secret_key = "23yerfgjuehib2qrf"
token_key=os.getenv('secret_key_lol')
app.url_map.strict_slashes = False

"""
@cuda.jit
def compute_trending_scores(post_data, scores):
    idx = cuda.grid(1)
    if idx < post_data.size:
        scores[idx] = post_data[idx] * 1.5
"""

openai.api_key="masked"
subtrenditt_id=0
"""
def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role":"user","content":prompt}]
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    while True:
        user_input = input("You:")
        if user_input.lower() in ["quit","exit","bye"]:
            break

        response = chat_with_gpt(user_input)
        print("Chatbot:",response)
"""

from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'token' not in session:
            return redirect(url_for('login'))
        try:
            data = jwt.decode(session['token'], token_key, algorithms=['HS256'])
        except:
            return redirect(url_for('login'))

        return f(*args, **kwargs)

    # Return the new decorated function
    return decorated



@app.route('/categories/≤int:cat_id>', methods =['GET', 'POST'])
def category():  # put application's code here
    return 'Hello!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    db = DatabaseWorker('unit4.db')
    if request.method == 'POST':
        uname = request.form.get('username')
        password = request.form.get('password')
        user = db.search("SELECT id, password FROM users WHERE username = ?", (uname,))
        if user and checkHash(password, user[1]):
            user_id = user[0]
            response = make_response(redirect(url_for('home2')))
            response.set_cookie('user_id', str(user_id))
            print(user_id)

            token = jwt.encode({'user_id': str(user_id), 'exp': datetime.utcnow() + timedelta(minutes=45)},token_key,algorithm='HS256')

            session['token'] = f"{token}"
            return response
        return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/register', methods = ['GET', 'POST'])
#@token_required
def register():
    if request.method == "POST":
        db = DatabaseWorker("unit4.db")
        email = request.form['email']
        password = request.form['password']
        city = request.form['city']
        username = request.form['username']
        if len(username)>0  and len(email)>0 and len(password)>0:
            if len(password) < 8:
                flash(('Password must be at least 8 characters.', 'danger'))
            else:
                if '@' not in email:
                    flash(("Invalid email address", 'danger'))
                else:
                    db.run_query(f"INSERT into users (username, email, password,city) values('{username}', '{email}', '{encrypt(password)}','{city}')")
                    flash(('Registration completed. Please log in.', 'success'))
                    db.close()

                    return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/users', methods=['GET', 'POST'])
def users():
    # Checks if the user is authenticated by checking if the user.id cookie exists
    if request.cookies.get('user.id'):
        db = DatabaseWorker(
            "unit4.db")  # Creates a database worker object to perform SQL queries on the "unit4.db" database
        full_users = db.search("SELECT * FROM users")  # Selects all users from the "users" table # selects username email adress and the city of the user
        db.close()  # Closes the database connection
    return render_template('users.html')


@app.route('/subtrenditt', methods = ['GET', 'POST'])
def subtrenditt():
    return render_template('subtrenditt.html')

@app.route('/subtrenditt/mumbai', methods =['GET', 'POST'])
def STmumbai():  # put application's code here
    subtrenditt_id=4
    return render_template('STmumbai.html.html')

@app.route('/subtrenditt/madrid', methods =['GET', 'POST'])
def STmadrid():  # put application's code here
    subtrenditt_id=1
    return render_template('STmadrid.html.html')
@app.route('/subtrenditt/london', methods =['GET', 'POST'])
def STlondon():
    return render_template('STlondon.html.html')


@app.route('/subtrenditt/<int:subtrenditt_id>/create', methods =['GET', 'POST'])
def create_post():
    db=DatabaseWorker('unit4.db')
    title = request.form['title']
    comment = request.form['comment']
    image_url = request.form['image_url']
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    likes = 0
    user_id = request.cookies.get('user_id')
    db.run_query(
        'INSERT INTO posts (title, comment, image_url, date, subtrenditt, likes, user_id) VALUES (%s, %s, %s, %s, 0, %s, %s)',
        title, comment, image_url, date, likes, user_id)


    if user_id is None:
        return "User not signed in", 401
    return redirect(url_for('index'))

@app.route('/subtrenditt/tokyo', methods =['GET', 'POST'])
def STtokyo():  # put application's code here
    subtrenditt_id=3
    return render_template('STtokyo.html')

@app.route('/recover', methods = ['GET','POST'])
def recover():
    return 'recover'


@app.route('/logout', methods = ['GET'])
def logout():
    return 'logout'


@app.route('/profile', methods = ['GET'])
def profile():
    return 'profile'

@app.route('/profile/edit', methods = ['GET','POST'])
def profile_edit():
    return 'profile edit'
from flask import Flask, render_template, request
from numba import cuda
import numpy as np

app = Flask(__name__)

# Define a simple kernel function to run on the GPU
@cuda.jit
def compute_trending_scores(post_data, scores):
    idx = cuda.grid(1)
    if idx < post_data.size:
        scores[idx] = post_data[idx] * 1.5  # Simplified example of computing a score

""""
@app.route('/popular', methods = ['GET','POST'])
def popular():
    # Example post data
    num_posts = 1000000
    post_data = np.random.rand(num_posts).astype(np.float32) #generates an array of num_posts random numbers between 0 and 1, and converts the array elements to 32-bit float data type.
    scores = np.zeros(num_posts, dtype=np.float32)

    # Transfer data to GPU
    post_data_device = cuda.to_device(post_data)
    scores_device = cuda.to_device(scores)

    # Configure the blocks and threads
    threads_per_block = 256
    blocks_per_grid = (post_data.size + (threads_per_block - 1)) // threads_per_block

    # Launch the kernel
    compute_trending_scores[blocks_per_grid, threads_per_block](post_data_device, scores_device)

    # Copy the results back to the CPU
    scores = scores_device.copy_to_host()

    # Example output for the first 10 scores
    #return f"Trending scores computed. First 10 scores: {scores[:10]}"
    scoress=scores[:10]
    return render_template("popular.html",scoress=scoress)
"""
@app.route('/',methods = ['GET','POST'])
def home():
    return render_template("home.html")

@app.route('/comment/edit',methods = ['GET','POST'])
def comment_edit(review_id, subtrenditt_id):
    db = DatabaseWorker('database.db')
    food = db.search(f"SELECT * FROM foods where id = {food_id}", multiple=False)
    reviews = db.search(f"SELECT * FROM reviews where food_id = {food_id}", multiple=True)
    review_to_edit = db.search(f"SELECT * FROM reviews where id = {review_id}", multiple=False)
    comments = review_to_edit[1]
    stars = review_to_edit[3]
    if request.method == 'POST': # update the review and redirect to the food page
        comment = request.form.get('comment')
        stars = request.form.get('stars')
        db.run_query(f"UPDATE reviews SET comment = '{comment}', stars = {stars} WHERE id = {review_id}")
        db.close()
        return redirect(url_for('get_food', food_id=food_id))

    return render_template("comment_edit.html.html")

@app.route('/home',methods = ['GET','POST'])
def home2():
    db = DatabaseWorker("unit4.db")
    userss = db.run_query("select username from users ")
    print(userss)
    return render_template("home2.html", userss=userss)



@app.route('/send_email', methods=['GET', 'POST'])
def send_email():
    if request.method == 'POST':
        email = request.form['email']
        subject = request.form['subject']
        message_body = request.form['message']

        # Create a message object
        msg = Message(subject, recipients=[email])
        msg.body = message_body

        try:
            # Send the email
            mail.send(msg)
            flash('Email sent successfully!', 'success')
        except Exception as e:
            flash(f'Failed to send email: {e}', 'error')

        return redirect(url_for('send_email'))

    return render_template('send_email.html')












@app.route('/chatbot',methods = ['GET','POST'])
def chatbot():
    return render_template("chatbot.html")
if __name__ == '__main__':
    app.run()

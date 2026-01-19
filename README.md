# Unit 4 Project
![](https://github.com/marinamen/unit4_project/blob/main/images/Disen%CC%83o_sin_ti%CC%81tulo__1_-removebg-preview.png)
# A Reddit Redesign:Trenditt

## [Background](#background)
2.1.[Success Criteria](#success-criteria)

2.2. [Sources](#sources)

2.3[Development](#development)

## [Criteria C: Development](#criteria-c-development)

2.1.[Tools and techniques used](#techniques-used)

2.2. [Sources](#sources)

2.3[Development](#development)

# Background


- For our Unit 4 and final G11 CS project we were tasked with re-creating a online board system such as reddit. Solely evaluated using Criteria C, D and E using a MVP.
- In accordance with this I chose to develop a redesign that would solely surround fashion, I got some inspiration from Pinterest *[1]*


## Success Criteria 

Create a Flask Web application for an online bulletin board system (like reddit). You are free to set the general theme, groups, visuals (CSS), topics, etc, but you need:

**1. A login/registration system.**

**2. A posting system to EDIT/CREATE/DELETE comments.**

**3. A system to add/remove likes.**

**4. A system to follow/unfollow users, follow/unfollow topics or groups.**

**5. A profile page with relevant information**

**6. [HLs] upload images**

**7. [HL++] send emails**

# Criteria C Development

## Existing tools

| Libraries      |
|----------------|
| Flask          |
| SQLite3        |
| JWT            |
| werkzeug.utils |
| datetime       |
| os             |
| sqlite 3       |
| passlib.hash   |


## Techniques used

1. Manipulating SQLite Database
2. Functions
3. For loops
4. If statements
5. Variables
6. Encryption
7. Nesting loops
8. HTML template usage
9. JSON JWT token usage
10. Cookie usage
11. CSS web design 
12. Flask Library
13. Get/Post methods
14. Cookies
15. OOP (object oriented programming)

## Sources
1. “Pinterest.” Pinterest, Pinterest, 2018, www.pinterest.es/.
2. “Flask HTTP Methods, Handle GET &amp; Post Requests.” GeeksforGeeks, GeeksforGeeks, 2 Feb. 2023, https://www.geeksforgeeks.org/flask-http-methods-handle-get-post-requests/. 
3. “Cirrus CSS.” Cirrus, https://www.cirrus-ui.com/buttons/basics. 
4. Auth0. “JSON Web Tokens.” Auth0 Docs, https://auth0.com/docs/secure/tokens/json-web-tokens. 
5. “How to - Search Bar.” How To Create a Search Bar, https://www.w3schools.com/howto/howto_css_searchbar.asp.
6. “GPU Programming: When, Why and How? — GPU Programming: Why, When and How? Documentation.” Enccs.github.io, enccs.github.io/gpu-programming/.
7. “Introduction to Numba: CUDA Programming.” Nyu-Cds.github.io, nyu-cds.github.io/python-numba/05-cuda/. Accessed 29 May 2024.
8. “Beginner’s Guide to GPU Accelerated Graph Analytics in Python.” NVIDIA Technical Blog, 24 Mar. 2021, developer.nvidia.com/blog/beginners-guide-to-gpu-accelerated-graph-analytics-in-python/.
9. “What Is User Interface (UI)? | Indeed.com.” Indeed Career Guide, www.indeed.com/career-advice/career-development/user-interface#:~:text=The%20user%20interface%20is%20the.


## SUCCESS CRITERIA 1 : An encrypted login/registration system.

In order for Trenditt to operate within the minimum viable product it needs to have an account system, like the standard website it has two options **Login** or **Register**. Within these it allows to create or gain access to an already created account, for our users information to be secure we also introduced a set of security measures that the users information is subjected to in order to eliminate any risk of external threat or misuse of information.

To start the a webpage there is certain things to take into account:

**LOGIN SYSTEM**
```.py
@app.route('/login', methods=['GET', 'POST'])
```
*fig.1*
App route, so into what adress from our website this page is saved under, in this case it would be under **"website/login.httml"** and the methods allowed. Essentially what this means is that within this page of our website there will be certain usages that will require the information to be fetched, updated or saved in the database, hence `GET` in order to retrieve information, `POST` in order to save and update what is written by the user. *Important note is that the code for the website in order to be functional it needs to be saved within a function of the page's name*

Within our login function:

A connection with our Database function is established following the usual protocol shown below. My previous `DatabaseWorker` had a significant downside, it's vulnerability to SQL injection attacks when  incorporating user input into the queries, in order to mitigate this risk and improve security, I altered the run_query method to accept a `params tuple`. 

```.py
def run_query(self, query: str, params: tuple = ()):
    self.cursor.execute(query, params)
    self.connection.commit()

```
*fig.2*

1. `params: tuple = ()` This change introduces a params parameter, which is a tuple (finite sequence or ordered list of numbers) containing the values to be safely inserted into the SQL query.
2.`self.cursor.execute(query, params)` By passing the params tuple to the execute method, I allow the database worker to handle the insertion of these parameters safely, this method replaces any placeholders in the query (typically represented by ? ) with the actual values in params, escaping them appropriately to prevent SQL injection.

*fig.2*

Following this we will now set what happens when a button is clicked within the website that needs information or verification from the database. In this case since it is a login we will use an if that is complied whenever a button that requires something to be verified with the database so it would be triggered when the `LOGIN` button is clicked after the user has inputted their information.

```.py
    if request.method == 'GET':
        uname = request.form.get('uname')
        password = request.form.get('psw')
```
*fig.3*

As I mentioned before when the website requires infomation from the database it will trigger the `GET` method and this will retrieve the information inputted in the text inputs  of *uname* and *password* and save it under the two variables shown above.

Next step is to verify whether the information inputted by the user matches the previous credentials. In order to do this we use our connection with the database to retrieve information with our Database Worker class. Using the function within it run_query that as the name says will run the SQL query, and in this case it will fetch the information where the username equals the one inputted and then will use index [0] for the id and [1] for the password. A problem I encountered was that I wanted to prevent my databases from sql injections, Using algorithmic thinking I used parameterized queries that ensures that user input is treated as data rather than executable code, it maintains the integrity and security of the SQL queries.


```.py
        user = db.run_query("SELECT id, password FROM users WHERE username = ?", (uname,))
        if user and check_password_hash(user[1], password):
```
*fig.4*

After this comes the most crucial part the actual verification of the user's credential, I used an if loop since it is simple and perfectly fitting for this condition. If user exists, meaning if the query retrieved any information from the database using the inputted username then it will check the password. Since the password is saved hashed, using sha256 encryption, the method i used to check was a function I had previously created called check_hash which simply dehashes the encryption and compares the result with the unhashed inputted password, returning `true[1]` or `false[0]`.

```.py
def checkHash(text: str, hashed: str) -> bool:
    return hasher.verify(text, hashed)
```
*fig.5*


When a true is returned the code that follows runs, it indexes the first value of user which would be the id and saves it under the `user_id`  . It then redirects the page to the home page and in order for the website to be altered and saved under a user, it sets a cookie in the user's browser  with the user id. 
```.py
    user_id = user[0]
    response = make_response(redirect(url_for('trenditt_home')))
    response.set_cookie('user_id', str(user_id))
    token = jwt.encode({'user_id': user_id, 'exp': datetime.utcnow() + timedelta(minutes=45)}, token_key, algorithm = 'HS256')
    session['token'] = token
```
*fig.6*

The first argument, `user_id`, is the name of the cookie, this is the key that will be used to retrieve the cookie's value later. The second argument, `str(user_id)`, is the value of the cookie. The user ID is converted to a string and stored in the cookie. 

Next under `token` a JSON Web Token (JWT) is created to securely store the user's ID and an expiration time. The token is generated with the user's id and set to expire in 45 minutes, this token is then stored in the user's session. This allows the application to verify the user's identity and session validity on subsequent requests.This important implementation was inspired by using computational thinking and decomposing the problem of webiste's safety into various parts, the encrypting and the JWT. Otherwise even after implementing cookies, the user could still redirect to a page without signing in beforehand, this is why I generalized the algorithm for creating JWT session tokens 11 which in turn allowed me to set a requirement that a user is logged in before accessing any features of the website. This improved security of the website and solved the previously decomposed problem of safety that the website had.
Its true that I couldve implemented a boolean variable that verified the user was logged in but this would require many more lines of code and so I used decomposition and code optimisation in order to find the most efficient and viable safety for the website.




Lastly if the conditions required are not met it an error pops up.
```.py
  return render_template('login.html', error='Invalid username or password')
```
*fig.7*


**REGISTRATION SYSTEM**



```.py
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

```
*fig.8*

As shown in fig.8 the additional feature that the register function has, after multiple verifications of whether the inputted information by the user meets requirements such as email having `@` or password confimation, the information is inputted into he database via the method `POST` from the register button in the website, by the SQL query shown above. Although the amount of if loops here is quite inefficient I wanted to be able to have many requirements and so I decomposed it into smaller bits and the safest and least time demanding technique was to just put conditions using if and else techniques. I used the flash message in html which allows you to display messages on the top of the website to your program requirements, in this case when I was decomposing the algorithm I found that the best way to alert the user to change was via these.


##  Retrieving all Comments for Profile Page Display

```.py
  if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            now=datetime.now()
            today = now.strftime("%d/%m/%Y")
            if len(title) > 0 and len(content) > 0 and str(user_id) == current_user_id:  # check if the comment is being made by the logged in user
                new_post = f"Insert into comment (title,content,user_id,publish_date) values('{title}','{content}','{user_id}','{today}')"
                db.run_save(query = new_post)
                return redirect(url_for('profile', user_id = user_id))
        users, comment = None, None
        user = db.search(f"SELECT * from users where id={user_id}")
        if user:
            posts = db.search(f"select * from posts where user_id={user_id}")
            user = user[0]  # remember search returns a list (should be one user so...

        return render_template("profile.html", user = user, posts = posts, current_user_id=int(current_user_id))

```
*fig.9*

I developed this  to handle the creation of a new comment and to link it with the user who posted iot . When the user clicks submit on the comment (POST request), the code retrieves the title and content of the post from the form data. It also gets the current date formatted as DD/MM/YYYY, before inserting the comment into the database, the code checks if the title and content are not empty and if the user ID from the form matches the currently logged-in user ID (current_user_id) using the JWT. This ensures that only the logged-in user can make the post, an extra layer of safety from the `@token_required` method. It these are met, a SQL query inserts the comments into the comments table, and db.run_save executes this query. After saving the post, the user is redirected to their profile page.

For the `GET` request, the code fetches the user's data and their posts, and comments from the database, initially the variables of comments and id are set  to None. The user's data is fetched using their ID, and if the user exists, their comments are retrieved from the comments table. The user variable is then set to the first item in the list since the search query returns a list finally, the profile page is rendered with the user's data, their posts, and the current_user_id to manage display and interaction logic on the front end, ensuring secure post creation and dynamic profile rendering.







*fig.8*

##  Nested Loop to Display Dynamic Feed

```.html
<div class="feed">
    {% for post in posts %}
    <!-- loop through each post in the 'posts' list -->
    <div class="post" id="post-{{ post.id }}">
        <!-- set the id of the post dynamically based on the post id -->
        <div class="post-header">
            <!-- post header section -->
            <img src="/static/{{ post.logo }}" alt="Logo" class="post-logo">
            <!-- display the posts logo image -->
            <span class="post-logo-text">t/ {{ post.subtrenditt }}</span>
            <!-- display the subtrenditt name -->
            <button class="join-button" onclick="toggleJoin(this)">Join</button>
            <!-- join button with an onclick event handler -->
        </div>
        <img src="/static/{{ post.image }}" alt="Post Image" onclick="viewPost({{ post.id }})">
        <!-- display the main post image with an onclick event handler to view the post -->
        <div class="post-title">{{ post.title }}</div>
        <!-- display the title of the post -->
        <div class="post-description">{{ post.description }}</div>
        <!-- display the description of the post -->
        <div class="post-user" onclick="viewProfile('{{ post.user }}')">Posted by {{ post.user }}</div>
        <!-- display the user who posted with an onclick event handler to view the profile -->
        <div class="post-actions">
            <button onclick="likePost({{ post.id }})">Like</button>
            <!-- like button with an onclick event handler to like the post -->
        </div>
    </div>
    {% endfor %}
    <!-- dnd of the for loop -->
</div>


```
*fig.10*

To create a dynamic post feed, I employed the principles of Decomposition and Abstraction. By decomposing the problem, I identified the need of a data source, pass this data to the HTML template, and generate HTML dynamically. The defined database is a SQLlite one in the table `posts`, where each post containins attributes like id, subtrenditt, logo, image, title, description, and user_id. We then passed this list of posts to the template using Flask's render_template function, in the template, I used `Jinja2` to and nested for loops to iterate through the list and dynamically generate the HTML structure for each post, thereby avoiding repetitive code and making the system scalable. This  assures that the content is easily maintainable and allows for simple updates by modifying the database using queries without altering the HTML structure, which allows for any developer to further develop it without much complication. This also follows the `KISS` programming paradigm, since it allows for the whole posting algorithm to be simple and not repetitive. 

During the development of this I encountered a significant amount of misformatted retrievals of data that then displayed the posts incorrectly, how I solved it was by implementing debugging techniques such as printing the information after being retrieved, this showed me that the problems were formed with my HTML formatting of the information, and after researching and trying different solutions, I realised that indexing brought me troubles so instead i used the `.example` technique that allowed no room for misformatting erros.


## SUCCESS CRITERIA 3 : A system to add/remove likes.
```.py
@app.route('/like_post/<int:post_id>', methods=['POST'])
@token_required  # ensure that the user is authenticated
def like_post(post_id):
    user_id = request.user_id  # retrieve the user_id from the request (set by the token_required decorator)
    if not user_id:
        # If the user is not authenticated, return an error response
        print("user not authenticated")
        return jsonify({'success': False, 'message': 'User not authenticated'}), 401

    db = DatabaseWorker('unit4.db')  # create an instance of DatabaseWorker to interact with the database

    # check if the user has already liked the post
    liked = db.search("SELECT * FROM post_likes WHERE post_id = ? AND user_id = ?", (post_id, user_id), multiple=False)
    print(liked)
    if liked:
        # if the user has already liked the post, remove the like
        db.run_query("DELETE FROM post_likes WHERE post_id = ? AND user_id = ?", (post_id, user_id))
        db.run_query("UPDATE posts SET likes = likes - 1 WHERE id = ?", (post_id,))
    else:
        # if the user has not liked the post yet, add the like
        db.run_query("INSERT INTO post_likes (post_id, user_id) VALUES (?, ?)", (post_id, user_id))
        db.run_query("UPDATE posts SET likes = likes + 1 WHERE id = ?", (post_id,))

    # get the updated number of likes for the post
    post = db.search("SELECT likes FROM posts WHERE id = ?", (post_id,), multiple=False)
    if post:
        likes = post[0]  # extract the number of likes from the query result
        return jsonify({'success': True, 'likes': likes})  # return the updated like count as a JSON response
    return jsonify({'success': False})  # if the post is not found, return a failure response



```
*fig.11*

In order to create a system that allows the user to like and unlike I used the computational thinking Algorithm Design to handle post likes effectively. I started by defining the route /like_post/<int:post_id> to manage POST requests, ensuring that only authenticated users could interact with it through the `@token_required` decorator. This decorator extracts the user_id from the JWT token and attaches it to the request, hence if the user is not authenticated, a JSON response indicates the failure and doesnt allow the unauthorised user to continue. Next step is,the function checks if the user has already liked the post, if it returns true , it removes the like and decrements the like count. Otherwise, it adds a new like and increments the count this ensures a correct use and not abuse of the existing like count. Finally, the updated like count is fetched and returned as a JSON response, this design ensures security, as the `@token_required` decorator only allows authenticated users. The self-duplicating like/unlike mechanism checks the current state and updates accordingly, preventing data corruption, parameterized queries in db.run_query and db.search methods safeguard against SQL injection. The code is also commented in order to enhance extensibility.






## SUCCESS CRITERIA 6 : [HLs] upload images.

Another success criteria was being able to upload images, and for this to function there needs to be a base assumption that the user has the files they want to upload already in their files. This is an issue in terms of scalability since in the future a way to expand it into uploading images from a remote cloud database such as Google Photos instead of Local Database such as finder.

```.py

def create_post():
    if request.method == 'POST':
        subtrenditt = request.form['subtrenditt']
        image = request.files['image']
        title = request.form['title']
        comment = request.form['comment']
        user_id = request.cookies.get('user_id')

        if image and user_id:
            filename = secure_filename(image.filename)
            image_path = os.path.join('static/uploads', filename)
            image.save(image_path)

            db = DatabaseWorker('unit4.db')
            db.run_query(
                "INSERT INTO posts (title, comment, image_url, date, subtrenditt, likes, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)",(title, comment, image_path, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), subtrenditt, 0, user_id))
            flash('Post created successfully!', 'success')
            return redirect(url_for('home2'))

    return render_template('create_post.html')



```


*fig.12*


As shown in fig.12 to develop the `create_post` function, I used the computational thinking technique of **Algorithmic Thinking** to effectively manage post creation, including a secure upload of photos. The function starts by extracting standard form data, such as `subtrenditt`, `image`, `title`, and `comment`, and retrieves the `user_id` from cookies to ensure the user is authenticated. For image uploads, the image filename is cleaned up by using `secure_filename` to prevent any malicious file names and is saved in the `static/uploads` directory created only for user uploads, this has limitations since it is still quite not secure which can lead to privacy leaks but it is a further reccomendation . A `DatabaseWorker` instance then runs a parameterized query to insert the new post into the `posts` table, which includes the image path, current date, subtrenditt, initial like count (set to 0), and user ID so that the social network is able to have enough information for all types of data handling later on. If the post is successfully created, a success message is flashed to the user, and they are redirected to the home page. An obstacle I encountered was ensuring the secure handling and storage of uploaded files, I solved this by using `secure_filename` and organizing uploads into a dedicated directory, this approach allows to securely manages user inputs and file uploads.

## SUCCESS CRITERIA 7 : [HL++] send emails.



```.py
@app.route('/send_email', methods=['POST', 'GET'])
@token_required
def send_email():
    user_id = request.user_id  #retrieve user_id from the token
    db = DatabaseWorker('unit4.db')
    user = db.search("SELECT email FROM users WHERE id = ?", (user_id,), multiple=False)
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('home2'))

    sender_email = user[0]

    if request.method == 'POST':
        recipient_email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        #simulate sending email by printing the details to the terminal
        print(f"Email from: {sender_email}")
        print(f"Email to: {recipient_email}")
        print(f"Subject: {subject}")
        print(f"Message: {message}")

        flash('Email sent successfully!', 'success')
        return redirect(url_for('send_email'))

    return render_template('send_email.html', sender_email=sender_email)

```
*fig.13*

The Send_email function shown in Fig.13 is a email sending replication system, I utilized the Object-Oriented Programming (OOP) principles to securely handle user authentication and database interactions. It then queries the database for the user's email, if the user is not found, an error message is flashed, and the user is redirected to the home page which mantains a safe and preventive algorithm . Upon a POST request, the function retrieves the recipient's email, subject, and message from the form data, for simplicity and safety in a development environment, the function simulates sending the email by printing the details to the terminal instead of actually sending it since I do not have a valid email port that I can use to send actual emails. After simulating the email send, a success message is flashed, and the user is redirected back to the homel my approach demonstrates OOP principles such as encapsulation, by encapsulating database operations within the DatabaseWorker class, and abstraction, by simplifying complex database interactions,h owever, a notable limitation is that as i mentioned previously it only simulates email sending, which is unsuitable for a production environment, this can be resolved by integrating a real email service, thus ensuring the function is ready for actual email dispatch if extended











## SUCCESS CRITERIA 8 : Trenditt will have a feature to display all users, emails and relevant information including no of posts and followers.

Since Trenditt is a social network that is still growing, I wanted to implement a feature for all current users to be able to access other user's information and see their amount of posts and followers. In order to develop this I had to use computational thinking and abstract all the non relevant information here which is the other feauture of the emails and the profile page. By using abstraction I developed the below:

```.py
@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.cookies.get('user_id'): # Checks if the user is authenticated by checking if the user.id cookie exists
        db = DatabaseWorker(
            "unit4.db")  # Creates a database worker object to perform SQL queries on the "unit4.db" database
        full_users = db.search("SELECT * FROM users")  # Selects all users from the "users" table # selects username email adress and the city of the user
        db.close()  # Closes the database connection
    return render_template('users.html')

```
*fig.14*

Fig.14 hows the function used to showcase the list of all trenditt users, it uses an algorithm that checks if the user has a valid cookie and then it shows the list of users extracted from the user database, although not shown here, for obvious reasons in the html code showing information such as the hashed password is omitted and only the relevant user information is displayed. So the table is formatted with username, email, city, followers, posts. 

A cool feauture I added in the home page is that along the main post feed, there is two boxes, displaying the usernames of all of the users that are currently part of the trenditt social network. Using my skills for UI, which its goal is to make the user's experience easy and intuitive, requiring minimum effort on the user's part to receive the maximum desired outcome[^9] I though about this feature, that for a growing network its a good incentive to want to interact with users in a very easy and intuitive way that doesnt require much further thought.

In order to do this, I will show how I set this up using abstraction, focusing only on the specific code that performs the task described.

```.py
#within home function and after establishing database connections

userss = db.run_query("select username from users ")


```

```.html
    <div class="feed-container">
        <div class="user-list">
            <h2>users</h2>
            <ul>
                {% for j in userss %}
                    <li>{{ j }}</li>   
                {% endfor %}
            </ul>
        </div>
    </div>
````

## Further Options: Analysing Trends with Numba CUDA NVIDIA  ( which incorporates GPU programming)

An important addition that could be added if Trenditt were expanded into a larger social network and would want to potentially become more personalized would be Analysing Trends by using Graphic Proccessing Unit programming. Imagine you are running a social media platform where you need to analyze engagement metrics from posts to determine trending topics. Each metric (likes, shares, comments) is assigned a score, and you need to process millions of these metrics quickly to update the trending topics in real-time.
By using GPU acceleration it would be able to:

*- Process large datasets much faster than using CPU alone.*

*- Provide real-time analytics and insights to users.*

*- Upgrade performance and responsiveness of Social Network.*

---------------------------------------------------------------------------------------------------------------------

I decided to give it a sample try, but before the process is described I would like to mention limitations:

---------------------------------------------------------------------------------------------------------------------


**➼ Simplistic computation only multiplies values, lacking real-world complexity.** `(my example only uses multiplication versus real word would use machine learning algorithms)`

**➼ No handling of data transfer overhead between CPU and GPU.** `(data pre proccessing not included, since my data is only integers)`

**➼ Limited error handling and debugging capabilities.** `(my code does not allow for any GPU memory allocation failures, invalid inputs, or kernel execution error)`

**➼ Does not account for diverse data types and structures.**`(only generating integers artifically, my values are generated randomly but usually they would be retrieved from databases)`

**➼ Lacks integration with other analytical and data processing tools.** `(the integration with my flask app is minimal, but if there was high traffic a seamless integration would be needed)`

---------------------------------------------------------------------------------------------------------------------

To start off I followed various tutorials **[^6] [^7] [^8]**  that are cited in [Sources](#sources). In order to develop this I used decomposition and abstraction since it is a pretty big algorithm to tackle that involves many broad elements surrounding it, I overcame those by using computational thinking.

1. In order to analyse trends using the GPU, we need to have a series of data points that represent engagement metrics, such as likes, comments or follow. `Num_posts` is set to 1,000,000, simulating a large dataset, `post_data` generates an array of one million random float numbers between 0 and 1 and converts them to 32-bit floats for efficient GPU processing. The `scores` array, is initialised to zero and it will store the worked scores after GPU processing. Essentially it allows us to leverage the GPU to perform parallel computations on the dataset efficiently.

```.py
@app.route('/popular', methods = ['GET','POST'])
def popular():
    num_posts = 1000000   #example post data
    post_data = np.random.rand(num_posts).astype(np.float32) #generates an array of num_posts random numbers between 0 and 1, and converts the array elements to 32-bit float data type
    scores = np.zeros(num_posts, dtype=np.float32) #creates an array of num_posts elements, all initialized to 0, with each element being a 32-bit float
```
2. Next step is to transfer data from the CPU to the GPU, `cuda.to_device(post_data)`copies the `post_data` array generated previously to the GPU's memory which allows it to later be proccessed by the GPU. Similarly stored into `scored_device`, `cuda.to_devices` copies the `scores` array to the memory, are the results of the computation.  This step is needed for the parallel processing.
   
```.py
    #transfers data to gpu
    post_data_device = cuda.to_device(post_data)
    scores_device = cuda.to_device(scores)
```
3. In CUDA programming it is essential to know what kernal function,threads and blocks are,
   
-*Kernal Function*: class of algorithm for pattern recognition.

- *Threads:* the smallest unit of execution, where each thread executes a copy of the kernel function.
  
- *Blocks:* groups of threads that run the kernel function, blocks can run independently and simultaneously on the GPU.
  
As shown this section of code configures the number of threads and blocks for the GPU computation, `threads_per_block` sets the number of threads in each block to 256. 
`blocks_per_grid` calculates the total number of blocks needed to cover all elements in `post_data`, it divides the total number of elements by the number of threads per block and uses `(threads_per_block - 1)` to make sure any remaining elements are also covered.

```.py
    # configures threads and blocks
    threads_per_block = 256
    blocks_per_grid = (post_data.size + (threads_per_block - 1)) // threads_per_block
```

4. Below I launched the kernel function with all of the needed variables, and this computed all the trending scores, next `scores`transfers the data from the GPU back to the CPU, it copies the scores array which is in the GPU´s memory back to the CPU's memory. The result is stored in the `scores` variable, which allows the CPU to access the results.

```.py
    #launch the kernel
    compute_trending_scores[blocks_per_grid, threads_per_block](post_data_device, scores_device)

    # Copy the results back to the CPU
    scores = scores_device.copy_to_host()
```

5. Then it  selects the first 10 elements in the array and using my html `popular` page the values of the trending scores get displayed.
```.py
    #example output for the first 10 scores

    scoress=scores[:10]
    return render_template("popular.html",scoress=scoress)
```

After attempting to run this program multiple times due to the fact I had abstracted the broader element I found myself with a challenge, or possibly more of an endpoint. NVIDIA CUDA toolkit is only possibly to be downloaded in Linux and/or Windows with compatible GPU's and since I'm operating from a Macbook it is not possible to run the actual program, still it is an interesting investigation that could be taken further with more consideration. GPU programming can be a breakthrough for not only analysis of trends but also running high traffic algorithms or visuals on webs, still compatibility issues are very predominant. 

When I hit the wall I decided to ask chatgpt to run a simulation instead and give me an example answer, Using `num_posts` of 1000000, it gave me the output below as an example of the `analysis_trend` function.

```.py
num_posts = 1000000
"Trending scores computed. First 10 scores: [1.275 1.4845 1.5675 0.7485 1.1325 1.932 0.6525 1.689 1.257 1.878]"
```











# Criteria D: Functionality and Extensibility 
## video link

https://drive.google.com/drive/u/0/folders/1u8XF1S-m0ZudBZugv-8VxZPUnOI8G1RP


# Criteria E: Evaluation
                                             
## Beta Testing 

Two potential users who had some knowledge in the development process reached out to us to try our social network and they gave us the feedback below. We have removed their names so that their identities are not compromised.

<img src="https://github.com/marinamen/unit4_project/blob/main/images/Disen%CC%83o%20sin%20ti%CC%81tulo%20(2).png" width=80% height=80%>

*fig.30*

<img src="https://github.com/marinamen/unit4_project/blob/main/images/Disen%CC%83o%20sin%20ti%CC%81tulo%20(3).png" width=70% height=70%>

*fig.31*

Additionally we asked them to complete the table below with their feebdack, they each adress the criteria mentioned before.

| Criteria | Met? | Feedback |
|---|---|---|
| The website has a login and registration system with input validations and secure storage | Yes | The login and registration process was smooth and easy to navigate. I felt secure knowing that my information was being stored safely. Great job on this! |
| The website only allows for users that are logged in to access the network (for longer than 10s) using JWT | Yes | The JWT implementation worked perfectly. I appreciate that only logged-in users can access the network, which adds an extra layer of security. |
| The website has a post system, that includes image, title, subtrenditt and date | Yes | Posting is straightforward and intuitive. I like how you can add images, titles, and select subtrenditts. The date feature is a nice touch, too. |
| The website allows for a like and comment system, which also allows to edit comment or remove like | Yes | The like and comment system is really engaging. I love that I can edit my comments and remove likes if needed. It makes interactions more flexible. |
| The website includes interactive feed that only displays posts of the subtrenditts followed | Yes | The feed is awesome. It only shows posts from the subtrenditts I follow, making it super relevant and easy to stay updated. |
| The website shows artificial trends in the popular by analysing trends. | Yes | The trends section is fascinating. It gives a great overview of what's popular by analyzing trends. This feature keeps the content fresh and interesting. |


### Reflection

Overall beta testers seemed pretty satisfied with the functionality and the appeal of it, however they do believe that in order to reach larger public we still have to implement more feauturesñ

## Reccomendations : Looking forward


### 1. Chat with other users

Expanding my trenditt to include a chat feature would significantly increase attraction, allowing users to communicate in real-time will create a more active and interactive communitym encouraging them to spend more time on the platform. By providing a space for users to share ideas, ask questions, and offer support, the chat feature would add value to their experience and increase overall satisfaction. It is definitely being considered for the future, however downsides could include that it could lead to cyberbullying or trolling, this would not be optimal since our web app aims to be a safe and exciting place where you can share your thoughts on fashion so that would mean that we would have to weigh out the pro's vs cons or possibly implement censoring into the chats to prevent this. This said we are definitely considering this as a future option.

### 2. Further expansion of cities/subtrenddits

The thing that the Beta Tester's mentioned multiple times was that even though all the cities for the subreddits were according to their tastes, as of this moment, they still think more cities or a system to create subtrenditts would be extremely attractive and necessary if we wanted Trenditt to expand. People hwo are not from the cities mentioned, are limited by this or forced to choose which they prefer, this is not ideal. If there is no increase in the number of subtrenditts then there will be no increase in users which supposes a problem because we want to continue expanding. However it is said that the cities picked are where the majority of global population is located hence why we chose them. Still, this is definitely in the top of our future priorities if we were to expand or someone would take over.

### 3. Analysis of Trends using GPU programming

An important addition that could be added if Trenditt were expanded into a larger social network and would want to potentially become more personalized would be Analysing Trends by using Graphic Proccessing Unit programming. Imagine you are running a social media platform where you need to analyze engagement metrics from posts to determine trending topics. Each metric (likes, shares, comments) is assigned a score, and you need to process millions of these metrics quickly to update the trending topics in real-time. If there was to be further expansion and it would reach a certain level of data stored then this would most definitely be a good and viable implementation.

# Appendix
## Forms Collected 
We collected 3 responses from a form in order to have a clearer picture of what the user wanted from their side and what they expected and whetehr they were even going to use it.

<img src="https://github.com/marinamen/unit4_project/blob/main/images/Screenshot%202024-05-30%20at%2011.50.25.png" width=80% height=80%>
<img src="https://github.com/marinamen/unit4_project/blob/main/images/Screenshot%202024-05-30%20at%2011.50.30.png" width=80% height=80%>
<img src="https://github.com/marinamen/unit4_project/blob/main/images/Screenshot%202024-05-30%20at%2011.50.35.png" width=80% height=80%>
<img src="https://github.com/marinamen/unit4_project/blob/main/images/Screenshot%202024-05-30%20at%2011.50.57.png" width=80% height=80%>
<img src="https://github.com/marinamen/unit4_project/blob/main/images/Screenshot%202024-05-30%20at%2011.51.02.png" width=80% height=80%>
<img src="https://github.com/marinamen/unit4_project/blob/main/images/Screenshot%202024-05-30%20at%2011.51.08.png" width=80% height=80%>
<img src="https://github.com/marinamen/unit4_project/blob/main/images/Screenshot%202024-05-30%20at%2011.51.16.png" width=80% height=80%>
<img src="https://github.com/marinamen/unit4_project/blob/main/images/Screenshot%202024-05-30%20at%2011.51.22.png" width=80% height=80%>



# Works cited
[^1]: Dream AI generated image (https://Project4pictureDreamAi.jpg)
[^2]: Sengar, Ritesh. “Python vs PHP: Which Is Better for Web Development?” Hackernoon, 7 Jan. 2021, hackernoon.com/python-vs-php-which-is-better-for-web-development-cj1236mj. 
[^3]: "Welcome to Flask." Flask Documentation, 15 Jan. 2023, flask.palletsprojects.com/en/2.1.x/. 
[^4]: Grinberg, Miguel. Flask Web Development: Developing Web Applications with Python. 2nd ed., O'Reilly Media, Inc., 2018. 
[^5]: “What Is a Database?” Oracle, https://www.oracle.com/database/what-is-database/. 
[^6]: "What is SQL?" W3Schools, W3Schools, https://www.w3schools.com/sql/
[^7]: "HTML Introduction." W3Schools, W3Schools, https://www.w3schools.com/html/html_intro.asp
[^8]: "Flash vs. HTML5." Digital.gov, 17 Dec. 2015, https://digital.gov/resources/flash-vs-html5/.
[^9]: "Why You Need an SEO-Friendly Website." SEO Werkz, 11 Jan. 2022, https://www.seowerkz.com/why-you-need-an-seo-friendly-website/.
[^10]: https://www.smashingmagazine.com/2010/01/color-theory-for-designers-part-1-the-meaning-of-color/
[^11]: 4. Auth0. “JSON Web Tokens.” Auth0 Docs, https://auth0.com/docs/secure/tokens/json-web-tokens. 

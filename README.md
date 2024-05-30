# Unit 4 Project
![](https://github.com/marinamen/unit4_project/blob/main/images/Disen%CC%83o_sin_ti%CC%81tulo__1_-removebg-preview.png)
# A Reddit Redesign : Trenditt

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

A connection with our Database function is established following the usual protocol shown below.
```.py
    db = DatabaseWorker('unit4.db')
```
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


## SUCCESS CRITERIA 2 : A posting system to EDIT/CREATE/DELETE comments.



## SUCCESS CRITERIA 3 : A system to add/remove likes.


## SUCCESS CRITERIA 4 : A system to follow/unfollow users, follow/unfollow topics or groups.
## SUCCESS CRITERIA 5 : A profile page with relevant information.
## SUCCESS CRITERIA 6 : [HLs] upload images.
## SUCCESS CRITERIA 7 : [HL++] send emails.
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
*fig.?*

Fig.? hows the function used to showcase the list of all trenditt users, it uses an algorithm that checks if the user has a valid cookie and then it shows the list of users extracted from the user database, although not shown here, for obvious reasons in the html code showing information such as the hashed password is omitted and only the relevant user information is displayed. So the table is formatted with username, email, city, followers, posts. 

A cool feauture I added in the home page is that along the main post feed, there is two boxes, displaying the usernames of all of the users that are currently part of the trenditt social network. Using my skills for UI, which its goal  is to make the user's experience easy and intuitive, requiring minimum effort on the user's part to receive the maximum desired outcome.

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

# Criteria E: Evaluation

| Criteria | Met? | Feedback |
|---|---|---|
| the website has a login and registration system with input validations and secure storage | yes |  |
| the website only allows for users that are logged in to access the network (for longer than 10s) using JWT | yes |  |
| the website has a post system, that includes image, title, subtrenditt and date | yes |  |
| the website allows for a like and comment system, which also allows to edit comment or remove like | yes |  |
| the website includes interactive feed that only displays posts of the subtrenditts followed | yes |  |
| the website shows artificial trends in the popular by analysing trends. | yes |  |
|  |  |  |                                               


## Reccomendations : Looking forward


### 1. Chat with other users

### 2. Further expansion of cities/subreddits

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

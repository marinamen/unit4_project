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
1. “Beautiful CSS Buttons Examples - CSS Scan.” 92 Beautiful CSS Buttons Examples - CSS Scan, https://getcssscan.com/css-buttons-examples. 
2. “Flask HTTP Methods, Handle GET &amp; Post Requests.” GeeksforGeeks, GeeksforGeeks, 2 Feb. 2023, https://www.geeksforgeeks.org/flask-http-methods-handle-get-post-requests/. 
3. “Cirrus CSS.” Cirrus, https://www.cirrus-ui.com/buttons/basics. 
4. Auth0. “JSON Web Tokens.” Auth0 Docs, https://auth0.com/docs/secure/tokens/json-web-tokens. 
5. “How to - Search Bar.” How To Create a Search Bar, https://www.w3schools.com/howto/howto_css_searchbar.asp.


## SUCCESS CRITERIA 1 : An encrypted login/registration system.

In order for Trenditt to operate within the minimum viable product it needs to have an account system, like the standard website it has two options **Login** or **Register**. Within these it allows to create or gain access to an already created account, for our users information to be secure we also introduced a set of security measures that the users information is subjected to in order to eliminate any risk of external threat or misuse of information.

To start the a webpage there is certain things to take into account:

**LOGIN SYSTEM**
```.py
@app.route('/login', methods=['GET', 'POST'])
```
App route, so into what adress from our website this page is saved under, in this case it would be under **"website/login.httml"** and the methods allowed. Essentially what this means is that within this page of our website there will be certain usages that will require the information to be fetched, updated or saved in the database, hence `GET` in order to retrieve information, `POST` in order to save and update what is written by the user. *Important note is that the code for the website in order to be functional it needs to be saved within a function of the page's name*

Within our login function:

A connection with our Database function is established following the usual protocol shown below.
```.py
    db = DatabaseWorker('unit4.db')
```
Following this we will now set what happens when a button is clicked within the website that needs information or verification from the database. In this case since it is a login we will use an if that is complied whenever a button that requires something to be verified with the database so it would be triggered when the `LOGIN` button is clicked after the user has inputted their information.

```.py
    if request.method == 'GET':
        uname = request.form.get('uname')
        password = request.form.get('psw')
```
As I mentioned before when the website requires infomation from the database it will trigger the `GET` method and this will retrieve the information inputted in the text inputs  of *uname* and *password* and save it under the two variables shown above.

Next step is to verify whether the information inputted by the user matches the previous credentials. In order to do this we use our connection with the database to retrieve information with our Database Worker class. Using the function within it run_query that as the name says will run the SQL query, and in this case it will fetch the information where the username equals the one inputted and then will use index [0] for the id and [1] for the password. 
```.py
        user = db.run_query("SELECT id, password FROM users WHERE username = ?", (uname,))
        if user and check_password_hash(user[1], password):
```
After this comes the most crucial part the actual verification of the user's credential, I used an if loop since it is simple and perfectly fitting for this condition. If user exists, meaning if the query retrieved any information from the database using the inputted username then it will check the password. Since the password is saved hashed, using sha256 encryption, the method i used to check was a function I had previously created called check_hash which simply dehashes the encryption and compares the result with the unhashed inputted password, returning `true[1]` or `false[0]`.

```.py
def checkHash(text: str, hashed: str) -> bool:
    return hasher.verify(text, hashed)
```

When a true is returned the code that follows runs, it indexes the first value of user which would be the id and saves it under the `user_id`  . It then redirects the page to the home page and in order for the website to be altered and saved under a user, it sets a cookie in the user's browser  with the user id. 
```.py
    user_id = user[0]
    response = make_response(redirect(url_for('trenditt_home')))
    response.set_cookie('user_id', str(user_id))
    token = jwt.encode({'user_id': user_id, 'exp': datetime.utcnow() + timedelta(minutes=45)}, token_key, algorithm = 'HS256')
    session['token'] = token
```
The first argument, `user_id`, is the name of the cookie, this is the key that will be used to retrieve the cookie's value later. The second argument, `str(user_id)`, is the value of the cookie. The user ID is converted to a string and stored in the cookie. 

Next under `token` a JSON Web Token (JWT) is created to securely store the user's ID and an expiration time. The token is generated with the user's id and set to expire in 45 minutes, this token is then stored in the user's session. This allows the application to verify the user's identity and session validity on subsequent requests.

Lastly if the conditions required are not met it an error pops up.
```.py
  return render_template('login.html', error='Invalid username or password')
```

**REGISTRATION SYSTEM**


in Fig.14 The function takes the usernamme,city,email and a password which is then encrypted before storing everything into user database. we see that after running the query and successfully storing the infromation of the newly registered user, a user is redirected to the login page where it can access the website using credentials of the newly registered account. When developing this part of code using generalisation I was able to recognize a way to solve one of the criteria requirements by including a option bar in the registration where a user would input the city which he would write about. This helped with solving the problem of seeing irellevent content creators that are not located in my city.


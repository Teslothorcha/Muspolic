# Muspolic!

Hi!  this project was created for fun so you can enjoy it, **Muspolic** is an interactive platform to create polls about the albums of your favorite artists. Users just need to log in and insert the Album's Spotify URI they want to postulate so others users can vote on it, in the same way the user can vote on polls created by the community. Start **Muspolicing**  and discover music everyday.

# TECHNOLOGIES
These are the technologies implemented on this project
- **Python** : back-end programming language.
- **Spotipy**: lightweight Python library for the [Spotify Web API]
- **MySQL**: relational database management.
- **Django**: python web framework.
- **Bootstrap**: Framework for HTML and CSS.
- **Digital ocean**: Linux-based virtual machine (VM).
- **Nginx**: open source software for web serving.
- **Gunicorn**: stand-alone WSGI web application server

# LIVE
This project is live right now http://www.teslothorcha.tech/pages/

# RUN IT LOCALLY

If you made it this far most likely you are tech savvy and if not I'm glad you are cheeking this. This project was build with Django meaning that if you want to add some features to this project or customize it you will code it on python.

Below you would see the changes you will need to apply in order to run Muspolic on your pc.



## Key factors to run it locally

First you will need to install python and some packages that will let use a virtual environment to run this project.
> <p>sudo apt-get install python3-pip</p>
> <p>sudo pip3 install virtualenv </p>

Clone this repo and create a virtual environment inside of it
> <p>virtualenv thisproject_env </p>

to activate your environment simply enter
> source thisproject_env/bin/activate

Now you will you shell prompt something like this
> (thisproject_env) current/path:$

In the root of this project there is a file called "requirements.txt", this file will help you install the modules needed to run the project. You would do so by entering the following command 
> (thisproject_env) current/path:$ pip install -r requirements.txt


Now you will to change is on the project is the environment. Django allows two kind of environments development and production, both of these are handled by one variable called "DEBUG" that is located on:
> muspolic
>----------settings.py

You will need to set DEBUG = True, meaning that you will run it on development so Django can tell you about errors and is easier to debug. By setting this variable value to "True" you are also activating a conditional for the DATABASES variable located in this same file. This will activate SQLite an embedded database software for local/client storage. With those changes being made you are missing only one last thing, to create a file called credentials.py inside muspolic folder with the following variables.
><p>g_app_email = 'the email used to password recovery process'</p>
><p>g_app_pass = 'google's password for app use (if you chose gmail above)'</p>
><p>sp_clinet_id = "your Spotify client app id"</p>
><p>sp_client_st = "Your Sporify client app secret"</p>
><p>sp_redirect_uri = "http://127.0.0.1:8000/polls/"</p>

In these links you can create your spotify own app credentials and google app password
- https://developer.spotify.com/dashboard/
-  https://support.google.com/accounts/answer/185833?hl=en

Now you need to tell Django to migrate the models on the project to the database.
> <p> (thisproject_env) current/path:$ python manage.py makemigrations </p>
> <p> (thisproject_env) current/path:$ python manage.py migrate</p>

Finally run it on your pc by entering
> <p> (thisproject_env) current/path:$ python manage.py runserver</p>

You can check your muspolic version on http://127.0.0.1:8000/

# AUTHORS
- <a href="http://juandavidmarinbernal.me/">Juan David Marin Bernal </a>
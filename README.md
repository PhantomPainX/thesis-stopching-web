# thesis-stopching-web
Stopching Web Services

# Setting-up

1. Create virtual enviroment

`$ virtualenv env`

2. Activate virtual enviroment

  + Windows
  
    `$ env\Scripts\activate`
    
  + Linux/MacOS
  
    `$ source env/bin/activate`
    
3. Install packages

`$ pip install > requirements.txt`

4. Create database

`mysql> create database stopching;`

5. Comment everything in models.py and admin.py

6. Execute first migration

`$ python manage.py makemigrations`
`$ python manage.py migrate`

7. Uncomment everything in models.py and admin.py and migrate again

`$ python manage.py makemigrations main_app`
`$ python manage.py migrate main_app`

8. Create the following folders

+ `stopching/media/`
+ `stopching/static/`

9. Run

`$ python manage.py runserver`
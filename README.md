# Favourite Recipes

This is a toy web applications for me to learn some HTML, CSS and Django.
The website is intended to store and manage cooking recipes.

## Installation

Installation of the python packages in your (local) environment.

```bash
pip install django>=5.0.7
pip install Pillow>=10.4.0
pip install djangorestframework>=3.15.2
pip install markdown>=3.6 
pip install django-filter>=24.3
```

And start the test-server on `http://127.0.0.1:8000/` with ``python manage.py runserver`` .


## Features

You can upload your recipes in a form to separate entries like ingredients, cooking time, image etc.
The recipes can be searched, sorted and also filtered by their assigned topics. They are rendered in an HTML template from the database with ingredients calculated based on the number of persons.
Topics are to be created by the admin ``python manage.py createsuperuser`` . And by visiting the `/admin` url.
You can also access/export the database via REST API at url `/api` and `/api/recipes` in json format.  

Example of the website.

<p align="center">
  <img src="https://github.com/PatReis/fav_reps/blob/main/static/images/example_6.jpg" />
</p>
<p align="center">
  <img src="https://github.com/PatReis/fav_reps/blob/main/static/images/example_4.jpg" />
</p>
<p align="center">
  <img src="https://github.com/PatReis/fav_reps/blob/main/static/images/example_5.jpg" />
</p>

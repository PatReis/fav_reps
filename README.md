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

You can upload your recipes, rate and like them and generate your personal cooking book.
You can discuss cooking in a forum tab and link videos to your recipe. 
The recipes can be searched, sorted and also filtered by their topics. 
Topics are to be created by the admin ``python manage.py createsuperuser`` . And by visiting the `/admin` url.


Example of the website.

<p align="center">
  <img src="https://github.com/PatReis/fav_reps/blob/main/static/images/example_1.jpg" width="80%"/>
</p>
<p align="center">
  <img src="https://github.com/PatReis/fav_reps/blob/main/static/images/example_2.jpg" width="80%" />
</p>
<p align="center">
  <img src="https://github.com/PatReis/fav_reps/blob/main/static/images/example_3.jpg" width="80%" />
</p>
<p align="center">
  <img src="https://github.com/PatReis/fav_reps/blob/main/static/images/example_4.jpg" width="80%" />
</p>
<p align="center">
  <img src="https://github.com/PatReis/fav_reps/blob/main/static/images/example_5.jpg" width="80%" />
</p>
<p align="center">
  <img src="https://github.com/PatReis/fav_reps/blob/main/static/images/example_6.jpg" width="80%" />
</p>

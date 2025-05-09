# Favourite Recipes

This is a toy web applications for me to learn some HTML, CSS and Django.

Version [1.x.x](https://github.com/PatReis/fav_reps/releases/tag/v1.2.1) only features the basic recipe forms. 
It is intended to be hosted in a private network to store and manage your personal cooking recipes.


## Features

You can upload your recipes in a form to separate entries like ingredients, cooking time, image etc.
The recipes can be searched, sorted and also filtered by their assigned topics. They are rendered in an HTML template from the database with ingredients calculated based on the number of persons.
Topics are to be created by the admin ``python manage.py createsuperuser`` . And by visiting the `/admin` url.
You can also access/export the database via REST API at url `/api` and `/api/recipes` in json format and further as LaTeX book.  

## Example

<p align="center">
  <img src="https://github.com/PatReis/fav_reps/blob/v1/static/images/example_1.jpg" />
</p>
<p align="center">
  <img src="https://github.com/PatReis/fav_reps/blob/v1/static/images/example_2.jpg" />
</p>

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

# Serving on Raspberry Pi 

I wanted access in a private network also for mobile devices and therefore to set up a Raspberry Pi.
So only for testing, not valid for public network (you also might want to switch to other database).
This also serves as a memo to myself. Here are the steps that I [followed](https://pimylifeup.com/raspberry-pi-django/) with [reference](https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/modwsgi/):

Install the desired OS for your Raspberry Pi with the [Raspberry Pi Imager](https://www.raspberrypi.com/software/), for example mine is model 2B. 
It is helpful to already set an admin with password, hostname and enable SSH when writing the image on SSD.
My username was 'patrick', change to your admin user in the following steps.
With the full desktop image, python is already installed, otherwise one may have to install python beforehand separately.

Install `apache2` and `wsgi` mod. Activate it and restart apache server.

```bash
sudo apt-get upgrade
sudo apt-get update
sudo apt install apache2 -y
sudo apt install libapache2-mod-wsgi-py3
sudo a2enmod wsgi
sudo systemctl restart apache2
```

If something goes wrong, check the error log at `/var/log/apache2/error.log` .
Make a folder to store the apps in your home folder (replace 'patrick' with your username). 

```bash
mkdir /home/patrick/django-apps
```

Copy the directories of this repo into `django-apps` (`/home/patrick/django-apps/fav-reps/`).
Either by SFTP with tools like [WinSCP](https://winscp.net/eng/download.php) or [FileZilla](https://filezilla-project.org/download.php?type=client) or directly from GitHub:

```bash
cd /home/patrick/django-apps
git clone https://github.com/PatReis/fav_reps
```
Note that I found it helpful to name the main directory other than your app.
E.g. 'fav_reps' vs. 'favourite_recipes' because otherwise I encountered some annoying import errors with for example [settings.py](favourite_recipes/settings.py).

Create a python environment in `django-apps` and activate it (always activate it to install packages).
And then install the packages necessary for django.

```bash
cd /home/patrick/django-apps
python3 -m venv djenv
source djenv/bin/activate
python3 -m pip install django
python3 -m pip install Pillow
python3 -m pip install djangorestframework
python3 -m pip install markdown
python3 -m pip install django-filter
```
Now adjust your apache2 config file like the file in this repo [000-default.conf](000-default.conf). 
Replace username 'patrick' with your username.

```bash
sudo nano /etc/apache2/sites-enabled/000-default.conf
```

With this apache2 conf file, the django app will be available in your network at `http://<your Raspberry's IP>/favourite_recipes/` .
To find out the Raspberry's IP address you can use ``hostname -I`` .

You also have to modify the [settings.py](favourite_recipes/settings.py) to point to your Raspberry Pi's IP address.

```bash
sudo nano /home/patrick/django-apps/fav_reps/favourite_recipes/settings.py
```

Change the python variable ``ALLOWED_HOSTS = ["???.???.???.??"]`` to your Raspberry Pi's IP address.

Finally, give access to media and database.

```bash
cd /home/patrick/django-apps/
sudo chmod 755 fav_reps
sudo chmod 755 fav_reps/db.sqlite3
sudo chmod 755 fav_reps/media
```

If necessary you can also change ownership.

```bash
cd /home/patrick/django-apps/
sudo chown :www-data fav_reps
sudo chown :www-data fav_reps/db.sqlite3 
sudo chown :www-data fav_reps/media 
```

> [!WARNING]  
> Just for private network. Be careful with read/write permissions like that.

Restart server.

```bash
sudo systemctl restart apache2
```

Now it should work.

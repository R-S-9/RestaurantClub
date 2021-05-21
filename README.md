# RestaurantClub
Applications for choosing a restaurant by dish.
## Features
* Ready service for finding dishes according to your request
* Offers of rated restaurants that are worthy of your attention
* Comments describing establishments and dishes from all sides
# Instructions for the developer
## Download repository
```
cd src
git clone https://github.com/R-S-9/RestaurantClub.git
```
## Launch surrounded by the developer
Create a database in PostgreSQL and point to `settings.py`. Example:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''
    }
}
```
Launch:
```
cd src
python manage.py runserver --insecure
```

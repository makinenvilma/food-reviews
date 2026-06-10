# Food Reviews

A multilingual (Finnish/English) restaurant review site built with Django and Wagtail. Reviews are shown as cards with star ratings, and content is managed through the Wagtail admin.

## Features

- Review cards on the front page (restaurant name, star rating 1-5, image)
- Individual review pages with rich text, categories, and tags
- Multilingual support (`wagtail-localize`) with a language switcher
- SCSS theme (red/yellow palette, card layout)

## Tech stack

- Django 5.2 + Wagtail 7.0
- SQLite (dev)
- SCSS via django-sass-processor
- wagtail-localize
- Python 3.13+

## Installation

```bash
cd mysite
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Site: http://localhost:8000 - Admin: http://localhost:8000/admin

## Adding a review

1. Admin -> Pages -> Ruoka-arvostelut
2. Add child page -> Blog Page
3. Fill in title, restaurant_name, rating, date, intro, body, optional gallery images
4. Publish

## Localization

The default language (FI) is served without a URL prefix; English is served under `/en/`. To translate a page, open it in the admin, choose More -> Translate, pick the target language, edit, and publish.

## Styles

SCSS source lives in `mysite/static/scss/mysite.scss` and is compiled automatically in dev. For production:

```bash
python manage.py compilescss
python manage.py collectstatic
```

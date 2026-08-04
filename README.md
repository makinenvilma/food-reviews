# Food Reviews

A restaurant review site built with Django and Wagtail. Every review rates the place
from one to five stars and splits the write-up into taste, sides, service and an
overall verdict, which keeps reviews written months apart comparable. Content is
written in the Wagtail admin and exists in both Finnish and English.

## Status

Working and in use, with real reviews in the database.

Working right now:

- Front page listing reviews as cards, with star rating and photo
- Filtering the list by location and by minimum star rating
- Review pages with separate taste, sides, service and overall sections
- Photo galleries with captions
- Tags, plus a tag index page for browsing by tag
- Authors as reusable snippets
- Finnish and English side by side, Finnish at the root and English under `/en/`

Not done yet:

- SQLite only, which is fine locally but not for hosting.
- No tests. `blog/tests.py` is still the file Django generated.
- Interface texts are written straight into the templates as `{% if is_en %}` checks
  instead of proper Django translations, which does not scale to more strings.
- No `.gitignore`, so the database and all uploaded images are committed to the repo.
- `pyproject.toml` in the root is leftover Poetry boilerplate and is unrelated to the
  site.

## Tech

Django 5.2 and Wagtail 7.0, with wagtail-localize handling the two languages. Styles
are SCSS compiled by django-sass-processor, which recompiles automatically while the
dev server runs. Python 3.13 or newer.

The review model lives in `blog/models.py`. Star rendering is a `stars` property on
the page, and the location and rating filters are handled in `BlogIndexPage.get_context`.

## Running it

```bash
cd mysite
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Site at http://localhost:8000, admin at http://localhost:8000/admin.

The database is committed to the repo, so the reviews are there from the start. You
will need your own admin account to edit anything:

```bash
python manage.py createsuperuser
```

## Layout of the code

```
mysite/
  blog/
    models.py           BlogPage, BlogIndexPage, tags, authors, gallery
    templates/blog/     list, single review, tag index
    templatetags/       locale_pageurl for the language switcher
  home/                 front page
  search/               search view
  mysite/
    settings/           base, dev, production
    static/scss/        mysite.scss, the red and yellow theme
  media/                uploaded images
```

## Writing a review

In the admin, go to Pages, then Ruoka-arvostelut, and add a child page of type Blog
Page. Fill in the restaurant, location, product and price, pick a star rating and a
date, then write the taste, sides, service and overall sections. Add gallery images
at the bottom. Publish.

To make an English version, open the page and choose More, then Translate.

## Next up

1. Tests, starting with the filters on the index page
2. Move interface texts into real translation files
3. A `.gitignore` and the database out of version control
4. PostgreSQL and somewhere to host it

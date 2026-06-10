# Food Reviews

A multilingual (Finnish/English) restaurant review site. Built with Django and Wagtail, featuring an SCSS-based theme and a card-style review listing with star ratings.

## Features

- **Review cards on the front page** — restaurant name, star rating (1–5), and image/placeholder
- **Individual review pages** — full review with rich text, categories, and tags
- **Multilingual support** (`wagtail-localize`) — separate page trees for Finnish and English, language switcher in the header
- **Themed UI** (SCSS) — red/yellow palette, card layout, modern rounded corners
- **Wagtail CMS** — browser-based content management; add and translate pages via the admin panel

## Tech stack

| Area           | Technology                       |
|----------------|----------------------------------|
| Backend        | Django 5.2 + Wagtail 7.0         |
| Database       | SQLite (dev)                     |
| Styles         | SCSS (django-sass-processor)     |
| Localization   | wagtail-localize                 |
| Python         | 3.13+                            |

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

The site is available at http://localhost:8000 and the admin at http://localhost:8000/admin.

## Site structure

```
/                              (FI home — Ruoka-arvostelut)
├── /kamppi-burger/            (individual review)
├── /itakeskus-salad/
└── /tagit/                    (tag index)

/en/                           (EN home — Food Reviews)
├── /en/kamppi-burger/
├── /en/itakeskus-salad/
└── /en/tags/
```

URL configuration uses `i18n_patterns(prefix_default_language=False)`, so the default language (FI) serves without a prefix and other languages are served under `/en/`.

## Page models

Defined in `blog/models.py`.

### `BlogIndexPage`
The home page that lists all reviews in a card grid.
- `intro` — introductory text (rich text)
- Children: all `BlogPage` instances

### `BlogPage` (review)
| Field             | Type                      | Description                                    |
|-------------------|---------------------------|------------------------------------------------|
| `title`           | CharField                 | Post title                                     |
| `restaurant_name` | CharField (120)           | Restaurant name (shown on the card)            |
| `rating`          | PositiveSmallIntegerField | Stars 1–5 (default 5)                          |
| `date`            | DateField                 | Review date                                    |
| `intro`           | CharField (250)           | Short intro                                    |
| `body`            | RichTextField             | Free-form review text                          |
| `authors`         | ParentalManyToMany        | Authors (Author snippet)                       |
| `tags`            | ClusterTaggableManager    | Tags                                           |
| `gallery_images`  | InlinePanel               | Gallery images (first one used as card image)  |

The `stars` property returns rendered stars, e.g. `★★★★☆`.

## Styles

SCSS source: `mysite/static/scss/mysite.scss`

Compiled automatically in dev mode by `django-sass-processor`. For production builds, run:

```bash
python manage.py compilescss
python manage.py collectstatic
```

### Color variables

```scss
$brand-red:    #DA291C;
$brand-yellow: #FFC72C;
$brand-dark:   #292929;
$brand-bg:     #FFFBF2;
```

### Key CSS classes

| Class                       | Purpose                                       |
|-----------------------------|-----------------------------------------------|
| `.page-content`             | Main content container (max-width 880 px)     |
| `.review-grid`              | Front-page card grid                          |
| `.review-card`              | Individual review card                        |
| `.review-card__placeholder` | Image placeholder (yellow with red accent)    |
| `.lang-switch`              | Language switcher                             |

## Localization

### Configuration

`mysite/settings/base.py`:
```python
LANGUAGE_CODE = "fi"
LANGUAGES = [("fi", "Suomi"), ("en", "English")]
WAGTAIL_CONTENT_LANGUAGES = LANGUAGES
WAGTAIL_I18N_ENABLED = True
```

`wagtail_localize` and `wagtail_localize.locales` are added to `INSTALLED_APPS`. `django.middleware.locale.LocaleMiddleware` is added to `MIDDLEWARE`.

### Translating a page

1. Open the page in the Wagtail admin (http://localhost:8000/admin)
2. Click **More → Translate**
3. Choose the target language (EN)
4. Edit the fields in English
5. Publish

### Language switcher

Custom template tag `blog/templatetags/locale_tags.py` returns the URL of a translated page:

```python
@register.simple_tag
def locale_pageurl(page):
    return page.specific.get_url() or "/"
```

Used in `base.html`:
```django
{% for translation in page.get_translations.live %}
    <a href="{% locale_pageurl translation %}">{{ translation.locale.language_code|upper }}</a>
{% endfor %}
```

## Adding a new review

### Via the admin
1. http://localhost:8000/admin → **Pages → Ruoka-arvostelut**
2. **Add child page → Blog Page**
3. Fill in: title, restaurant_name, rating, date, intro, body, optional gallery_images
4. **Publish**

### Programmatically
```python
from datetime import date
from blog.models import BlogIndexPage, BlogPage

parent = BlogIndexPage.objects.first()
review = BlogPage(
    title="Restaurant Tikkurila - Burger review",
    slug="tikkurila-burger",
    date=date.today(),
    restaurant_name="Restaurant Tikkurila",
    rating=3,
    intro="A decent experience, nothing extraordinary.",
    body="<p>At the Tikkurila restaurant...</p>",
)
parent.add_child(instance=review)
review.save_revision().publish()
```

## Directory layout

```
food-reviews/
├── README.md                          (this file)
└── mysite/
    ├── manage.py
    ├── requirements.txt
    ├── db.sqlite3
    ├── venv/                          (local virtual environment)
    ├── blog/
    │   ├── models.py                  (BlogIndexPage, BlogPage, Author)
    │   ├── migrations/
    │   ├── templates/blog/
    │   │   ├── blog_index_page.html
    │   │   ├── blog_page.html
    │   │   └── blog_tag_index_page.html
    │   └── templatetags/
    │       └── locale_tags.py
    ├── home/                          (deprecated HomePage model)
    ├── search/
    └── mysite/
        ├── settings/
        │   ├── base.py
        │   ├── dev.py
        │   └── production.py
        ├── static/scss/
        │   └── mysite.scss
        ├── templates/
        │   └── base.html
        └── urls.py
```

## Dependencies

`mysite/requirements.txt`:
- `Django>=5.2,<5.3`
- `wagtail>=7.0,<7.1`
- `django-sass-processor>=1.4,<2.0`
- `libsass>=0.23,<0.24`
- `wagtail-localize>=1.13,<2.0`

## Development tips

- **SCSS changes don't appear:** Touch the source file (`touch mysite/static/scss/mysite.scss`) or remove the cached `static/scss/mysite.css`.
- **New template tag not loading:** Restart `runserver` — Django reads `templatetags` modules only on startup.
- **Switching locale breaks URLs:** Make sure `LocaleMiddleware` is placed after `SessionMiddleware` and before `CommonMiddleware`.
- **EN page not visible:** Verify the page is published (`live=True`) and its `locale` is set to English.

## Changes from the original blog template

1. **Review-themed content** — removed old sample posts, renamed the site, added example reviews.
2. **Front-page card view** — extended `BlogPage` with `restaurant_name` and `rating` fields; the index page now renders as a card grid.
3. **Removed Wagtail's default Home page** — `BlogIndexPage` is now the site root.
4. **SCSS theme** — red/yellow color palette, cards, placeholder graphics.
5. **Localization** — wagtail-localize, language switcher, separate page trees per locale.

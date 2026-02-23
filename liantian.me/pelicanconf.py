AUTHOR = 'liantian'
SITENAME = "LIANTIAN's LOG"
SITEURL = 'http://127.0.0.1:8000'

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'cn'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

MARKDOWN = {
    'extensions' : ['markdown.extensions.codehilite', 'markdown.extensions.extra', 'markdown.extensions.admonition'],
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight','guess_lang': 'False', 'linenums': 'True'},
    },
    'output_format': 'html5',
}

MANGLE_EMAILS = True
# Blogroll
LINKS =  (('Home','/index.html'),
('About Me','/pages/about.html'),)

# Social widget
SOCIAL = SOCIAL = (
                ('Feed','/feeds/all.atom.xml'),
                # ('Email','mailto:xxx@gmail.com'),
                ('GitHub','http://github.com/liantian-cn'),
                ('Twitter','https://twitter.com/liantian-cn'),
                )



# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = './themes/voce/'                          # make sure path points to folder where you cloned the theme
DEFAULT_DATE_FORMAT = "%b %d, %Y"                 # short date format, optional but recommended 
USER_LOGO_URL = "/images/5621496.gif"  # change URL to point to desired logo for site


DEFAULT_PAGINATION = 8

RELATIVE_URLS = True
DELETE_OUTPUT_DIRECTORY = True
OUTPUT_RETENTION = [".git"]

DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = False
SUMMARY_MAX_LENGTH = 50


ARCHIVES_URL = "archives.html"
ARCHIVES_SAVE_AS = 'archives.html'
ARTICLE_URL = 'articles/{slug}.html'
ARTICLE_SAVE_AS = 'articles/{slug}.html'
PAGE_URL = 'pages/{slug}.html'
PAGE_SAVE_AS = 'pages/{slug}.html'
TAGS_URL = 'tag/{slug}.html'



AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
CATEGORY_SAVE_AS = ''
CATEGORIES_SAVE_AS = ''
STATIC_PATHS = [
'images',
'files',
'extra/robots.txt',
'extra/favicon-16x16.png',
'extra/favicon-32x32.png',
'extra/CNAME',
]
 
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon-16x16.png': {'path': 'favicon-16x16.png'},
    'extra/favicon-32x32.png': {'path': 'favicon-32x32.png'},
    'extra/CNAME': {'path': 'CNAME'}
    }


GOOGLE_ANALYTICS_ID = 'UA-69272843-2'
# GOOGLE_ANALYTICS_PROP = 
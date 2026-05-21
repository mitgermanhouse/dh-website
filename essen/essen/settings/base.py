"""
Base Settings file.
"""

import os

from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Application definition
INSTALLED_APPS = [
    "home.apps.HomeConfig",
    "faqs.apps.FaqsConfig",
    "recipes.apps.RecipesConfig",
    "menu.apps.MenuConfig",
    "alumni.apps.AlumniConfig",
    "admin_interface",
    "colorfield",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "widget_tweaks",
    "crispy_forms",
    "crispy_bootstrap5",
    "easy_thumbnails",
    "easy_thumbnails.optimize",
    "adminsortable",
    "django_cleanup.apps.CleanupConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "mit.auth.KerbRemoteUserMiddleware",
    "home.middleware.CreateProfileMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "mit.auth.KerbRemoteUserBackend",
    "django.contrib.auth.backends.ModelBackend",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.static",
            ],
            "libraries": {
                "essen_base_tags": "essen.templatetags.base_tags",
            },
        },
    },
]

ROOT_URLCONF = "essen.urls"
WSGI_APPLICATION = "essen.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = "/home"

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
MEDIA_URL = "/media/"
STATIC_URL = "/static/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Easy Thumbnails
THUMBNAIL_BASEDIR = "thumbs"
THUMBNAIL_ALIASES = {
    "home": {
        "avatar": {"size": (750, 750), "crop": False},
        "carousel": {"size": (1920, 1080), "crop": "smart"},
    },
}

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Required by admin_interface
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

# Bootstrap Messages
MESSAGE_TAGS = {
    messages.DEBUG: "alert-secondary",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}


#TODO: YC's comment - Putting the URL in the settings instead of hardcoding it in the HTML is a good idea. 
#  This is ok, but I imagine we have a couple of other key-value pairs scattered in the HTML templates right now
#  that could benefit from this organization, so perhaps it would be good to group this under a section, e.g. 
# External content (such as i3 videos) or a dictionary. You could also add some way of updating these pairs in the CMS (overkill for this, but maybe good for i3 video).
  
# External Links
EXTERNAL_CONTENT ={
    'ALUMNI_FORM_URL': "https://docs.google.com/forms/d/e/1FAIpQLSfEGCG-j4cafu4-mMhyeebDZFl9j_XJzzQNxnl18j_--ZraXA/viewform?usp=publish-editor",
    'I3_VIDEOS': { 2024: {"url": "TfJ4DCnrups",
                          "source": "YouTube"},
                   2023: {'url': "851610025",
                          "source": "Vimeo"},
                   2022: {'url': "731080849",
                          "source": "Vimeo"},
                   2021: {'url': "562801172",
                          "source": "Vimeo"},
                   2020: {'url': "417246220",
                          "source": "Vimeo"},
                   2019: {'url': "333324282",
                          "source": "Vimeo"},
    }
}
# ALUMNI_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfEGCG-j4cafu4-mMhyeebDZFl9j_XJzzQNxnl18j_--ZraXA/viewform?usp=publish-editor"
"""
Django settings for Connect project.

Generated by 'django-admin startproject' using Django.

For more information on this file, see
https://docs.djangoproject.com/en/stable/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/stable/ref/settings/
"""

import string
from copy import deepcopy
from pathlib import Path

import dj_database_url
from configurations import Configuration, values


class ProjectDefault(Configuration):
    """
    The default settings from the Django project template.

    Django Configurations
    https://django-configurations.readthedocs.io
    """

    # Build paths inside the project like this: BASE_DIR / "subdir".
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.SecretValue()

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(True)

    ALLOWED_HOSTS = values.ListValue([])

    # Application definition

    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
    ]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "connect.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    WSGI_APPLICATION = "connect.wsgi.application"

    # Database
    # https://docs.djangoproject.com/en/stable/ref/settings/#databases

    DATABASES = {
        "default": dj_database_url.config(),
    }

    # Password hashing
    # https://docs.djangoproject.com/en/stable/topics/auth/passwords/

    PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.Argon2PasswordHasher",
        "django.contrib.auth.hashers.PBKDF2PasswordHasher",
        "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
        "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
        "django.contrib.auth.hashers.ScryptPasswordHasher",
    ]

    # Password validation
    # https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
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

    # Internationalization
    # https://docs.djangoproject.com/en/stable/topics/i18n/

    LANGUAGE_CODE = "en-us"

    TIME_ZONE = "UTC"

    USE_I18N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/stable/howto/static-files/

    STATIC_URL = "static/"

    STATIC_ROOT = BASE_DIR / "static"

    # Default primary key field type
    # https://docs.djangoproject.com/en/stable/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    # Stored files
    # https://docs.djangoproject.com/en/stable/topics/files/

    # Uncomment when using local media

    # MEDIA_URL = "/media/"

    # MEDIA_ROOT = BASE_DIR / "media"

    # Email Settings
    # https://docs.djangoproject.com/en/stable/topics/email/

    ADMINS = values.SingleNestedTupleValue((("admin", "errors@connect.com"),))

    DEFAULT_FROM_EMAIL = values.EmailValue("info@connect.com")

    EMAIL_SUBJECT_PREFIX = "[Connect] "

    EMAIL_USE_LOCALTIME = True

    SERVER_EMAIL = values.EmailValue("server@connect.com")

    # Email URL
    # https://django-configurations.readthedocs.io/en/stable/values.html

    EMAIL = values.EmailURLValue("console://")

    # Cache URL
    # https://django-configurations.readthedocs.io/en/stable/values.html

    CACHES = values.CacheURLValue("locmem://")

    # Translation
    # https://docs.djangoproject.com/en/stable/topics/i18n/translation/

    # LANGUAGES = (("en", "English"), ("it", "Italiano"))

    # Clickjacking Protection
    # https://docs.djangoproject.com/en/stable/ref/clickjacking/

    X_FRAME_OPTIONS = "SAMEORIGIN"  # Default: 'SAMEORIGIN'

    # Session auth
    # https://docs.djangoproject.com/en/stable/ref/settings/#sessions

    SESSION_COOKIE_DOMAIN = values.Value()

    SESSION_COOKIE_SECURE = True

    # Secure Proxy SSL Header
    # https://docs.djangoproject.com/en/stable/ref/settings/#secure-proxy-ssl-header

    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    # CSRF Trusted Origins
    # https://docs.djangoproject.com/en/stable/ref/settings/#csrf-trusted-origins

    CSRF_TRUSTED_ORIGINS = values.ListValue([])

    LOGIN_URL = "admin:login"


class Local(ProjectDefault):
    """The local settings."""

    # Application definition

    INSTALLED_APPS = ProjectDefault.INSTALLED_APPS.copy()

    MIDDLEWARE = ProjectDefault.MIDDLEWARE.copy()

    # Django Debug Toolbar
    # https://django-debug-toolbar.readthedocs.io/en/stable/configuration.html

    try:
        import debug_toolbar  # noqa: F401
    except ModuleNotFoundError:  # pragma: no cover
        pass
    else:  # pragma: no cover
        INTERNAL_IPS = values.ListValue(["127.0.0.1"])
        INSTALLED_APPS.append("debug_toolbar")
        MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
        DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda x: True}

    # Django Extensions
    # https://django-extensions.readthedocs.io/en/stable/graph_models.html

    try:
        import django_extensions  # noqa: F401
    except ModuleNotFoundError:  # pragma: no cover
        pass
    else:  # pragma: no cover
        INSTALLED_APPS.append("django_extensions")
        SHELL_PLUS_PRINT_SQL = True
        SHELL_PLUS_PRINT_SQL_TRUNCATE = None
        GRAPH_MODELS = {
            "all_applications": True,
            "arrow_shape": "diamond",
            "disable_abstract_fields": False,
            "disable_fields": False,
            "exclude_columns": [
                "id",
            ],
            "exclude_models": ",".join(
                (
                    "AbstractBaseSession",
                    "AbstractBaseUser",
                    "AbstractUser",
                    "ContentType",
                    "LogEntry",
                    "PermissionsMixin",
                    "Session",
                    "UserGroup",
                )
            ),
            "group_models": True,
            "hide_edge_labels": True,
            "inheritance": True,
            "language": "en",
            "layout": "dot",
            "relations_as_fields": True,
            "theme": "django2018",
            "verbose_names": False,
        }


class Testing(ProjectDefault):
    """The testing settings."""

    SECRET_KEY = string.ascii_letters

    # Debug
    # https://docs.djangoproject.com/en/stable/ref/settings/#debug

    DEBUG = False

    # Application definition

    INSTALLED_APPS = ProjectDefault.INSTALLED_APPS.copy()

    # Email URL
    # https://django-configurations.readthedocs.io/en/stable/values/

    EMAIL = "dummy://"

    # Cache URL
    # https://django-configurations.readthedocs.io/en/stable/values/

    CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

    # The MD5 based password hasher is much less secure but faster
    # https://docs.djangoproject.com/en/stable/topics/auth/passwords/

    PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.MD5PasswordHasher",
    ]

    # Behave
    # https://behave-django.readthedocs.io/en/latest/installation.html

    try:
        import behave_django  # noqa: F401
    except ModuleNotFoundError:  # pragma: no cover
        pass
    else:  # pragma: no cover
        INSTALLED_APPS.append("behave_django")

    # Stored files
    # https://docs.djangoproject.com/en/stable/topics/files/

    # Uncomment when using media

    # MEDIA_ROOT = ProjectDefault.BASE_DIR / "media_test"


class Remote(ProjectDefault):
    """The remote settings."""

    # Debug
    # https://docs.djangoproject.com/en/stable/ref/settings/#debug

    DEBUG = False

    @property
    def MIDDLEWARE(self):  # pragma: no cover
        """Return the middleware settings."""
        middleware = deepcopy(ProjectDefault.MIDDLEWARE)
        try:
            # WhiteNoise
            # http://whitenoise.evans.io/en/stable/django.html

            import whitenoise  # noqa: F401
        except ModuleNotFoundError:  # pragma: no cover
            pass
        else:  # pragma: no cover
            middleware.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
        return middleware

    # Storages
    # https://docs.djangoproject.com/en/stable/ref/settings/#std-setting-STORAGES

    @property
    def STORAGES(self):  # pragma: no cover
        """Return the storage settings."""
        storages = deepcopy(ProjectDefault.STORAGES)
        try:
            # WhiteNoise
            # http://whitenoise.evans.io/en/stable/django.html

            import whitenoise  # noqa: F401
        except ModuleNotFoundError:  # pragma: no cover
            pass
        else:  # pragma: no cover
            storages["staticfiles"][
                "BACKEND"
            ] = "whitenoise.storage.CompressedManifestStaticFilesStorage"
        return storages

    # DB Transaction pooling and server-side cursors
    # https://docs.djangoproject.com/en/stable/ref/databases/#transaction-pooling-and-server-side-cursors  # noqa

    DISABLE_SERVER_SIDE_CURSORS = values.BooleanValue(False)

    @property
    def DATABASES(self):  # pragma: no cover
        """Return the databases."""
        databases = deepcopy(ProjectDefault.DATABASES)
        databases["default"][
            "DISABLE_SERVER_SIDE_CURSORS"
        ] = self.DISABLE_SERVER_SIDE_CURSORS
        return databases

    # Email URL
    # https://django-configurations.readthedocs.io/en/stable/values/

    EMAIL = values.EmailURLValue()

    # Security
    # https://docs.djangoproject.com/en/stable/topics/security/

    CSRF_COOKIE_SECURE = True

    SECURE_BROWSER_XSS_FILTER = True

    SECURE_CONTENT_TYPE_NOSNIFF = True

    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    SECURE_HSTS_PRELOAD = True

    SECURE_HSTS_SECONDS = 3_600

    X_FRAME_OPTIONS = "DENY"

    # Persistent connections
    # https://docs.djangoproject.com/en/stable/ref/databases/#general-notes

    CONN_MAX_AGE = None

    # Sentry
    # https://sentry.io/for/django/

    try:
        import sentry_sdk  # noqa: F401
    except ModuleNotFoundError:  # pragma: no cover
        pass
    else:  # pragma: no cover
        from sentry_sdk.integrations.django import DjangoIntegration

        sentry_sdk.init(
            integrations=[DjangoIntegration()],
            send_default_pii=True,
        )  # noqa

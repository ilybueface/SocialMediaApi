from .settings import *

if "LOGGING" in globals():
    if "loggers" in LOGGING and "django.request" in LOGGING["loggers"]:
        LOGGING["loggers"]["django.request"]["handlers"] = [
            h
            for h in LOGGING["loggers"]["django.request"]["handlers"]
            if h != "telegram"
        ]

    if "handlers" in LOGGING and "telegram" in LOGGING["handlers"]:
        del LOGGING["handlers"]["telegram"]

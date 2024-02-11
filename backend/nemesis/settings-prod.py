import sentry_sdk
from .settings import *
import os

DEBUG = False
ALLOWED_HOSTS = ["*"]


sentry_sdk.init(
    dsn="https://0da9f980cd1bd4398de5cb2c9b4b76c9@o4506729422848000.ingest.sentry.io/4506729426190336",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

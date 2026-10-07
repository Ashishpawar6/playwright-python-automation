"""Test configuration and test data, kept out of the tests and page objects."""
import os

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")

PASSWORD = "secret_sauce"  # public demo credentials published on the sample site

STANDARD_USER = "standard_user"
LOCKED_OUT_USER = "locked_out_user"

BACKPACK = "sauce-labs-backpack"
BIKE_LIGHT = "sauce-labs-bike-light"

import os
from flask import current_app
import pytest

from bank_api import create_app

def test_app_exists(test_client):
    assert current_app is not None

def test_app_is_testing(test_client):
    assert current_app.config['TESTING'] == True
import os

import pytest

from accounts import create_app


@pytest.fixture()
def test_client():
    app = create_app('testing')

    with app.test_client() as client:
        yield client


def test_empty_db(test_client):
    response = test_client.get('/')
    assert response.json == {'hello': 'world'}

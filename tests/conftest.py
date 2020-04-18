import pytest

from bank_api import create_app
from bank_api.models import Account, db


@pytest.fixture()
def test_client():
    app = create_app('testing')

    with app.test_client() as client:
        ctx = app.app_context()
        ctx.push()
        db.drop_all()
        db.create_all()
   
        yield client
        db.drop_all()
        ctx.pop()
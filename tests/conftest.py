import pytest
from api import create_app


@pytest.fixture
def client():
    app = create_app()

    with app.app.test_client() as client:
        yield client

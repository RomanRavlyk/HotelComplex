import pytest
from unittest.mock import MagicMock

mock_session = MagicMock

def test_get_db():
    try:
       yield mock_session
    finally:
        mock_session.remove()


@pytest.fixture
def test_mock_db_session():
    return mock_session

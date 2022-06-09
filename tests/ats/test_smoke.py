import pytest
import logging

from test_fixtures import fixtures

LOGGER = logging.getLogger(__name__)

@pytest.mark.smoke
def test_empty_test(fixtures) -> None:
    LOGGER.info("Dummy test here")
    assert True == True

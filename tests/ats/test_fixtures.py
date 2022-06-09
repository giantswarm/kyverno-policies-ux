import pytest
import logging

LOGGER = logging.getLogger(__name__)

@pytest.fixture
def fixtures():
    LOGGER.info("dummy_fixture here")
    return "ret"

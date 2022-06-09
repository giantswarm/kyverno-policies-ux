import sys
sys.path.append('../../../tests')

import yaml
from functools import partial
import time
import random
import string
import ensure
from textwrap import dedent

from ensure import silence
from ensure import silence_with_matchers

import pytest
from pytest_kube import forward_requests, wait_for_rollout, app_template

import logging
LOGGER = logging.getLogger(__name__)

@pytest.mark.smoke
def test_empty_test() -> None:
    LOGGER.info("Dummy test here")
    assert True == False

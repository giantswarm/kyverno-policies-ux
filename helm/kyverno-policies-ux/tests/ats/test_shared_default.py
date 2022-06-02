import sys
sys.path.append('../../../tests')

import json
from functools import partial
import time
import random
import string
import ensure
from textwrap import dedent

from ensure import cluster_name
from ensure import kubernetes_cluster

import pytest
from pytest_kube import forward_requests, wait_for_rollout, app_template

import logging
LOGGER = logging.getLogger(__name__)

@pytest.mark.smoke
def test_service_priority_cluster_label(kubernetes_cluster) -> None:
    """
    Checks whether our policy to prevent invalid 'giantswarm.io/service-priority' label
    values is working.
    """

    raw = kubernetes_cluster.kubectl(f"label --overwrite=true clusters.cluster.x-k8s.io {cluster_name}", output="json")

    #processed = json.loads(raw)

    LOGGER.info(f"Output of 'kubectl label' command: {raw}")
    
    assert True == False

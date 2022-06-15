from pytest_helm_charts.clusters import Cluster
from pytest_helm_charts.k8s.deployment import wait_for_deployments_to_run
import logging
import pykube
import pytest
import time

LOGGER = logging.getLogger(__name__)

# TODO: Can we take this from a central config to avoid repetition?
KYVERNO_VERSION = "v1.5.7"

@pytest.fixture(scope='module')
def fixtures(kube_cluster: Cluster):
    """
    Ensure that all prerequisites for our tests are in place.
    """

    # Cluster CRD
    LOGGER.info("Create cluster.x-k8s.io CRD")
    ret = kube_cluster.kubectl("apply", filename="cluster-crd.yaml", output_format="json")
    LOGGER.debug("Created cluster CRD")

    # Kyverno
    LOGGER.info(f"Install Kyverno {KYVERNO_VERSION}")
    ret = kube_cluster.kubectl("apply", filename=f"https://raw.githubusercontent.com/kyverno/kyverno/{KYVERNO_VERSION}/definitions/release/install.yaml", output_format="json")
    wait_for_deployments_to_run(kube_cluster.kube_client, deployment_names=["kyverno"], deployments_namespace="kyverno", timeout_sec=100)
    LOGGER.debug(f"Install Kyverno result: {ret}")

    # Our policies
    LOGGER.info("Deploy Kyverno policies for the service-priority cluster label")
    ret = kube_cluster.kubectl("apply", filename="../../policies/ux/clusters-label-service-priority.yaml", output_format="json")
    LOGGER.debug(f"Created kyverno policies result: {ret}")

    # Test cluster CR
    LOGGER.info("Create cluster.x-k8s.io/v1beta1 named 'test-cluster'")
    ret = kube_cluster.kubectl("apply", filename="test-cluster.yaml", output_format="json")
    LOGGER.debug(f"Created cluster result: {ret}")

    time.sleep(5)

    return True

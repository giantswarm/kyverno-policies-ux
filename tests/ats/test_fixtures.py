from pytest_helm_charts.clusters import Cluster
from pytest_helm_charts.k8s.deployment import wait_for_objects_condition
import logging
import pykube
import pytest
import time

LOGGER = logging.getLogger(__name__)

# TODO: Can we take this from a central config to avoid repetition?
KYVERNO_VERSION = "v1.9.0"

@pytest.fixture(scope='module')
def fixtures(kube_cluster: Cluster):
    """
    Ensure that all prerequisites for our tests are in place.
    """
    if kube_cluster.kube_client is None:
        raise Exception("kube_cluster.kube_client is None")

    # Cluster CRD
    LOGGER.info("Create cluster.x-k8s.io CRD")
    ret = kube_cluster.kubectl("apply", filename="cluster-crd.yaml", output_format="json")
    LOGGER.debug("Created cluster CRD")

    # Organization CRD
    LOGGER.info("Create Organization CRD")
    ret = kube_cluster.kubectl("apply", filename="https://raw.githubusercontent.com/giantswarm/organization-operator/main/config/crd/security.giantswarm.io_organizations.yaml", output_format="json")
    LOGGER.debug(f"Created Organization CRD: {ret}")

    # Kyverno
    LOGGER.info(f"Install Kyverno {KYVERNO_VERSION}")
    ret = kube_cluster.kubectl("apply --server-side", filename=f"https://github.com/kyverno/kyverno/releases/download/{KYVERNO_VERSION}/install.yaml", output_format="json" )

    wait_for_objects_condition(
        kube_client=kube_cluster.kube_client,
        obj_type=pykube.Deployment,
        obj_names=["kyverno"],
        objs_namespace="kyverno",
        obj_condition_func=lambda d: int(d.obj["status"].get("readyReplicas", 0)) > 0,
        timeout_sec=100,
        missing_ok=False
    )
    LOGGER.debug(f"Install Kyverno result: {ret}")

    # Our policies
    LOGGER.info("Deploy Kyverno policies for the service-priority cluster label")
    ret = kube_cluster.kubectl("apply", filename="../../policies/ux/clusters-label-service-priority.yaml", output_format="json")
    LOGGER.debug(f"Created cluster service priority policies result: {ret}")
    ret = kube_cluster.kubectl("apply", filename="../../policies/ux/organization-deletion-when-has-clusters.yaml", output_format="json")
    LOGGER.debug(f"Created organization deletion policies result: {ret}")

    # Create Organization namespace
    LOGGER.info("Create namespaces named 'org-giantswarm' and 'org-empty'")
    ret = kube_cluster.kubectl("apply", filename="test-organization.yaml", output_format="json")
    LOGGER.debug(f"Created giantswarm organization and its namespace: {ret}")
    ret = kube_cluster.kubectl("apply", filename="test-empty-organization.yaml", output_format="json")
    LOGGER.debug(f"Created empty organization and its namespace: {ret}")

    # This block is commented because test fail but I can't figure out why. If someone with Python experience could help, please let me know.
    # Patch Organizations so that they contain their namespace on their status field, like organization-operator does
    # ret = kube_cluster.kubectl("patch organization giantswarm --subresource status --type merge --patch '\{\"status\": \{\"namespace\": \"org-giantswarm\"\}\}'")
    # LOGGER.debug(f"Patched giantswarm organization status with namespace: {ret}")
    # ret = kube_cluster.kubectl("patch organization empty --subresource status --type merge --patch '\{\"status\": \{\"namespace\": \"org-empty\"\}\}'")
    # LOGGER.debug(f"Patched empty organization status with namespace: {ret}")

    # Test cluster CR
    LOGGER.info("Create cluster.x-k8s.io/v1beta1 named 'test-cluster'")
    ret = kube_cluster.kubectl("apply", filename="test-cluster.yaml", output_format="json")
    LOGGER.debug(f"Created cluster result: {ret}")

    time.sleep(5)

    return True

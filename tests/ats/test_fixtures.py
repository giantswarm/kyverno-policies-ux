from pykube.config import os
from pytest_helm_charts.clusters import Cluster
from pytest_helm_charts.k8s.deployment import wait_for_objects_condition
from pytest_helm_charts.giantswarm_app_platform.app import (
    create_app,
    wait_for_apps_to_run,
)
import logging
import pykube
import pytest
import time
import yaml


TEST_CLUSTER_NAME = "test"
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
    ret = kube_cluster.kubectl("apply", filename="manifests/crds/cluster-crd.yaml", output_format="json")
    LOGGER.debug("Created cluster CRD")
    LOGGER.info("Create machinepools.cluster.x-k8s.io CRD")
    ret = kube_cluster.kubectl("apply", filename="manifests/crds/machinepool-crd.yaml", output_format="json")
    LOGGER.debug("Created machinepool CRD")
    LOGGER.info("Create machinedeployments.cluster.x-k8s.io CRD")
    ret = kube_cluster.kubectl("apply", filename="manifests/crds/machinedeployment-crd.yaml", output_format="json")
    LOGGER.debug("Created machinedeployment CRD")

    # Organization CRD
    LOGGER.info("Create Organization CRD")
    ret = kube_cluster.kubectl("apply", filename="https://raw.githubusercontent.com/giantswarm/organization-operator/main/config/crd/security.giantswarm.io_organizations.yaml", output_format="json")
    LOGGER.debug(f"Created Organization CRD: {ret}")

    # CertConfig CRD
    LOGGER.info("Create CertConfig CRD")
    ret = kube_cluster.kubectl("apply", filename="manifests/crds/cert-config-crd.yaml", output_format="json")
    LOGGER.debug(f"Created CertConfig CRD: {ret}")

    # Kyverno
    LOGGER.info(f"Install Kyverno {KYVERNO_VERSION}")
    ret = kube_cluster.kubectl("apply --server-side", filename=f"https://github.com/kyverno/kyverno/releases/download/{KYVERNO_VERSION}/install.yaml", output_format="json" )

    wait_for_objects_condition(
        kube_client=kube_cluster.kube_client,
        obj_type=pykube.Deployment,
        obj_names=["kyverno"],
        objs_namespace="kyverno",
        obj_condition_func=lambda d: int(d.obj["status"].get("readyReplicas", 0)) > 0,
        timeout_sec=180,
        missing_ok=False
    )
    LOGGER.debug(f"Install Kyverno result: {ret}")

    app_name = "kyverno-policies-ux"
    namespace = "default"
    # get version from env `ATS_CHART_VERSION`
    version = os.environ.get("ATS_CHART_VERSION")
    if version is None:
        raise Exception("ATS_CHART_VERSION is not set")


    test_values_path = "test-values.yaml"
    LOGGER.info(f"Reading test values from {test_values_path}")
    with open(test_values_path) as stream:
        try:
            test_values = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise Exception(f"Error loading test values from {test_values_path}: {exc}")

    LOGGER.info(f"Deploy app {app_name} version {version}")
    create_app(
        kube_client=kube_cluster.kube_client,
        app_name=app_name,
        app_version=version,
        catalog_name="chartmuseum",
        catalog_namespace="default",
        namespace=namespace,
        deployment_namespace=namespace,
        config_values=test_values,
    )
    wait_for_apps_to_run(kube_cluster.kube_client, [app_name], namespace, 1800)
    LOGGER.debug(f"Deployed app {app_name}")
        

    # Create Organization namespace
    LOGGER.info("Create namespaces named 'org-giantswarm' and 'org-empty'")
    ret = kube_cluster.kubectl("apply", filename="manifests/test-organization.yaml", output_format="json")
    LOGGER.debug(f"Created giantswarm organization and its namespace: {ret}")
    ret = kube_cluster.kubectl("apply", filename="manifests/test-empty-organization.yaml", output_format="json")
    LOGGER.debug(f"Created empty organization and its namespace: {ret}")

    # This block is commented because test fail but I can't figure out why. If someone with Python experience could help, please let me know.
    # Patch Organizations so that they contain their namespace on their status field, like organization-operator does
    # ret = kube_cluster.kubectl("patch organization giantswarm --subresource status --type merge --patch '\{\"status\": \{\"namespace\": \"org-giantswarm\"\}\}'")
    # LOGGER.debug(f"Patched giantswarm organization status with namespace: {ret}")
    # ret = kube_cluster.kubectl("patch organization empty --subresource status --type merge --patch '\{\"status\": \{\"namespace\": \"org-empty\"\}\}'")
    # LOGGER.debug(f"Patched empty organization status with namespace: {ret}")

    # Test cluster CR
    LOGGER.info(f"Create cluster.x-k8s.io/v1beta1 named '{TEST_CLUSTER_NAME}'")
    ret = kube_cluster.kubectl("apply", filename="manifests/test-cluster.yaml", output_format="json")
    LOGGER.debug(f"Created cluster result: {ret}")

    time.sleep(5)

    return True

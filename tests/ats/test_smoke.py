from pytest_helm_charts.clusters import Cluster
from test_fixtures import fixtures
import logging
import pykube
import pytest
import subprocess

LOGGER = logging.getLogger(__name__)

SERVICE_PRIORITY_LABEL = "giantswarm.io/service-priority"

@pytest.mark.smoke
def test_api_working(fixtures, kube_cluster: Cluster) -> None:
    """
    Test if the Kubernetes API works by adding a label to our test cluster
    """
    assert kube_cluster.kube_client is not None
    assert len(pykube.Node.objects(kube_cluster.kube_client)) >= 1

    LOGGER.info("Adding label mylabel=myvalue to cluster test-cluster")
    kube_cluster.kubectl(
        "label --overwrite clusters.cluster.x-k8s.io test-cluster mylabel=myvalue"
    )

@pytest.mark.smoke
def test_service_priority_cluster_label(fixtures, kube_cluster: Cluster) -> None:
    """
    Checks whether our policy to prevent invalid service-priority label
    values is working.
    """

    # Set valid label value
    LOGGER.info(f"Attempt to set valid {SERVICE_PRIORITY_LABEL} label")
    cluster = kube_cluster.kubectl(
        f"label --overwrite clusters.cluster.x-k8s.io test-cluster {SERVICE_PRIORITY_LABEL}=medium"
    )
    LOGGER.info(f"Attempt to set valid service-priority label - result: {cluster}")

    # Set invalid label value
    LOGGER.info("Attempt to set invalid service-priority label")
    with pytest.raises(subprocess.CalledProcessError):
        cluster = kube_cluster.kubectl(
            f"label --overwrite clusters.cluster.x-k8s.io test-cluster {SERVICE_PRIORITY_LABEL}=badvalue"
        )

    # TODO: assert based on stderr content, once we know how. This is the expected output:
    # Error from server: admission webhook "validate.kyverno.svc-fail" denied the request:
    #
    # resource Cluster/default/test-cluster was blocked due to the following policies
    #
    # restrict-cluster-label-service-priority:
    # restrict-label-value-changes: 'validation error: The `giantswarm.io/service-priority`
    #     label only accepts the values `highest`, `medium`, and `lowest`. Rule restrict-label-value-changes[0]
    #     failed at path /metadata/labels/giantswarm.io/service-priority/. Rule restrict-label-value-changes[1]
    #     failed at path /metadata/labels/giantswarm.io/service-priority/. Rule restrict-label-value-changes[2]
    #     failed at path /metadata/labels/giantswarm.io/service-priority/.'
        
    assert cluster["metadata"]["labels"][SERVICE_PRIORITY_LABEL] != "badvalue"

    # Remove label
    cluster = kube_cluster.kubectl(
        f"label clusters.cluster.x-k8s.io test-cluster {SERVICE_PRIORITY_LABEL}-"
    )
    assert SERVICE_PRIORITY_LABEL not in cluster["metadata"]["labels"]

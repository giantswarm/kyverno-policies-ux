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
def test_service_priority_cluster_label_valid_set(fixtures, kube_cluster: Cluster) -> None:
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


@pytest.mark.smoke
def test_service_priority_cluster_label_valid_edit(fixtures, kube_cluster: Cluster) -> None:
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

    # Edit label value
    LOGGER.info(f"Attempt to edit {SERVICE_PRIORITY_LABEL} label")
    cluster = kube_cluster.kubectl(
        f"label --overwrite clusters.cluster.x-k8s.io test-cluster {SERVICE_PRIORITY_LABEL}=lowest"
    )
    LOGGER.info(f"Attempt to edit service-priority label - result: {cluster}")


@pytest.mark.smoke
def test_service_priority_cluster_label_invalid_edit(fixtures, capfd, kube_cluster: Cluster) -> None:
    with pytest.raises(subprocess.CalledProcessError):
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
        output = kube_cluster.kubectl(
            f"label --overwrite clusters.cluster.x-k8s.io test-cluster {SERVICE_PRIORITY_LABEL}=badvalue"
        )
        LOGGER.warn(f"Setting invalid service-priority label did not fail, output: {output}")

    _, stderr = capfd.readouterr()

    assert SERVICE_PRIORITY_LABEL in stderr
    assert "validate.kyverno.svc-fail" in stderr


@pytest.mark.smoke
def test_service_priority_cluster_label_remove(fixtures, kube_cluster: Cluster) -> None:
    """
    Checks whether our policy to prevent invalid service-priority label
    values is working.
    """

    # Set valid label value
    LOGGER.info(f"Attempt to set valid {SERVICE_PRIORITY_LABEL} label")
    cluster = kube_cluster.kubectl(
        f"label --overwrite clusters.cluster.x-k8s.io test-cluster {SERVICE_PRIORITY_LABEL}=highest"
    )
    LOGGER.info(f"Attempt to set valid service-priority label - result: {cluster}")

    # Remove label
    cluster = kube_cluster.kubectl(
        f"label clusters.cluster.x-k8s.io test-cluster {SERVICE_PRIORITY_LABEL}-"
    )
    assert SERVICE_PRIORITY_LABEL not in cluster["metadata"]["labels"]


@pytest.mark.smoke
def test_service_priority_cluster_label_invalid_set(fixtures, capfd, kube_cluster: Cluster) -> None:
    with pytest.raises(subprocess.CalledProcessError):
        """
        Checks whether our policy to prevent invalid service-priority label
        values is working.
        """

        # Set invalid label value
        LOGGER.info("Attempt to set invalid service-priority label")
        output = kube_cluster.kubectl(
            f"label --overwrite clusters.cluster.x-k8s.io test-cluster {SERVICE_PRIORITY_LABEL}=badvalue"
        )
        LOGGER.warn(f"Setting invalid service-priority label did not fail, output: {output}")

    _, stderr = capfd.readouterr()

    assert SERVICE_PRIORITY_LABEL in stderr
    assert "validate.kyverno.svc-fail" in stderr


# @pytest.mark.smoke
# def test_block_organization_deletion_when_still_has_clusters(fixtures, kube_cluster: Cluster) -> None:
#   with pytest.raises(subprocess.CalledProcessError):
#       """
#       Checks whether our policy prevents deleting organization that still have clusters on them.
#       """
#
#       LOGGER.info("Attempt to delete organization with existing clusters")
#       output = subprocess.check_output(
#           kube_cluster.kubectl(
#               f"delete organization giantswarm"
#               ),
#           stderr=subprocess.STDOUT
#       )
#       LOGGER.info(f"Attempt to set invalid service-priority label - result: {cluster}")
#       assert "organization" in output
#       assert "remove the clusters" in output


# @pytest.mark.smoke
# def test_allows_organization_deletion_when_it_has_no_clusters(fixtures, kube_cluster: Cluster) -> None:
#     """
#     Checks whether our policy prevents deleting organization that still have clusters on them.
#     """
#
#     LOGGER.info("Attempt to delete organization with no clusters on it")
#     try:
#         res = kube_cluster.kubectl("delete", filename="test-empty-organization.yaml", output_format=""),
#     except:
#         if res.stdout != "organization.security.giantswarm.io \"empty\" deleted":
#             raise

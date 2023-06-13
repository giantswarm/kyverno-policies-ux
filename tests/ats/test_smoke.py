from pytest_helm_charts.clusters import Cluster
from test_fixtures import fixtures, TEST_CLUSTER_NAME
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

    LOGGER.info(f"Adding label mylabel=myvalue to cluster {TEST_CLUSTER_NAME}")
    kube_cluster.kubectl(
        f"label --overwrite clusters.cluster.x-k8s.io {TEST_CLUSTER_NAME} mylabel=myvalue"
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
        f"label --overwrite clusters.cluster.x-k8s.io {TEST_CLUSTER_NAME} {SERVICE_PRIORITY_LABEL}=medium"
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
        f"label --overwrite clusters.cluster.x-k8s.io {TEST_CLUSTER_NAME} {SERVICE_PRIORITY_LABEL}=medium"
    )
    LOGGER.info(f"Attempt to set valid service-priority label - result: {cluster}")

    # Edit label value
    LOGGER.info(f"Attempt to edit {SERVICE_PRIORITY_LABEL} label")
    cluster = kube_cluster.kubectl(
        f"label --overwrite clusters.cluster.x-k8s.io {TEST_CLUSTER_NAME} {SERVICE_PRIORITY_LABEL}=lowest"
    )
    LOGGER.info(f"Attempt to edit service-priority label - result: {cluster}")


@pytest.mark.smoke
def test_service_priority_cluster_label_invalid_edit(fixtures, kube_cluster: Cluster) -> None:
    with pytest.raises(subprocess.CalledProcessError):
        """
        Checks whether our policy to prevent invalid service-priority label
        values is working.
        """

        # Set valid label value
        LOGGER.info(f"Attempt to set valid {SERVICE_PRIORITY_LABEL} label")
        cluster = kube_cluster.kubectl(
            f"label --overwrite clusters.cluster.x-k8s.io {TEST_CLUSTER_NAME} {SERVICE_PRIORITY_LABEL}=medium"
        )
        LOGGER.info(f"Attempt to set valid service-priority label - result: {cluster}")

        # Set invalid label value
        LOGGER.info("Attempt to set invalid service-priority label")
        output = subprocess.check_output(
            kube_cluster.kubectl(
                f"label --overwrite clusters.cluster.x-k8s.io {TEST_CLUSTER_NAME} {SERVICE_PRIORITY_LABEL}=badvalue"
            ),
            stderr=subprocess.STDOUT
        )
        LOGGER.info(f"Attempt to set invalid service-priority label - result: {cluster}")
        assert cluster["metadata"]["labels"][SERVICE_PRIORITY_LABEL] != "badvalue"
        assert SERVICE_PRIORITY_LABEL in output
        assert "validate.kyverno.svc-fail" in output


@pytest.mark.smoke
def test_service_priority_cluster_label_remove(fixtures, kube_cluster: Cluster) -> None:
    """
    Checks whether our policy to prevent invalid service-priority label
    values is working.
    """

    # Set valid label value
    LOGGER.info(f"Attempt to set valid {SERVICE_PRIORITY_LABEL} label")
    cluster = kube_cluster.kubectl(
        f"label --overwrite clusters.cluster.x-k8s.io {TEST_CLUSTER_NAME} {SERVICE_PRIORITY_LABEL}=highest"
    )
    LOGGER.info(f"Attempt to set valid service-priority label - result: {cluster}")

    # Remove label
    cluster = kube_cluster.kubectl(
        f"label clusters.cluster.x-k8s.io {TEST_CLUSTER_NAME} {SERVICE_PRIORITY_LABEL}-"
    )
    assert SERVICE_PRIORITY_LABEL not in cluster["metadata"]["labels"]


@pytest.mark.smoke
def test_service_priority_cluster_label_invalid_set(fixtures, kube_cluster: Cluster) -> None:
    with pytest.raises(subprocess.CalledProcessError):
        """
        Checks whether our policy to prevent invalid service-priority label
        values is working.
        """

        # Set invalid label value
        LOGGER.info("Attempt to set invalid service-priority label")
        output = subprocess.check_output(
            kube_cluster.kubectl(
                f"label --overwrite clusters.cluster.x-k8s.io {TEST_CLUSTER_NAME} {SERVICE_PRIORITY_LABEL}=badvalue"
            ),
            stderr=subprocess.STDOUT
        )
        LOGGER.info(f"Attempt to set invalid service-priority label - result: {cluster}")
        assert cluster["metadata"]["labels"][SERVICE_PRIORITY_LABEL] != "badvalue"
        assert SERVICE_PRIORITY_LABEL in output
        assert "validate.kyverno.svc-fail" in output


@pytest.mark.smoke
def test_valid_cluster_name(fixtures, kube_cluster: Cluster) -> None:
    LOGGER.info("Attempt to create cluster with valid name")
    output = kube_cluster.kubectl(
        "apply",
        filename="valid-cluster.yaml",
        output_format="json"
    ),
    LOGGER.info(f"Created cluster without error, result: {output}")


@pytest.mark.smoke
def test_valid_machinepool_name(fixtures, kube_cluster: Cluster) -> None:
    LOGGER.info("Attempt to create machinepool with valid name")
    output = kube_cluster.kubectl(
        "apply",
        filename="valid-machinepool.yaml",
        output_format="json"
    ),
    LOGGER.info(f"Created machinepool without error, result: {output}")


@pytest.mark.smoke
def test_valid_machinedeployment_name(fixtures, kube_cluster: Cluster) -> None:
    LOGGER.info("Attempt to create machinedeployment with valid name")
    output = kube_cluster.kubectl(
        "apply",
        filename="valid-machinedeployment.yaml",
        output_format="json"
    ),
    LOGGER.info(f"Created machinedeployment without error, result: {output}")


@pytest.mark.smoke
def test_invalid_cluster_name(fixtures, capfd, kube_cluster: Cluster) -> None:
    with pytest.raises(subprocess.CalledProcessError):
        """
        Checks whether our policy prevents creating Cluster resources with
        invalid names.
        """

        # Set invalid label value
        LOGGER.info("Attempt to create cluster with invalid name")
        output = kube_cluster.kubectl(
            "apply",
            filename="invalid-clusters.yaml",
            output_format="json"
        ),
        LOGGER.warn(f"Creating cluster did not fail as expected, result: {output}")

    _, stderr = capfd.readouterr()
    assert "validate.kyverno.svc-fail" in stderr
    assert "cluster-name-maximum-length" in stderr
    assert "cluster-name-does-not-start-with-number" in stderr


@pytest.mark.smoke
def test_invalid_machinepool_name(fixtures, capfd, kube_cluster: Cluster) -> None:
    with pytest.raises(subprocess.CalledProcessError):
        """
        Checks whether our policy prevents creating MachinePool resources with
        invalid names.
        """

        LOGGER.info("Attempt to create machinepool with invalid name")
        output = kube_cluster.kubectl("apply", filename="invalid-machinepools.yaml", output_format="json"),
        LOGGER.warn(f"Creating machinepool did not fail as expected, result: {output}")

    _, stderr = capfd.readouterr()
    assert "validate.kyverno.svc-fail" in stderr
    assert "machine-pool-name-maximum-length" in stderr
    assert "machine-pool-name-does-not-start-with-number" in stderr


@pytest.mark.smoke
def test_invalid_machinedeployment_name(fixtures, capfd, kube_cluster: Cluster) -> None:
    with pytest.raises(subprocess.CalledProcessError):
        """
        Checks whether our policy prevents creating MachineDeployment resources with
        invalid names.
        """

        LOGGER.info("Attempt to create machinedeployment with invalid name")
        output = kube_cluster.kubectl("apply", filename="invalid-machinedeployments.yaml", output_format="json"),
        LOGGER.warn(f"Creating machinedeployment did not fail as expected, result: {output}")

    _, stderr = capfd.readouterr()
    assert "machine-deployment-name-maximum-length" in stderr
    assert "machine-deployment-name-does-not-start-with-number" in stderr


@pytest.mark.smoke
@pytest.mark.capture_disabled
def test_invalid_cluster_name(fixtures, capfd, kube_cluster: Cluster) -> None:
    with pytest.raises(subprocess.CalledProcessError):
        """
        Checks whether our policy prevents creating Cluster resources with
        invalid names.
        """

        # Set invalid label value
        LOGGER.info("Attempt to create cluster with invalid name")
        output = subprocess.check_output(
                kube_cluster.kubectl("apply", filename="invalid-clusters.yaml", output_format="json"), 
                stderr=subprocess.STDOUT
        )
        LOGGER.info(f"Attempt to create cluster with invalid name - result: {output}")
        assert "cluster-name-maximum-length" in output

        # LOGGER.info("Attempt to create cluster with invalid name")
        # # with pytest.raises(subprocess.CalledProcessError) as e:
        # # with pytest.raises(Exception) as e:
        # LOGGER.info(f"Attempt to create cluster with invalid name")
        # try:
        #     output = subprocess.check_output(
        #         kube_cluster.kubectl("apply", filename="invalid-clusters.yaml", output_format="json"),
        #         stderr=subprocess.STDOUT
        #     )
        # except subprocess.CalledProcessError as e:
        #     LOGGER.info(f"After kubectl e: {e}")
        # stdout, stderr = capfd.readouterr()
        # LOGGER.info(f"captured stdout: {stdout}")
        # LOGGER.info(f"captured stderr: {stderr}")
        #
        # with capfd.disabled():
        #     LOGGER.info("works")
        # try:
        #     output = kube_cluster.kubectl("apply", filename="invalid-clusters.yaml", output_format="json")
        #     assert False  # should raise exception
        # except subprocess.CalledProcessError as e:
        #     LOGGER.info("After kubectl - subprocess.CalledProcessError")
        #     LOGGER.info(f"Attempted to create cluster with invalid name: {e}")
        #     LOGGER.info(f"Stdout: {e.stdout}")
        #     LOGGER.info(f"Stderr: {e.stdout}")
        #     assert "cluster-name-maximum-length" in str(e)



# @pytest.mark.smoke
# def test_invalid_machinepool_name(fixtures, kube_cluster: Cluster) -> None:
#     with pytest.raises(subprocess.CalledProcessError):
#         """
#         Checks whether our policy prevents creating MachinePool resources with
#         invalid names.
#         """
#
#         LOGGER.info("Attempt to create machinepool with invalid name")
#         with pytest.raises(subprocess.CalledProcessError) as e:
#             LOGGER.info(f"Attempt to create machinepool with invalid name - result: {e}")
#             output = kube_cluster.kubectl("apply", filename="invalid-machinepools.yaml", output_format="json")
#             assert "machinepool-name-maximum-length" in str(e.value)
#
#
# @pytest.mark.smoke
# def test_invalid_machinedeployment_name(fixtures, kube_cluster: Cluster) -> None:
#     with pytest.raises(subprocess.CalledProcessError):
#         """
#         Checks whether our policy prevents creating MachineDeployment resources with
#         invalid names.
#         """
#
#         LOGGER.info("Attempt to create machinedeployment with invalid name")
#         with pytest.raises(subprocess.CalledProcessError) as e:
#             LOGGER.info(f"Attempt to create machinedeployment with invalid name - result: {e}")
#             output = kube_cluster.kubectl("apply", filename="invalid-machinedeployments.yaml", output_format="json")
#             assert "machinedeployment-name-maximum-length" in str(e.value)


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

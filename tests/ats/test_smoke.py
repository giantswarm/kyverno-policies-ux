import time
from pytest_helm_charts.clusters import Cluster
from test_fixtures import fixtures, TEST_CLUSTER_NAME
import logging
import pykube
import pytest
import subprocess

LOGGER = logging.getLogger(__name__)

SERVICE_PRIORITY_LABEL = "giantswarm.io/service-priority"
PREVENT_DELETION_LABEL = "giantswarm.io/prevent-deletion"



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
    with pytest.raises(subprocess.CalledProcessError) as e:
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
        output = kube_cluster.kubectl(
            f"label --overwrite clusters.cluster.x-k8s.io {TEST_CLUSTER_NAME} {SERVICE_PRIORITY_LABEL}=badvalue"
        )
        LOGGER.warn(f"Setting invalid service-priority label did not fail, output: {output}")

    LOGGER.info(f"stdout: {e.value.stdout}, stderr: {e.value.stderr}")
    stderr = e.value.stderr
    assert SERVICE_PRIORITY_LABEL in stderr
    assert "restrict-label-value-changes" in stderr
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
        f"label --overwrite clusters.cluster.x-k8s.io {TEST_CLUSTER_NAME} {SERVICE_PRIORITY_LABEL}=highest"
    )

    # Remove label
    cluster = kube_cluster.kubectl(
        f"label clusters.cluster.x-k8s.io {TEST_CLUSTER_NAME} {SERVICE_PRIORITY_LABEL}-"
    )

    cluster = kube_cluster.kubectl(
        f"get clusters.cluster.x-k8s.io {TEST_CLUSTER_NAME} -o yaml"
    )
    LOGGER.info(f"cluster: {cluster}")
    LOGGER.info(f"cluster metadata: {cluster['metadata']}")
    assert SERVICE_PRIORITY_LABEL not in cluster["metadata"]["labels"]


@pytest.mark.smoke
def test_service_priority_cluster_label_invalid_set(fixtures, kube_cluster: Cluster) -> None:
    with pytest.raises(subprocess.CalledProcessError) as e:
        """
        Checks whether our policy to prevent invalid service-priority label
        values is working.
        """

        # Set invalid label value
        LOGGER.info("Attempt to set invalid service-priority label")
        output = kube_cluster.kubectl(
            f"label --overwrite clusters.cluster.x-k8s.io {TEST_CLUSTER_NAME} {SERVICE_PRIORITY_LABEL}=badvalue"
        )
        LOGGER.warn(f"Setting invalid service-priority label did not fail, output: {output}")

    stderr = e.value.stderr
    assert SERVICE_PRIORITY_LABEL in stderr
    assert "restrict-label-value-changes" in stderr
    assert "validate.kyverno.svc-fail" in stderr


@pytest.mark.smoke
def test_valid_cluster_name(fixtures, kube_cluster: Cluster) -> None:
    LOGGER.info("Attempt to create cluster with valid name")
    output = kube_cluster.kubectl(
        "apply",
        filename="manifests/valid-cluster.yaml",
        output_format="json"
    ),
    LOGGER.info(f"Created cluster without error, result: {output}")


@pytest.mark.smoke
def test_valid_machinepool_name(fixtures, kube_cluster: Cluster) -> None:
    LOGGER.info("Attempt to create machinepool with valid name")
    output = kube_cluster.kubectl(
        "apply",
        filename="manifests/valid-machinepool.yaml",
        output_format="json"
    ),
    LOGGER.info(f"Created machinepool without error, result: {output}")


@pytest.mark.smoke
def test_valid_machinedeployment_name(fixtures, kube_cluster: Cluster) -> None:
    LOGGER.info("Attempt to create machinedeployment with valid name")
    output = kube_cluster.kubectl(
        "apply",
        filename="manifests/valid-machinedeployment.yaml",
        output_format="json"
    ),
    LOGGER.info(f"Created machinedeployment without error, result: {output}")


@pytest.mark.smoke
def test_invalid_cluster_name(fixtures, kube_cluster: Cluster) -> None:
    with pytest.raises(subprocess.CalledProcessError) as e:
        """
        Checks whether our policy prevents creating Cluster resources with
        invalid names.
        """

        # Set invalid label value
        LOGGER.info("Attempt to create cluster with invalid name")
        output = kube_cluster.kubectl(
            "apply",
            filename="manifests/invalid-clusters.yaml",
            output_format="json"
        ),
        LOGGER.warn(f"Creating cluster did not fail as expected, result: {output}")

    stderr = e.value.stderr
    assert "validate.kyverno.svc-fail" in stderr
    assert "cluster-name-maximum-length" in stderr


@pytest.mark.smoke
def test_invalid_machinepool_name(fixtures, kube_cluster: Cluster) -> None:
    with pytest.raises(subprocess.CalledProcessError) as e:
        """
        Checks whether our policy prevents creating MachinePool resources with
        invalid names.
        """

        LOGGER.info("Attempt to create machinepool with invalid name")
        output = kube_cluster.kubectl("apply", filename="manifests/invalid-machinepools.yaml", output_format="json"),
        LOGGER.warn(f"Creating machinepool did not fail as expected, result: {output}")

    stderr = e.value.stderr
    assert "validate.kyverno.svc-fail" in stderr
    assert "machine-pool-name-maximum-length" in stderr


@pytest.mark.smoke
def test_invalid_machinedeployment_name(fixtures, kube_cluster: Cluster) -> None:
    with pytest.raises(subprocess.CalledProcessError) as e:
        """
        Checks whether our policy prevents creating MachineDeployment resources with
        invalid names.
        """

        LOGGER.info("Attempt to create machinedeployment with invalid name")
        output = kube_cluster.kubectl("apply", filename="manifests/invalid-machinedeployments.yaml", output_format="json"),
        LOGGER.warn(f"Creating machinedeployment did not fail as expected, result: {output}")

    stderr = e.value.stderr
    assert "machine-deployment-name-maximum-length" in stderr

def test_prevent_deletion_with_label(fixtures, kube_cluster: Cluster) -> None:
    """
    Checks whether our policy prevents the deletion of a cluster that has the `giantswarm.io/prevent-deletion` label.
    """

    # create namespace
    kube_cluster.kubectl("create namespace test-namespace")
    # label namespace
    kube_cluster.kubectl(
        f"label --overwrite namespace test-namespace {PREVENT_DELETION_LABEL}=true"
    )
    with pytest.raises(subprocess.CalledProcessError) as e:
        LOGGER.info("Attempt to delete namespace with prevent-deletion label")
        output = kube_cluster.kubectl(
            "delete namespace test-namespace"
        )
        LOGGER.warn(f"Deleting cluster with prevent-deletion label did not fail, output: {output}")
    stderr = e.value.stderr
    LOGGER.info(f"stderr: {stderr}")

    assert "block-resource-deletion-if-has-prevent-deletion-label" in stderr
    assert "validate.kyverno.svc-fail" in stderr

    # remove label
    kube_cluster.kubectl(
        f"label --overwrite namespace test-namespace {PREVENT_DELETION_LABEL}-"
    )

    # delete namespace
    kube_cluster.kubectl("delete namespace test-namespace")


@pytest.mark.smoke
def test_dont_prevent_deletion_without_label(fixtures, kube_cluster: Cluster) -> None:
    # create namespace
    kube_cluster.kubectl("create namespace test-namespace")

    LOGGER.info("Attempt to delete namespace without prevent-deletion label")
    output = kube_cluster.kubectl(
        "delete namespace test-namespace"
    )
    LOGGER.info(f"Deleting cluster without prevent-deletion label did not fail, output: {output}")

@pytest.mark.smoke
def test_prevent_release_deletion_when_used_by_clusters(fixtures, kube_cluster: Cluster) -> None:
    """
    Checks whether our policy prevents deletion of a Release that is still in use by clusters.
    """
    kube_cluster.kubectl("apply", filename="manifests/test-release.yaml")
    
    # Attempt to delete the release - should be prevented
    with pytest.raises(subprocess.CalledProcessError) as e:
        LOGGER.info("Attempting to delete release that is used by clusters")
        kube_cluster.kubectl("delete release aws-30.1.0")
        
    stderr = e.value.stderr
    LOGGER.info(f"stderr: {stderr}")
    
    assert "protect-active-releases" in stderr
    assert "Cannot delete release aws-30.1.0" in stderr
    
    # Clean up
    kube_cluster.kubectl("delete cluster test-release")
    kube_cluster.kubectl("delete release aws-30.1.0")

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

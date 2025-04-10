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
    # Create a test release
    release_yaml = """
    apiVersion: release.giantswarm.io/v1alpha1
    kind: Release
    metadata:
      annotations:
        giantswarm.io/docs: https://docs.giantswarm.io/use-the-api/management-api/crd/releases.release.giantswarm.io
        giantswarm.io/release-notes: https://github.com/giantswarm/releases/tree/master/capa/v30.1.0
      name: aws-30.1.0
    spec:
      apps:
      - catalog: default
        dependsOn:
        - cloud-provider-aws
        name: aws-ebs-csi-driver
        version: 3.0.5
      - catalog: default
        dependsOn:
        - prometheus-operator-crd
        name: aws-ebs-csi-driver-servicemonitors
        version: 0.1.0
      - catalog: default
        name: aws-nth-bundle
        version: 1.2.1
      - catalog: default
        dependsOn:
        - cert-manager
        name: aws-pod-identity-webhook
        version: 1.19.1
      - catalog: default
        name: capi-node-labeler
        version: 1.0.2
      - catalog: default
        dependsOn:
        - kyverno-crds
        name: cert-exporter
        version: 2.9.5
      - catalog: default
        dependsOn:
        - prometheus-operator-crd
        name: cert-manager
        version: 3.9.0
      - catalog: default
        dependsOn:
        - prometheus-operator-crd
        name: chart-operator-extensions
        version: 1.1.2
      - catalog: default
        name: cilium
        version: 0.31.1
      - catalog: cluster
        name: cilium-crossplane-resources
        version: 0.2.0
      - catalog: default
        dependsOn:
        - prometheus-operator-crd
        name: cilium-servicemonitors
        version: 0.1.2
      - catalog: default
        dependsOn:
        - vertical-pod-autoscaler-crd
        name: cloud-provider-aws
        version: 1.30.8-gs1
      - catalog: default
        dependsOn:
        - kyverno-crds
        name: cluster-autoscaler
        version: 1.30.4-gs1
      - catalog: default
        dependsOn:
        - cilium
        name: coredns
        version: 1.24.0
      - catalog: default
        dependsOn:
        - vertical-pod-autoscaler-crd
        name: coredns-extensions
        version: 0.1.2
      - catalog: default
        dependsOn:
        - kyverno-crds
        name: etcd-defrag
        version: 1.0.2
      - catalog: default
        dependsOn:
        - kyverno-crds
        name: etcd-k8s-res-count-exporter
        version: 1.10.3
      - catalog: default
        dependsOn:
        - prometheus-operator-crd
        name: external-dns
        version: 3.2.0
      - catalog: default
        dependsOn:
        - prometheus-operator-crd
        name: irsa-servicemonitors
        version: 0.1.0
      - catalog: default
        dependsOn:
        - kyverno-crds
        name: k8s-audit-metrics
        version: 0.10.2
      - catalog: default
        dependsOn:
        - kyverno-crds
        name: k8s-dns-node-cache
        version: 2.8.1
      - catalog: default
        dependsOn:
        - kyverno-crds
        name: metrics-server
        version: 2.6.0
      - catalog: default
        dependsOn:
        - prometheus-operator-crd
        name: net-exporter
        version: 1.22.0
      - catalog: cluster
        dependsOn:
        - cilium
        name: network-policies
        version: 0.1.1
      - catalog: default
        dependsOn:
        - kyverno-crds
        name: node-exporter
        version: 1.20.2
      - catalog: default
        dependsOn:
        - coredns
        name: observability-bundle
        version: 1.11.0
      - catalog: default
        dependsOn:
        - kyverno-crds
        name: observability-policies
        version: 0.0.1
      - catalog: default
        dependsOn:
        - prometheus-operator-crd
        name: prometheus-blackbox-exporter
        version: 0.5.0
      - catalog: giantswarm
        dependsOn:
        - prometheus-operator-crd
        name: security-bundle
        version: 1.10.0
      - catalog: default
        name: teleport-kube-agent
        version: 0.10.4
      - catalog: default
        dependsOn:
        - prometheus-operator-crd
        name: vertical-pod-autoscaler
        version: 5.4.0
      - catalog: default
        name: vertical-pod-autoscaler-crd
        version: 3.2.0
      components:
      - catalog: cluster
        name: cluster-aws
        version: 3.2.1
      - catalog: control-plane-catalog
        name: flatcar
        version: 4152.2.1
      - catalog: control-plane-catalog
        name: kubernetes
        version: 1.30.11
      - catalog: control-plane-catalog
        name: os-tooling
        version: 1.24.0
      date: "2025-03-18T12:00:00Z"
      state: active
    """
    kube_cluster.kubectl_apply(release_yaml)
    
    # Create a test cluster with the release version label
    cluster_yaml = """
    apiVersion: cluster.x-k8s.io/v1beta1
    kind: Cluster
    metadata:
      name: test-cluster
      namespace: default
      labels:
        release.giantswarm.io/version: "30.1.0"
    spec:
      clusterNetwork:
        services:
          cidrBlocks: ["10.96.0.0/12"]
        pods:
          cidrBlocks: ["192.168.0.0/16"]
      controlPlaneEndpoint:
        host: test-api.example.com
        port: 6443
    """
    kube_cluster.kubectl_apply(cluster_yaml)
    
    # Attempt to delete the release - should be prevented
    with pytest.raises(subprocess.CalledProcessError) as e:
        LOGGER.info("Attempting to delete release that is used by clusters")
        kube_cluster.kubectl("delete release aws-30.1.0")
        
    stderr = e.value.stderr
    LOGGER.info(f"stderr: {stderr}")
    
    assert "protect-active-releases" in stderr
    assert "Cannot delete release aws-30.1.0" in stderr
    
    # Clean up
    kube_cluster.kubectl("delete cluster test-cluster -n org-giantswarm")
    kube_cluster.kubectl("delete release aws-30.1.0")


@pytest.mark.smoke
def test_allow_release_deletion_when_not_used(fixtures, kube_cluster: Cluster) -> None:
    """
    Checks whether our policy allows deletion of a Release that is not in use by any clusters.
    """
    # Create a test release with a different version
    release_yaml = """
    apiVersion: release.giantswarm.io/v1alpha1
    kind: Release
    metadata:
      annotations:
        giantswarm.io/docs: https://docs.giantswarm.io/use-the-api/management-api/crd/releases.release.giantswarm.io
        giantswarm.io/release-notes: https://github.com/giantswarm/releases/tree/master/capa/v30.0.0
      name: aws-30.0.0
    spec:
      apps:
      - catalog: default
        dependsOn:
        - cloud-provider-aws
        name: aws-ebs-csi-driver
        version: 3.0.3
      - catalog: default
        dependsOn:
        - prometheus-operator-crd
        name: aws-ebs-csi-driver-servicemonitors
        version: 0.1.0
      - catalog: default
        name: aws-nth-bundle
        version: 1.2.1
      - catalog: default
        dependsOn:
        - cert-manager
        name: aws-pod-identity-webhook
        version: 1.19.0
      - catalog: default
        name: capi-node-labeler
        version: 1.0.1
      - catalog: default
        dependsOn:
        - kyverno-crds
        name: cert-exporter
        version: 2.9.4
      - catalog: default
        dependsOn:
        - prometheus-operator-crd
        name: cert-manager
        version: 3.9.0
      - catalog: default
        dependsOn:
        - prometheus-operator-crd
        name: chart-operator-extensions
        version: 1.1.2
      - catalog: default
        name: cilium
        version: 0.31.0
      - catalog: cluster
        name: cilium-crossplane-resources
        version: 0.2.0
      - catalog: default
        dependsOn:
        - prometheus-operator-crd
        name: cilium-servicemonitors
        version: 0.1.2
      - catalog: default
        dependsOn:
        - vertical-pod-autoscaler-crd
        name: cloud-provider-aws
        version: 1.30.7-gs3
      - catalog: default
        dependsOn:
        - kyverno-crds
        name: cluster-autoscaler
        version: 1.30.3-gs2
      - catalog: default
        dependsOn:
        - cilium
        name: coredns
        version: 1.24.0
      - catalog: default
        dependsOn:
        - vertical-pod-autoscaler-crd
        name: coredns-extensions
        version: 0.1.2
      - catalog: default
        dependsOn:
        - kyverno-crds
        name: etcd-defrag
        version: 1.0.1
      - catalog: default
        dependsOn:
        - kyverno-crds
        name: etcd-k8s-res-count-exporter
        version: 1.10.1
      - catalog: default
        dependsOn:
        - prometheus-operator-crd
        name: external-dns
        version: 3.2.0
      - catalog: default
        dependsOn:
        - prometheus-operator-crd
        name: irsa-servicemonitors
        version: 0.1.0
      - catalog: default
        dependsOn:
        - kyverno-crds
        name: k8s-audit-metrics
        version: 0.10.1
      - catalog: default
        dependsOn:
        - kyverno-crds
        name: k8s-dns-node-cache
        version: 2.8.1
      - catalog: default
        dependsOn:
        - kyverno-crds
        name: metrics-server
        version: 2.6.0
      - catalog: default
        dependsOn:
        - prometheus-operator-crd
        name: net-exporter
        version: 1.21.0
      - catalog: cluster
        dependsOn:
        - cilium
        name: network-policies
        version: 0.1.1
      - catalog: default
        dependsOn:
        - kyverno-crds
        name: node-exporter
        version: 1.20.1
      - catalog: default
        dependsOn:
        - coredns
        name: observability-bundle
        version: 1.9.0
      - catalog: default
        dependsOn:
        - kyverno-crds
        name: observability-policies
        version: 0.0.1
      - catalog: default
        dependsOn:
        - prometheus-operator-crd
        name: prometheus-blackbox-exporter
        version: 0.5.0
      - catalog: giantswarm
        dependsOn:
        - prometheus-operator-crd
        name: security-bundle
        version: 1.9.1
      - catalog: default
        name: teleport-kube-agent
        version: 0.10.3
      - catalog: default
        dependsOn:
        - prometheus-operator-crd
        name: vertical-pod-autoscaler
        version: 5.4.0
      - catalog: default
        name: vertical-pod-autoscaler-crd
        version: 3.2.0
      components:
      - catalog: cluster
        name: cluster-aws
        version: 3.0.0
      - catalog: control-plane-catalog
        name: flatcar
        version: 4152.2.1
      - catalog: control-plane-catalog
        name: kubernetes
        version: 1.30.10
      - catalog: control-plane-catalog
        name: os-tooling
        version: 1.23.1
      date: "2025-02-20T12:00:00Z"
      state: active
    """
    kube_cluster.kubectl_apply(release_yaml)
    
    # Delete should succeed as no clusters use this release
    output = kube_cluster.kubectl("delete release aws-30.0.0")
    LOGGER.info(f"Successfully deleted unused release, output: {output}")

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

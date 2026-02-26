#!/usr/bin/env bash

set -euo pipefail

# Install CRDs required for Chainsaw tests

kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api/refs/heads/main/config/crd/bases/cluster.x-k8s.io_clusters.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api/refs/heads/main/config/crd/bases/cluster.x-k8s.io_machinepools.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api/refs/heads/main/config/crd/bases/cluster.x-k8s.io_machinedeployments.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api/refs/heads/main/controlplane/kubeadm/config/crd/bases/controlplane.cluster.x-k8s.io_kubeadmcontrolplanes.yaml

# AWSCluster CRD from CAPA (used by block-infracluster-deletion-if-has-controlplane, capa only)
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/cluster-api-provider-aws/refs/heads/main/config/crd/bases/infrastructure.cluster.x-k8s.io_awsclusters.yaml

# Release CRD from giantswarm/releases
kubectl apply -f https://raw.githubusercontent.com/giantswarm/releases/master/sdk/config/crd/bases/release.giantswarm.io_releases.yaml

# Organization CRD without status subresource so tests can set status.namespace via regular apply
kubectl apply -f - <<'EOF'
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: organizations.security.giantswarm.io
spec:
  group: security.giantswarm.io
  names:
    kind: Organization
    listKind: OrganizationList
    plural: organizations
    singular: organization
  scope: Cluster
  versions:
  - name: v1alpha1
    served: true
    storage: true
    schema:
      openAPIV3Schema:
        type: object
        x-kubernetes-preserve-unknown-fields: true
EOF

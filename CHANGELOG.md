# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.12.0] - 2025-06-05

### Added

- Cluster Roles for Kyverno towards giantswarm/issues/33418

## [0.11.0] - 2025-04-22

- Add `clusterRole` for `admission-controller` on `cloud-director` clusters to support Kyverno `v0.19.0`.

## [0.10.0] - 2025-04-15

### Added

- Add `clusterRole` to support Kyverno `v0.19.0`.

## [0.9.0] - 2025-04-11

### Added

- Prevent active releases from being deleted.

### Changed

- Cluster names can start with a number. Remove restriction that prevented that.

## [0.8.0] - 2025-02-19

### Changed

- Use `Enforce` instead of `enforce` as ValidationFailureAction.

### Added

- Add `AzureCluster` to list of objects protected by the deletion prevention label

## [0.7.4] - 2024-11-14

### Changed

- Apply `CertConfig` policy just on vintage, since that CRD is not in use in CAPI anymore.

## [0.7.3] - 2024-09-25

- `cluster-names` now targets Cluster by GVK
- Use `Enforce` validationFailureAction.

## [0.7.2] - 2024-01-29

### Changed

- Update values schema

### Added

- Add `VCDCluster` and `KubeadmControlPlane` resources as acceptable deletion prevention targets.

### Fixed

- Move pss values under the global property
- Fix team ownership

## [0.7.1] - 2023-11-15

### Changed

- Increase the cluster name length to 20 characters
- Increase the machine pool name length to 31 characters
- Increase the machine deployment name length to 31 characters

## [0.7.0] - 2023-09-27

### Changed

- Fixed test values for chart tests.

## [0.6.0] - 2023-09-12

### Changed

- Changed configuration of resources for `giantswarm.io/prevent-deletion` label from GVK to just Kind.

## [0.5.0] - 2023-08-23

### Added

- Add ConfigMap and Secret as default targeted resource for `giantswarm.io/prevent-deletion` label.

## [0.4.0] - 2023-08-22

### Added

- Add policy that blocks deletion of resources with the `giantswarm.io/prevent-deletion` label.

### Changed

- Updates ats, abs and ats python dependencies.

## [0.3.1] - 2023-06-20

- Revert 38: some customer clusters violate the rule that machine deployment names should not start with a number.

## [0.3.0] - 2023-06-20

### Removed

- Stop pushing to `openstack-app-collection`.

### Added

- Restrict cluster names to 10 characters and forbid them to start with a number.
- Restrict machine pools and deployments to 21 characters (10 for the cluster
  name prefix, 1 for a delimiter '-' and 10 for the deployment/pool name itself)
  and forbid them to start with a number.

### Changed

- Improve/fix cluster label policy tests to also check error message.

## [0.2.3] - 2023-04-25

### Changed

- Push to vsphere app collection.
- Don't push to openstack app collection.

## [0.2.2] - 2023-03-14

### Changed

- Don't block deletion of `Organization` if the clusters are already being deleted.

## [0.2.1] - 2023-03-09

### Fixed

- Add default value when trying to look up the organization namespace from the organization status field, as this may be empty when the organization was just created.

## [0.2.0] - 2023-03-07

### Added

- Push to cloud-director app collection.
- Push to `capz` app collection.
- Bump `clusterctl`, `kind` and `kyverno` versions from tests.
- Add policy that blocks the deletion of `Organizations` if they still have `Clusters`.

### Changed

- Remove deprecated `validate` step from CI.

## [0.1.1] - 2022-08-05

## [0.1.0] - 2022-06-15

### Added

- Validation of `giantswarm.io/service-priority` label values on `clusters.cluster.x-k8s.io/v*/Cluster` resources.

### Fixed

- Repaired ATS tests to have a basis to work with.

## [0.0.1] - 2022-03-31

### Added

- Initial policies moved from [`kyverno-policies`](https://github.com/giantswarm/kyverno-policies).
- Push to AWS, Azure, KVM, and OpenStack collections.

[Unreleased]: https://github.com/giantswarm/kyverno-policies-ux/compare/v0.12.0...HEAD
[0.12.0]: https://github.com/giantswarm/kyverno-policies-ux/compare/v0.11.0...v0.12.0
[0.11.0]: https://github.com/giantswarm/kyverno-policies-ux/compare/v0.10.0...v0.11.0
[0.10.0]: https://github.com/giantswarm/kyverno-policies-ux/compare/v0.9.0...v0.10.0
[0.9.0]: https://github.com/giantswarm/kyverno-policies-ux/compare/v0.8.0...v0.9.0
[0.8.0]: https://github.com/giantswarm/kyverno-policies-ux/compare/v0.7.4...v0.8.0
[0.7.4]: https://github.com/giantswarm/kyverno-policies-ux/compare/v0.7.3...v0.7.4
[0.7.3]: https://github.com/giantswarm/kyverno-policies-ux/compare/v0.7.2...v0.7.3
[0.7.2]: https://github.com/giantswarm/kyverno-policies-ux/compare/v0.7.1...v0.7.2
[0.7.1]: https://github.com/giantswarm/kyverno-policies-ux/compare/v0.7.0...v0.7.1
[0.7.0]: https://github.com/giantswarm/kyverno-policies-ux/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/giantswarm/kyverno-policies-ux/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/giantswarm/kyverno-policies-ux/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/giantswarm/kyverno-policies-ux/compare/v0.3.1...v0.4.0
[0.3.1]: https://github.com/giantswarm/kyverno-policies-ux/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/giantswarm/kyverno-policies-ux/compare/v0.2.3...v0.3.0
[0.2.3]: https://github.com/giantswarm/kyverno-policies-ux/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/giantswarm/kyverno-policies-ux/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/giantswarm/kyverno-policies-ux/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/giantswarm/kyverno-policies-ux/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/giantswarm/kyverno-policies-ux/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/giantswarm/kyverno-policies-ux/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/giantswarm/kyverno-policies-ux/releases/tag/v0.0.1

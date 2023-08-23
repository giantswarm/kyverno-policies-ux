# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0] - 2023-08-22

### Added

- Add ConfigMap and Secret as default targeted resource for `giantswarm.io/prevent-deletion` label.

### Added

- Add policy that blocks deletion of resources with the `giantswarm.io/prevent-deletion` label.

### Changed

- Updates ats, abs and ats python dependencies.

## [0.3.1] - 2023-06-20

## [0.3.0] - 2023-06-20

### Removed

- Stop pushing to `openstack-app-collection`.

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

[Unreleased]: https://github.com/giantswarm/kyverno-policies-ux/compare/v0.4.0...HEAD
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

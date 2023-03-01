# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/giantswarm/kyverno-policies-ux/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/giantswarm/kyverno-policies-ux/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/giantswarm/kyverno-policies-ux/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/giantswarm/kyverno-policies-ux/releases/tag/v0.0.1

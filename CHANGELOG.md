# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [3.0.0] - 2021-03-13
### Removed
- Removed support to legacy Python versions, now supports Python 3.6+.
- Removed ordereddict package dependency.
### Added
- Added support for Python 3.8 and Python 3.9.
- Added option to set custom `user_agent`.
### Changed
- Updated default "User-Agent" to `WooCommerce-Python-REST-API/3.0.0`.
- Updated Request library to 2.25.1.
### Fixed
- Fixed Basic Auth in Python 3.8.

## [2.1.1] - 2019-07-22
### Changed
- Updated Request library to 2.22.0.
- Updated examples.

## [2.1.0] - 2019-01-15
### Changed
- Uses WP REST API by default, need to set `wp_api` as `False` in order to use the legacy WooCommerce API.
- Updated default REST API version to `wc/v3`.

## [2.0.0] - 2019-01-15
### Added
- Added support for custom timestamps in oAuth1.0a requests with `oauth_timestamp`.
- Allow pass custom arguments to "Requests" library..
### Changed
- Updated "Requests" library to version 2.20.0.

## [1.2.1] - 2016-12-14
### Fixed
- Fixed use of `content-type` to fix issues with WordPress 4.7.

## [1.2.0] - 2016-06-22
### Added
- Added option `query_string_auth` to allow Basic Auth as query strings.

## [1.1.1] - 2016-06-03
### Fixed
- Fixed oAuth signature for WP REST API.

## [1.1.0] - 2016-05-09
### Added
- Added support for WP REST API.
- Added method to handle HTTP OPTIONS requests.

## [1.0.5] - 2015-12-07
### Fixed
- Fixed oAuth filters sorting.

## [1.0.4] - 2015-09-25
### Added
- Adds `timeout` argument for `API` class.

## [1.0.3] - 2015-08-07
### Changed
- Forced utf-8 encoding on `API.__request()` to avoid `UnicodeDecodeError`.

## [1.0.2] - 2015-08-05
### Fixed
- Fixed handler for query strings.

## [1.0.1] - 2015-07-13
### Fixed
- Fixed support for Python 2.6.

## [1.0.0] - 2015-07-12
### Added
- Initial release.

[Unreleased]: https://github.com/woocommerce/wc-api-python/compare/3.0.0...HEAD
[3.0.0]: https://github.com/woocommerce/wc-api-python/compare/2.1.1...3.0.0
[2.1.1]: https://github.com/woocommerce/wc-api-python/compare/2.0.1...2.1.1
[2.1.0]: https://github.com/woocommerce/wc-api-python/compare/2.0.0...2.1.0
[2.0.0]: https://github.com/woocommerce/wc-api-python/compare/1.2.1...2.0.0
[1.2.1]: https://github.com/woocommerce/wc-api-python/compare/1.2.0...1.2.1
[1.2.0]: https://github.com/woocommerce/wc-api-python/compare/1.1.1...1.2.0
[1.1.1]: https://github.com/woocommerce/wc-api-python/compare/1.1.0...1.1.1
[1.1.0]: https://github.com/woocommerce/wc-api-python/compare/1.0.5...1.1.0
[1.0.5]: https://github.com/woocommerce/wc-api-python/compare/1.0.4...1.0.5
[1.0.4]: https://github.com/woocommerce/wc-api-python/compare/1.0.3...1.0.4
[1.0.3]: https://github.com/woocommerce/wc-api-python/compare/1.0.2...1.0.3
[1.0.2]: https://github.com/woocommerce/wc-api-python/compare/1.0.1...1.0.2
[1.0.1]: https://github.com/woocommerce/wc-api-python/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/woocommerce/wc-api-python/releases/tag/1.0.0

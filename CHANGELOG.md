# Changelog

All notable changes to this project will be documented in this file.


## [0.0.3] - 2020-06-20

### Changelog

Changelog:
- url variable become public
- Added modes: normal and test mode
 - Normal:
  - Works on real website with requests, for day-to-day use
 - Test:
  - Works on dummy website in /data, only for testing purposes
- Better string formatting
- Corrected variables names
- Corrected small mistakes with mypy
- Splitted main scraper function into smaller ones
- Added sub-class JobOffer
- Changed __repr__ to __str__
- Added better tests

## [0.0.2] - 2020-06-20

### Changelog

- Added argparse
- Added option to skip offer that are older than any day
- Improved classes privacy
- Removed scraper_local.py (replaced with -t)
- Changed tests

## [0.0.1] - 2020-05-30

### Added

- First working version


[0.0.3]: https://github.com/grzesiekdev/indeed_scraper/commit/7598901eb366cf21a20a19d9763a2115568520ce
[0.0.2]: https://github.com/grzesiekdev/indeed_scraper/commit/6f1c34a5e3a38d027015e390b92cedabd1584b16
[0.0.1]: https://github.com/grzesiekdev/indeed_scraper/commit/e9b0e82035925dc025cc3fcba9662fb7da46151c

# Changelog

## [0.2.0] - 
### Added
- Add changelog.
- Add settings stored in config.py file.
- Authentication using jwt token and refresh token.
- Encryption of access_token information in jwt token.

### Changed
- Application has been split into multiple files instead of one main.py file
- Changed port from 8005 to 8000

## [0.1.0] - 2020-08-05
### Added
- Add routes for groups and group resources (issues, boards, labels, members)
- Add mapping of gitlab package response model to match fastapi response models
- Prepare code to use start in container environment

[Unreleased]: https://github.com/GitLab-Helper/gitlab-helper-backend/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/GitLab-Helper/gitlab-helper-backend/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/GitLab-Helper/gitlab-helper-backend/releases/tag/v0.1.0
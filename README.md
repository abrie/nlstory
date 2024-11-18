# nlstory
A tool that converts the issues and PRs of a repository into a story

## Summary List of Non-Pull Request Issues
This tool generates a summary list of all non-pull request issues in the repository using the python GraphQL API and jinja2 Template library.

### Features
- Fetches issues from the repository using the python GraphQL API.
- Generates HTML output for the summary list using the jinja2 Template library.
- Only lists issues that are not pull requests by filtering nodes based on the `__typename` field in the GraphQL response.
- Includes associated pull requests for each issue by fetching `timelineItems` and filtering for `CrossReferencedEvent`.

### Usage
1. Set the `GITHUB_TOKEN` environment variable for authentication.
2. Run the tool to generate the summary list of non-pull request issues and their associated pull requests.

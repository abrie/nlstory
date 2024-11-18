# nlstory
A tool that converts the issues and PRs of a repository into a story

## Summary List of Issues with Associated Pull Requests
This tool generates a summary list of all issues in the repository, including associated Pull Requests listed underneath each issue, using the python GraphQL API and jinja2 Template library.

### Features
- Fetches issues from the repository using the python GraphQL API.
- Generates HTML output for the summary list using the jinja2 Template library.
- Lists associated Pull Requests underneath each issue by querying the `linkedPullRequests` field in the GraphQL response.
- Highlights merged pull requests in the summary output.
- Only lists issues that are not pull requests by filtering nodes based on the `__typename` field in the GraphQL response.

### Usage
1. Set the `GITHUB_TOKEN` environment variable for authentication.
2. Run the tool to generate the summary list of issues with associated Pull Requests.

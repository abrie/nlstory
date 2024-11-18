# nlstory
A tool that converts the issues and PRs of a repository into a story

## Summary List of Issues and Pull Requests
This tool generates a summary list of all issues and pull requests in the repository using the python GraphQL API and jinja2 Template library.

### Features
- Fetches issues and pull requests from the repository using the python GraphQL API.
- Generates HTML output for the summary list using the jinja2 Template library.
- Lists issues and pull requests separately in the generated HTML output.

### Usage
1. Set the `GITHUB_TOKEN` environment variable for authentication.
2. Run the tool to generate the summary list of issues and pull requests.

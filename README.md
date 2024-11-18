# nlstory
A tool that converts the issues and PRs of a repository into a story

## Usage

To use the tool, run the following command:

```
python generate_issue_list.py <repository> <output_file>
```

### Parameters

- `repository`: The name of the repository (e.g., `owner/repo`)
- `output_file`: The name of the output file where the HTML list will be saved

### Example

```
python generate_issue_list.py abrie/nlstory output.html
```

### Requirements

The tool requires the `requests` library. You can install it using the following command:

```
pip install -r requirements.txt
```

### Authentication

The tool uses the `GITHUB_TOKEN` environment variable for authentication. Make sure to set this variable before running the tool.

```
export GITHUB_TOKEN=<your_github_token>
```

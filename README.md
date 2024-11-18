# nlstory
A tool that converts the issues and PRs of a repository into a story

## Usage

To use the CLI tool to generate an HTML list of issues with associated PRs, follow the instructions below:

1. Ensure you have Python installed on your system.
2. Clone this repository to your local machine.
3. Install the required dependencies by running:
   ```
   pip install -r requirements.txt
   ```
4. Set the `GITHUB_TOKEN` environment variable with your Github personal access token:
   ```
   export GITHUB_TOKEN=your_personal_access_token
   ```
5. Run the CLI tool with the following command:
   ```
   python generate_html_list.py --repository <repository> --output <output_file>
   ```

Replace `<repository>` with the name of the repository (e.g., `owner/repo`) and `<output_file>` with the desired output file name (e.g., `output.html`).

## Example

Here is an example command to run the tool:
```
python generate_html_list.py --repository abrie/nlstory --output issues_and_prs.html
```

This will generate an HTML file named `issues_and_prs.html` containing a chronological list of issues and their associated PRs from the `abrie/nlstory` repository.

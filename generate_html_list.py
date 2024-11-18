import os
import requests
from jinja2 import Template

GITHUB_API_URL = "https://api.github.com/graphql"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def run_query(query):
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    response = requests.post(GITHUB_API_URL, json={"query": query}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")

def get_issues_and_prs(repo_owner, repo_name):
    issues_query = """
    {
      repository(owner: "%s", name: "%s") {
        issues(first: 100, states: OPEN) {
          nodes {
            number
            title
            createdAt
            closingIssuesReferences(first: 5) {
              nodes {
                number
                title
              }
            }
          }
        }
        pullRequests(first: 100, states: OPEN) {
          nodes {
            number
            title
            createdAt
          }
        }
      }
    }
    """ % (repo_owner, repo_name)
    result = run_query(issues_query)
    return result["data"]["repository"]["issues"]["nodes"], result["data"]["repository"]["pullRequests"]["nodes"]

def generate_html(issues, prs):
    template = Template("""
    <html>
    <head><title>Issues and PRs</title></head>
    <body>
    <h1>Issues and PRs</h1>
    <ul>
    {% for issue in issues %}
      <li>
        <strong>Issue #{{ issue.number }}: {{ issue.title }}</strong> ({{ issue.createdAt }})
        <ul>
        {% for pr in issue.closingIssuesReferences.nodes %}
          <li>PR #{{ pr.number }}: {{ pr.title }}</li>
        {% endfor %}
        </ul>
      </li>
    {% endfor %}
    </ul>
    </body>
    </html>
    """)
    return template.render(issues=issues, prs=prs)

def main():
    repo_owner = "abrie"
    repo_name = "nlstory"
    issues, prs = get_issues_and_prs(repo_owner, repo_name)
    html_content = generate_html(issues, prs)
    with open("output.html", "w") as f:
        f.write(html_content)

if __name__ == "__main__":
    main()

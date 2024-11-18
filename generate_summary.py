import os
import requests
import jinja2

def fetch_issues():
    url = "https://api.github.com/graphql"
    query = """
    {
      repository(owner: "abrie", name: "nl12") {
        issues(first: 100) {
          nodes {
            __typename
            title
            body
            url
          }
        }
        pullRequests(first: 100) {
          nodes {
            __typename
            title
            body
            url
          }
        }
      }
    }
    """
    headers = {"Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"}
    response = requests.post(url, json={'query': query}, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")
    data = response.json()['data']['repository']
    issues = [issue for issue in data['issues']['nodes'] if issue['__typename'] == 'Issue']
    prs = [pr for pr in data['pullRequests']['nodes'] if pr['__typename'] == 'PullRequest']
    return issues, prs

def generate_html(issues, prs):
    template = jinja2.Template("""
    <html>
    <head><title>Summary of Issues and PRs</title></head>
    <body>
    <h1>Summary of Issues</h1>
    <ul>
    {% for issue in issues %}
      <li><a href="{{ issue.url }}">{{ issue.title }}</a>: {{ issue.body }}</li>
    {% endfor %}
    </ul>
    <h1>Summary of Pull Requests</h1>
    <ul>
    {% for pr in prs %}
      <li><a href="{{ pr.url }}">{{ pr.title }}</a>: {{ pr.body }}</li>
    {% endfor %}
    </ul>
    </body>
    </html>
    """)
    return template.render(issues=issues, prs=prs)

def main():
    issues, prs = fetch_issues()
    html_output = generate_html(issues, prs)
    with open("summary.html", "w") as f:
        f.write(html_output)

if __name__ == "__main__":
    main()

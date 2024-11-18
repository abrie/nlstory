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
            title
            body
            url
          }
        }
        pullRequests(first: 100) {
          nodes {
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
    issues = response.json()['data']['repository']['issues']['nodes']
    pull_requests = response.json()['data']['repository']['pullRequests']['nodes']
    return issues + pull_requests

def generate_html(issues):
    template = jinja2.Template("""
    <html>
    <head><title>Summary of Issues</title></head>
    <body>
    <h1>Summary of Issues</h1>
    <ul>
    {% for issue in issues %}
      <li><a href="{{ issue.url }}">{{ issue.title }}</a>: {{ issue.body }}</li>
    {% endfor %}
    </ul>
    </body>
    </html>
    """)
    return template.render(issues=issues)

def main():
    issues = fetch_issues()
    html_output = generate_html(issues)
    with open("summary.html", "w") as f:
        f.write(html_output)

if __name__ == "__main__":
    main()

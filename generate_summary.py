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
            timelineItems(itemTypes: CROSS_REFERENCED_EVENT, first: 100) {
              nodes {
                ... on CrossReferencedEvent {
                  source {
                    __typename
                    ... on PullRequest {
                      title
                      url
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    """
    headers = {"Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"}
    response = requests.post(url, json={'query': query}, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")
    issues = []
    for issue in response.json()['data']['repository']['issues']['nodes']:
        if issue['__typename'] == 'Issue':
            prs = [item['source'] for item in issue['timelineItems']['nodes'] if item['source']['__typename'] == 'PullRequest']
            issue['associatedPRs'] = prs
            issues.append(issue)
    return issues

def generate_html(issues):
    template = jinja2.Template("""
    <html>
    <head><title>Summary of Issues</title></head>
    <body>
    <h1>Summary of Issues</h1>
    <ul>
    {% for issue in issues %}
      <li>
        <a href="{{ issue.url }}">{{ issue.title }}</a>: {{ issue.body }}
        {% if issue.associatedPRs %}
          <ul>
          {% for pr in issue.associatedPRs %}
            <li><a href="{{ pr.url }}">{{ pr.title }}</a></li>
          {% endfor %}
          </ul>
        {% endif %}
      </li>
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

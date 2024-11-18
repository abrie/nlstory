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
            timelineItems(first: 100) {
              nodes {
                ... on CrossReferencedEvent {
                  source {
                    ... on PullRequest {
                      number
                      title
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
    return [issue for issue in response.json()['data']['repository']['issues']['nodes'] if issue['__typename'] == 'Issue']

def generate_html(issues):
    template = jinja2.Template("""
    <html>
    <head><title>Summary of Issues</title></head>
    <body>
    <h1>Summary of Issues</h1>
    <ul>
    {% for issue in issues %}
      <li><a href="{{ issue.url }}">{{ issue.title }}</a>: {{ issue.body }}
        {% if issue.timelineItems.nodes|length > 0 %}
          <ul>
          {% for event in issue.timelineItems.nodes %}
            {% if event.source.__typename == 'PullRequest' %}
              <li>PR #{{ event.source.number }}: {{ event.source.title }}</li>
            {% endif %}
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

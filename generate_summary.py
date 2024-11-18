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
                __typename
                ... on LabeledEvent {
                  createdAt
                  label {
                    name
                  }
                }
                ... on UnlabeledEvent {
                  createdAt
                  label {
                    name
                  }
                }
                ... on MilestonedEvent {
                  createdAt
                  milestoneTitle
                }
                ... on DemilestonedEvent {
                  createdAt
                  milestoneTitle
                }
                ... on ClosedEvent {
                  createdAt
                }
                ... on ReopenedEvent {
                  createdAt
                }
                ... on AssignedEvent {
                  createdAt
                  assignee {
                    login
                  }
                }
                ... on UnassignedEvent {
                  createdAt
                  assignee {
                    login
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
      <li>
        <a href="{{ issue.url }}">{{ issue.title }}</a>: {{ issue.body }}
        <ul>
        {% for event in issue.timelineItems.nodes %}
          <li>{{ event.createdAt }} - 
            {% if event.__typename == 'LabeledEvent' %}
              Labeled: {{ event.label.name }}
            {% elif event.__typename == 'UnlabeledEvent' %}
              Unlabeled: {{ event.label.name }}
            {% elif event.__typename == 'MilestonedEvent' %}
              Milestoned: {{ event.milestoneTitle }}
            {% elif event.__typename == 'DemilestonedEvent' %}
              Demilestoned: {{ event.milestoneTitle }}
            {% elif event.__typename == 'ClosedEvent' %}
              Closed
            {% elif event.__typename == 'ReopenedEvent' %}
              Reopened
            {% elif event.__typename == 'AssignedEvent' %}
              Assigned to: {{ event.assignee.login }}
            {% elif event.__typename == 'UnassignedEvent' %}
              Unassigned from: {{ event.assignee.login }}
            {% endif %}
          </li>
        {% endfor %}
        </ul>
      </li>
    {% endfor %}
    </ul>
    </body>
    </html>
    """)
    return template.render(issues=issues)

def main():
    issues = fetch_issues()
    for issue in issues:
        issue['timelineItems']['nodes'].sort(key=lambda x: x['createdAt'])
    html_output = generate_html(issues)
    with open("summary.html", "w") as f:
        f.write(html_output)

if __name__ == "__main__":
    main()

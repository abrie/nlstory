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
            number
          }
        }
        pullRequests(first: 100) {
          nodes {
            title
            number
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
    for issue in issues:
        issue['is_pr'] = False
    for pr in pull_requests:
        pr['is_pr'] = True
    return issues + pull_requests

def generate_html(issues):
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("index.html.jinja")
    return template.render(issues=issues)

def main():
    issues = fetch_issues()
    html_output = generate_html(issues)
    with open("index.html", "w") as f:
        f.write(html_output)

if __name__ == "__main__":
    main()

import os
import requests
import jinja2
import re
import markdown2  # P4528

def parse_commit_message_for_issue_references(commit_message):
    issue_references = re.findall(r'#(\d+)', commit_message)
    return [int(issue) for issue in issue_references]

def fetch_issues():
    url = "https://api.github.com/graphql"
    query = """
    {
      repository(owner: "abrie", name: "nl12") {
        issues(first: 100) {
          nodes {
            title
            number
            createdAt
          }
        }
        pullRequests(first: 100) {
          nodes {
            title
            number
            createdAt
            merged
            commits(first: 100) {
              nodes {
                commit {
                  message
                  oid
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
    issues = response.json()['data']['repository']['issues']['nodes']
    pull_requests = response.json()['data']['repository']['pullRequests']['nodes']
    for issue in issues:
        issue['is_pr'] = False
        issue['pull_requests'] = []
    for pr in pull_requests:
        pr['is_pr'] = True
        pr['merged'] = pr.get('merged', False)
        pr['commits'] = [{'message': markdown2.markdown(commit['commit']['message']), 'hash': commit['commit']['oid']} for commit in pr['commits']['nodes']]  # P8dc9
        for commit in pr['commits']:
            referenced_issues = parse_commit_message_for_issue_references(commit['message'])
            for issue_number in referenced_issues:
                for issue in issues:
                    if issue['number'] == issue_number:
                        issue['pull_requests'].append(pr)
                        break
    combined_list = issues + [pr for pr in pull_requests if not any(pr in issue['pull_requests'] for issue in issues)]
    combined_list.sort(key=lambda x: x['createdAt'])
    return combined_list

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

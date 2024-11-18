import os
import sys
import requests
import argparse
import json

def get_issues(repository, token):
    query = """
    {
      repository(owner: "%s", name: "%s") {
        issues(first: 100, states: OPEN) {
          edges {
            node {
              number
              title
              createdAt
              url
              timelineItems(itemTypes: [CROSS_REFERENCED_EVENT], first: 100) {
                edges {
                  node {
                    ... on CrossReferencedEvent {
                      source {
                        ... on PullRequest {
                          number
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
      }
    }
    """ % tuple(repository.split('/'))
    headers = {"Authorization": "Bearer " + token}
    response = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if response.status_code == 200:
        return response.json()['data']['repository']['issues']['edges']
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))

def get_pull_requests(repository, token):
    query = """
    {
      repository(owner: "%s", name: "%s") {
        pullRequests(first: 100, states: OPEN) {
          edges {
            node {
              number
              title
              createdAt
              url
            }
          }
        }
      }
    }
    """ % tuple(repository.split('/'))
    headers = {"Authorization": "Bearer " + token}
    response = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if response.status_code == 200:
        return response.json()['data']['repository']['pullRequests']['edges']
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))

def associate_prs_with_issues(issues, prs):
    issue_pr_map = {}
    for issue in issues:
        issue_pr_map[issue['node']['number']] = {
            'issue': issue['node'],
            'prs': []
        }
        for event in issue['node']['timelineItems']['edges']:
            if 'source' in event['node'] and 'number' in event['node']['source']:
                pr_number = event['node']['source']['number']
                for pr in prs:
                    if pr['node']['number'] == pr_number:
                        issue_pr_map[issue['node']['number']]['prs'].append(pr['node'])
    return issue_pr_map

def generate_html(issue_pr_map):
    html = "<html><body><h1>Issues and Associated PRs</h1><ul>"
    for issue_number in sorted(issue_pr_map.keys()):
        issue = issue_pr_map[issue_number]['issue']
        html += "<li><a href='{}'>{}</a> - {}</li>".format(issue['url'], issue['title'], issue['createdAt'])
        if issue_pr_map[issue_number]['prs']:
            html += "<ul>"
            for pr in issue_pr_map[issue_number]['prs']:
                html += "<li><a href='{}'>{}</a> - {}</li>".format(pr['url'], pr['title'], pr['createdAt'])
            html += "</ul>"
    html += "</ul></body></html>"
    return html

def main():
    parser = argparse.ArgumentParser(description='Generate an HTML list of issues with associated PRs from a Github repository.')
    parser.add_argument('--repository', required=True, help='The repository in the format owner/repo')
    parser.add_argument('--output', required=True, help='The output HTML file')
    args = parser.parse_args()

    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set.")
        sys.exit(1)

    issues = get_issues(args.repository, token)
    prs = get_pull_requests(args.repository, token)
    issue_pr_map = associate_prs_with_issues(issues, prs)
    html = generate_html(issue_pr_map)

    with open(args.output, 'w') as f:
        f.write(html)

if __name__ == "__main__":
    main()

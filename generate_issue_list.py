import os
import sys
import requests
import json

def get_issues(repository, token):
    url = "https://api.github.com/graphql"
    headers = {"Authorization": f"Bearer {token}"}
    query = """
    query($repo: String!, $cursor: String) {
        repository(name: $repo) {
            issues(first: 100, after: $cursor) {
                edges {
                    node {
                        id
                        title
                        createdAt
                        closedAt
                        url
                        closingIssuesReferences(first: 5) {
                            nodes {
                                id
                                title
                                url
                            }
                        }
                    }
                }
                pageInfo {
                    endCursor
                    hasNextPage
                }
            }
        }
    }
    """
    issues = []
    cursor = None
    while True:
        variables = {"repo": repository, "cursor": cursor}
        response = requests.post(url, headers=headers, json={"query": query, "variables": variables})
        data = response.json()
        issues.extend(data["data"]["repository"]["issues"]["edges"])
        if not data["data"]["repository"]["issues"]["pageInfo"]["hasNextPage"]:
            break
        cursor = data["data"]["repository"]["issues"]["pageInfo"]["endCursor"]
    return issues

def get_pull_requests(repository, token):
    url = "https://api.github.com/graphql"
    headers = {"Authorization": f"Bearer {token}"}
    query = """
    query($repo: String!, $cursor: String) {
        repository(name: $repo) {
            pullRequests(first: 100, after: $cursor) {
                edges {
                    node {
                        id
                        title
                        createdAt
                        closedAt
                        url
                    }
                }
                pageInfo {
                    endCursor
                    hasNextPage
                }
            }
        }
    }
    """
    pull_requests = []
    cursor = None
    while True:
        variables = {"repo": repository, "cursor": cursor}
        response = requests.post(url, headers=headers, json={"query": query, "variables": variables})
        data = response.json()
        pull_requests.extend(data["data"]["repository"]["pullRequests"]["edges"])
        if not data["data"]["repository"]["pullRequests"]["pageInfo"]["hasNextPage"]:
            break
        cursor = data["data"]["repository"]["pullRequests"]["pageInfo"]["endCursor"]
    return pull_requests

def associate_issues_with_prs(issues, pull_requests):
    pr_dict = {pr["node"]["id"]: pr["node"] for pr in pull_requests}
    for issue in issues:
        issue["node"]["associatedPRs"] = []
        for pr in issue["node"]["closingIssuesReferences"]["nodes"]:
            if pr["id"] in pr_dict:
                issue["node"]["associatedPRs"].append(pr_dict[pr["id"]])
    return issues

def generate_html(issues, output_file):
    issues.sort(key=lambda x: x["node"]["createdAt"])
    with open(output_file, "w") as f:
        f.write("<html><body><ul>\n")
        for issue in issues:
            f.write(f'<li><a href="{issue["node"]["url"]}">{issue["node"]["title"]}</a>\n')
            if issue["node"]["associatedPRs"]:
                f.write("<ul>\n")
                for pr in issue["node"]["associatedPRs"]:
                    f.write(f'<li><a href="{pr["url"]}">{pr["title"]}</a></li>\n')
                f.write("</ul>\n")
            f.write("</li>\n")
        f.write("</ul></body></html>\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_issue_list.py <repository> <output_file>")
        sys.exit(1)
    repository = sys.argv[1]
    output_file = sys.argv[2]
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set")
        sys.exit(1)
    issues = get_issues(repository, token)
    pull_requests = get_pull_requests(repository, token)
    issues = associate_issues_with_prs(issues, pull_requests)
    generate_html(issues, output_file)

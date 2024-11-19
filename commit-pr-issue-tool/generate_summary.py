import os
import requests
import jinja2
import markdown2

def fetch_commits():
    url = "https://api.github.com/graphql"
    query = """
    {
      repository(owner: "abrie", name: "nl12") {
        defaultBranchRef {
          target {
            ... on Commit {
              history(first: 100) {
                edges {
                  node {
                    message
                    oid
                    committedDate
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
    commits = response.json()['data']['repository']['defaultBranchRef']['target']['history']['edges']
    return [{'message': markdown2.markdown(commit['node']['message']), 'sha': commit['node']['oid'], 'date': commit['node']['committedDate']} for commit in commits]

def generate_html(commits):
    template_loader = jinja2.FileSystemLoader(searchpath="./commit-pr-issue-tool")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("index.html.jinja")
    return template.render(commits=commits)

def main():
    commits = fetch_commits()
    html_output = generate_html(commits)
    with open("commit-pr-issue-tool/index.html", "w") as f:
        f.write(html_output)

if __name__ == "__main__":
    main()

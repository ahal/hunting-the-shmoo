import os
import sys
from datetime import datetime
from pathlib import Path

import yaml
from github import Github

here = Path(__file__).parent.resolve()
COMMENTS_DIR = here / 'data' / 'comments'

if 'GITHUB_ACCESS_TOKEN' not in os.environ:
    print("Set the GITHUB_ACCESS_TOKEN environment")
    sys.exit(1)


def submit_comments(comments):
    g = Github(os.environ['GITHUB_ACCESS_TOKEN'])
    repo = g.get_repo("ahal/hunting-the-shmoo")

    for comment in comments:
        date = datetime.strptime(comment['date'], "%Y-%m-%dT%H:%M:%S%z")
        title = f"blog/{date.year}/{comment['slug']}/"

        issue = None
        for i in repo.get_issues(state='open'):
            if i.title == title:
                issue = i
                break
        else:
            body = f"https://ahal.ca/{title}"

            kwargs = {
                'body': body,
                'labels': ['comment'],
                'title': title,
            }
            issue = repo.create_issue(**kwargs)

        issue.create_comment(f"""
**{comment['name']}** wrote on *{date.strftime("%Y-%m-%d %H:%M:%S")}*

{comment['msg']}
""")


def load_comments(comments_dir):
    comments = []
    for path in comments_dir.glob('**/*.yml'):
        with open(path, 'r') as fh:
            yield yaml.safe_load(fh)

comments = sorted(load_comments(COMMENTS_DIR), key=lambda c: c['date'])
submit_comments(comments)

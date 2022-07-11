__version__ = "0.1.0"

import json
import os
import sys
from github import Github  # pip install --user PyGithub


def scan_repo(repo):
    files = {}
    root_content = repo.get_contents("/")
    root_files = [f.name for f in root_content]
    files["/"] = root_files

    for subfolder in ("docs", ".github", ".circleci"):
        if subfolder not in root_files:
            continue
        sub_content = repo.get_contents(f"/{subfolder}")
        docs_files = [f.name for f in sub_content]
        files[f"/{subfolder}"] = docs_files

    makefile = None
    if "Makefile" in root_files:
        contentfile = repo.get_contents("Makefile")
        makefile = contentfile.decoded_content.decode("utf-8")

    readme = None
    for rm in ("README", "README.md", "README.rst"):
        if rm in root_files:
            contentfile = repo.get_contents(rm)
            readme = contentfile.decoded_content.decode("utf-8")

    return {
        "name": repo.name,
        "files": files,
        "makefile": makefile,
        "readme": readme,
    }


if __name__ == "__main__":
    g = Github(os.getenv("TOKEN"))
    org = os.getenv("ORG", "mozilla-services")

    print("[")

    org = g.get_organization(org)
    for repo in org.get_repos(sort="pushed"):
        if repo.archived:
            continue
        try:
            report = scan_repo(repo)
            print(json.dumps(report, indent=2), end=",\n")
        except Exception as e:
            sys.stderr.write(f"{repo}: {e}")

    print("]")

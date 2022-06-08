#!/bin/python

import requests, json, git

class GHRepo:
    def __init__(self, name, url):
        self.name = name
        self.url = url

github_user = None
clone_dir = None

def GetRepos(user, response_data):
    if(type(response_data).__name__ != "list"):
        return None
    if not len(response_data):
        return None

    repo_list = []
    for repo in response_data:
        repo_list.append(GHRepo(repo["name"], repo["html_url"]))

    return repo_list

if __name__ == "__main__": # main()
    github_user = input("Please enter your username:")
    print("Getting user...")
    ret = requests.get(f"https://api.github.com/users/{github_user}/repos")
    if ret.status_code == 200:
        clone_dir = input("Clone Directory(abs/relative, nothing for current dir):")
        if not clone_dir:
            clone_dir = "."
        jsonized = None
        try:
            jsonized = json.loads(ret.content)
        except:
             print("Failed to serialize request")
        if jsonized:
            repos = GetRepos(github_user,jsonized)
            if repos and len(repos):
                print(f"Got {len(repos)} repos")
                for repo in repos:
                    print(f"Cloning {repo.name}({repo.url})..")
                    try:
                        git.Repo.clone_from(repo.url, clone_dir + "/" + repo.name)
                    except git.GitCommandError as GCE:
                        print(f"Failed to clone {repo.name} into " + clone_dir + "/" + repo.name)
                        if "already exists" in GCE.stderr:
                            print("Directory " + clone_dir + "/" + repo.name + " already exists")
                    except:
                        print(f"Failed to clone {repo.name} into " + clone_dir + "/" + repo.name)
            else:
                print("No repositories were found")
        else:
            print("Failed to parse data")
    else:
        print("Account not found")

# run infer by infer.py
import sys
import subprocess
import os
from github import Github

import infer
import sonar


git_project = ''        # target project on github
user_token = ''         # git authority

def printf(format, *args):
    sys.stdout.write(format % args)

# return path directory
def parseInputToPath(args):
    return args[1]

def getGitReleases(project, token):
    # Put your GitHub token here
    G = Github(token)
    repo = G.get_repo(project)
    releases = repo.get_releases()
    for release in releases:
        print(release)


if __name__ == '__main__':
    # first read in user info
    git_project = input("Target git project: (eg. eclipse/ditto)")
    user_token = input("Your github access token: ")
    getGitReleases(git_project, user_token)
    chosen_release = input("Input release to be analyzed: ")
    print(chosen_release)
    change_directory = input("Where is your project: ")
    print(change_directory)
    
    # move to the directory and change the tags
    os.chdir(change_directory)
    os.system("git checkout tags/"+chosen_release)
    

    # after some manipulation -----------------------------------
    # os.system("git checkout master")
    sonar.sonar_analyze()

    # Store in DB

    os.system("git checkout master")
    sys.exit()
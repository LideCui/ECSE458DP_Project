# run infer by infer.py
import sys
import subprocess
from github import Github
import os

def printf(format, *args):
    sys.stdout.write(format % args)

# return path directory
def parseInputToPath(args):
    return args[1]

def getGitReleases(args):
    # Put your GitHub token here

    G = Github("")  
    repo = G.get_repo("eclipse/paho.mqtt.java")
    releases = repo.get_releases()
    for release in releases:
        print(release)

def infer_analyze():
    # changeDirectory = "cd ./paho.mqtt.java"
    # path = parseInputToPath(sys.argv)
    path = input("Input your infer target path: ")
    os.chdir(path)

    runInfer="infer run -o /output -- mvn compile -DskipTests -Dlicense.skip=true"
    # subprocess.call(runInfer.split(), cwd=path)
    os.system(runInfer)

    # getGitReleases(sys.argv)

if __name__ == '__main__':
    infer_analyze()
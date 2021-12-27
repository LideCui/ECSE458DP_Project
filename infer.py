# run infer by infer.py
import sys
import subprocess
from git import GitHub

def printf(format, *args):
    sys.stdout.write(format % args)

# return path directory
def parseInputToPath(args):
    return args[1]

def getGitReleases(args):
    # Put your GitHub token here
    G = Github("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")  
    repo = G.get_repo("eclipse/paho.mqtt.java")
    releases = repo.get_releases()
    for release in releases:
        print(release)

if __name__ == '__main__':
    changeDirectory = "cd ./paho.mqtt.java"
    path = parseInputToPath(sys.argv)
    """
    print(sys.argv)
    runInfer="infer analyze -- mvn verify -DskipTests"
    subprocess.call(runInfer.split(), cwd=path)
    """
    getGitReleases(sys.argv)
    sys.exit()
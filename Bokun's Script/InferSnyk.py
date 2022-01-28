import os
import subprocess
import fileinput
from asyncore import file_wrapper
from builtins import print


def snyk_analysis(version_list, index):
    os.system("git reset --hard")
    os.system("git checkout master")
    current = version_list[index]
    subprocess.run(['git', 'checkout', 'tags/' + current], stdout=subprocess.DEVNULL) # run command, supress CLI stdout
    os.system("snyk code test --json > SnykOut.json")  # store report in a new file "SnykOut.json"
    os.system("cp SnykOut.json ~/Downloads/LeShanReports/Snyk/" + str(current) + ".json")


# example of automated fix of plugin version...not particularly useful is the fix isn't same across versions
def plugin_fix():
    found = False
    for line in fileinput.input(files='pom.xml', inplace=True):
        if found:
            print("                    <version>5.1.1</version>")
            found = False
            continue
        print(line[:-1])
        if "maven-bundle-plugin" in line:
            found = True


def infer_analysis(version_list, index):
    # index of "leshan-1.0.0-M9" = 28
    os.system("git reset --hard")
    os.system("git checkout master")
    current = version_list[index]
    subprocess.run(['git', 'checkout', 'tags/' + current], stdout=subprocess.DEVNULL)
    plugin_fix()
    input("fix your pom, press enter when ready:")

    print("analyzing version " + current + "...")
    subprocess.run(['infer', 'run', '--', 'mvn', 'clean', 'verify', '-DskipTests'], stdout=subprocess.DEVNULL)
    os.system("cp infer-out/report.json ~/Downloads/LeShanReports/Infer/" + str(current) + ".json")
    print("\n=====report for " + str(current) + " extracted to target folder=====\n")


def init():
    print("\n\nHello, I'm here to partially automate Infer/Snyk Analysis on releases of Eclipse LeShan Project.")
    # Assume currently in "Downloads" folder
    os.chdir("../Downloads/leshan")
    os.system("git reset --hard")
    os.system("git checkout master")
    os.system("git pull --ff-only")
    os.system("git config --global advice.detachedHead false")
    print("Current directory: " + subprocess.check_output(["pwd"]).decode("utf-8"))
    list_files = subprocess.check_output(["git", "tag"])  # store CLI stdout into variable "list_files"
    all_versions = list_files.decode("utf-8").strip("\n").split("\n")
    print("No. of versions: " + str(len(all_versions)))
    return all_versions


if __name__ == '__main__':
    # Analysis
    versions = init()
    count = len(versions)
    for i in range(26, count):  # "leshan-1.0.0-M7 " is at index 26
        # infer_analysis(versions, i)
        snyk_analysis(versions, i)
        print("hello")

    print("finished!!")

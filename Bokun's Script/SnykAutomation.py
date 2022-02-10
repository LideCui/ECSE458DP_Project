import os
import subprocess
import json
import copy
from builtins import print
import matplotlib.pyplot as plt

project_url = "https://github.com/eclipse/ditto.git"  # the web URL
project_name = "ditto"  # the cloned folder name

# statistics (each element in the list is for a specific release)
versions = []  # list of all tags
total = []  # list of total issues count
source = []  # list of source code issues count
test = []  # list of test code issues count
fixed = []  # list of fixed issues count
introduced = []  # list of new issues count
pre = []  # list of old issues count
unique = []  # list of encountered unique issues count


def plot_graph(dict):
    # dict: ['fingerprint' : '["introVersion", "EndVersion", <dict>]']
    # TODO: more sophisticated graph using data stored in dict
    plt.title(project_name)
    plt.plot(versions, total, '.-', label='total issues')
    plt.plot(versions, source, '.-', label='source code issues')
    plt.plot(versions, test, '.-', label='test code issues')
    plt.plot(versions, fixed, '.-', label='fixed issues')
    plt.plot(versions, introduced, '.-', label='new issues')
    plt.plot(versions, pre, '.-', label='old issues')
    plt.plot(versions, unique, '.-', label='unique issue count')
    plt.yticks(list(range(0, max(max(total), max(unique))+1)))
    plt.tick_params(axis='x', labelcolor='r', labelsize=10, rotation=90)
    plt.legend()
    plt.show()
    return


# Read in content of json report, return two lists of dictionaries. each dictionary is an issue
# update the record (passed in as a pointer) to keep track of all issues.
def parse_snyk_report(version, record, prev_no_of_issues):
    f = open(version + ".json")
    sample_report = json.load(f)

    # sample_report["runs"][0]["results"] is a "list" of "dict" objects, each entry is an issue
    sample_report = sample_report["runs"][0]["results"]
    source_code_issues = copy.deepcopy(sample_report)
    test_code_issues = []
    fix = 0
    new = 0
    preexist = 0
    for entry in sample_report:
        # separate test code issues from source code issues
        if "/test" in str(entry['ruleId']):
            source_code_issues.remove(entry)
            test_code_issues.append(entry)
    for entry in source_code_issues:  # Mainly care about source code issues, track their lifecycles
        # fingerprint "0" uses both line numbers and file path
        # fingerprint "1" uses line content and NOT file path
        # since line number changes quite often, leading to "false new", we don't use fingerprint "0"
        # repeated fingerprint "1" within the same report implies same type of issue at two different location
        # OK to treat as "one" issue
        # key = str(str(entry['fingerprints']['0']) + str(entry['fingerprints']['1']))
        key = str(str(entry['fingerprints']['1']))
        if key not in record.keys():
            # Above comparison works...data types in python is magical
            # new discovered issue that got introduced in this version, add to record
            record[key] = [version, None, entry]
            new += 1
        elif record[key][0] == version:
            # repeated hash code within the same report
            # design decision: ignore.
            print("repeated hash code within the same report: " + key)
            continue
        else:
            # pre-existed issue, update endVersion
            record[key][1] = [version]
            preexist += 1
        # an unmodified entry in record means it is resolved in previous version
        # which is fine because its entry contains correct intro/end version stamping
    fix = prev_no_of_issues - preexist
    print("version: " + version + " summary:")
    print("\tno. of issues in raw report: " + str(len(sample_report)))
    total.append(len(sample_report))
    print("\tno. of issues in source code report: " + str(len(source_code_issues)))
    source.append(len(source_code_issues))
    print("\tno. of issues in test code report: " + str(len(test_code_issues)))  # SUCCESS!~
    test.append(len(test_code_issues))
    print("\tno. of fixed issues: " + str(fix))
    fixed.append(fix)
    print("\tno. of new issues: " + str(new))
    introduced.append(new)
    print("\tno. of pre-existing issues: " + str(preexist))
    pre.append(preexist)
    print("\tsize of recorded issues: " + str(len(record)) + '\n')
    unique.append(len(record))
    return len(source_code_issues)  # source_code_issues, test_code_issues (or don't return anything)


def snyk_analysis(version_list, index):
    os.system("git reset --hard")
    os.system("git checkout master")
    current = version_list[index]
    subprocess.run(['git', 'checkout', 'tags/' + current], stdout=subprocess.DEVNULL)  # run command, supress CLI stdout
    print("starting Snyk analysis on: " + current + "...")
    os.system("snyk code test --json > SnykOut.json")  # store report in a new file "SnykOut.json"
    os.chdir("..")
    os.system("cp " + project_name + "/SnykOut.json " + project_name + "versionReports/" + str(current) + ".json")
    os.chdir(project_name)


def init():
    print("\n\nHello, I'm here to automate Snyk Analysis on releases of Eclipse " + project_name + " Project.")
    os.system("git clone " + project_url)
    os.system("mkdir " + project_name + "versionReports")  # create new directory to store all reports
    os.chdir(project_name)
    os.system("git reset --hard")
    os.system("git checkout master")
    os.system("git pull --ff-only")
    os.system("git config --global advice.detachedHead false")
    print("Current directory: " + subprocess.check_output(["pwd"]).decode("utf-8"))
    # store CLI stdout into variable "list_files"
    list_files = subprocess.check_output(["git", "tag", "--sort=creatordate"])
    all_versions = list_files.decode("utf-8").strip("\n").split("\n")
    print("No. of versions: " + str(len(all_versions)))
    return all_versions


if __name__ == '__main__':

    # Initialization
    versions = init()
    print(versions)
    count = len(versions)
    print("total no. of releases (tags): " + str(count))
    print("\n============================Initialization Complete!=============================\n")
    # input("press enter to continue:")

    # Analysis
    # for i in range(0, count):
    #     snyk_analysis(versions, i)
    print("\n===============================Analysis Finished!!===============================\n")

    # Parse
    os.chdir("../" + project_name + "versionReports")
    # create a dictionary to track of each issue's lifecycle, each entry in dict has format:
    # ['fingerprint' : '["introVersion", "EndVersion", <dict>]']
    # where the <dict> object contains the issue itself
    track_lifecycle = dict()
    prev_issue_count = 0
    for i in range(0, count):  # index 35 is leshan-1.3.0
        prev_issue_count = parse_snyk_report(versions[i], track_lifecycle, prev_issue_count)
    print("\n=============================Report Parse Finished!!=============================\n")

    # Plot
    plot_graph(track_lifecycle)

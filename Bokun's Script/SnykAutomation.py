import os
import subprocess
import json
import copy
from builtins import print
import matplotlib.pyplot as plt
import projectStatistics

project_url = "https://github.com/eclipse/leshan.git"  # the web URL

project_name = "leshan"  # the cloned folder name

# statistics (each element in the following list is for a specific release)
versions = []  # list of all tags
total = []  # list of total issues count
source = []  # list of source code issues count
test = []  # list of test code issues count
fixed = []  # list of fixed issues count
introduced = []  # list of new issues count
pre = []  # list of old issues count
unique = []  # list of encountered unique issues count
no_of_lines = []  # list of statistics: no. of lines
no_of_files = []  # list of statistics: no. of files

addition_btw_tags = []
deletion_btw_tags = []
verify_stat = []

file_ratio = []
loc_ratio = []
new_issue_new_line_ratio = []


def count_add_and_del(version_list):
    print("=====in count_add_and_del====")
    print("in directory: " + os.getcwd())
    for i in range(0, count-1):
        tokens = subprocess.run(["git", "diff", "--shortstat",
                                 version_list[i], version_list[i + 1], "--", "*.java", "*.js"],
                                check=True, stdout=subprocess.PIPE, text=True).stdout.strip("\n").split(" ")
        addition_btw_tags.append(int(tokens[4]))
        deletion_btw_tags.append(int(tokens[6]))


def plot_graph(dict):
    # dict: ['fingerprint' : '["introVersion", "EndVersion", <dict>]']
    # TODO: more sophisticated graph using data stored in dict
    plt.figure()
    plt.title(project_name + ": basic issue counts")
    plt.plot(versions, total, '.-', label='total issues')
    plt.plot(versions, source, '.-', label='source code issues')
    plt.plot(versions, test, '.-', label='test code issues')
    plt.plot(versions, fixed, '.-', label='fixed issues')
    plt.plot(versions, introduced, '.-', label='new issues')
    plt.plot(versions, pre, '.-', label='old issues')
    plt.plot(versions, unique, '.-', label='unique issue count')
    plt.yticks(list(range(0, max(max(total), max(unique)) + 1)))
    plt.tick_params(axis='y', labelcolor='black', labelsize=5)
    plt.tick_params(axis='x', labelcolor='black', labelsize=8, rotation=90)
    plt.legend()
    # plt.axvline(x="leshan-1.3.2", color='black')
    plt.margins(x=0.01)
    plt.subplots_adjust(left=0.02, right=0.98, bottom=0.2)
    plt.grid(visible='true', axis='y', color='grey', linestyle='--')

    # #issues / #lines (java and javascript, test code included)
    plt.figure()
    plt.title(project_name + ": # issues / #lines")
    plt.plot(versions, loc_ratio, '.-', label='#issues/#lines')
    plt.tick_params(axis='y', labelcolor='black', labelsize=5)
    plt.tick_params(axis='x', labelcolor='black', labelsize=8, rotation=90)
    plt.margins(x=0.01)
    plt.subplots_adjust(left=0.05, right=0.98, bottom=0.2)
    plt.grid(visible='true', axis='y', color='grey', linestyle='--')
    plt.legend()
    plt.show()

    # # new issues / # new lines (java and javascript, test code included)
    plt.figure()
    plt.title(project_name + ": # new issues / # new lines")
    plt.plot(versions, new_issue_new_line_ratio, '.-', label='#issues/#lines')
    plt.tick_params(axis='y', labelcolor='black', labelsize=5)
    plt.tick_params(axis='x', labelcolor='black', labelsize=8, rotation=90)
    plt.margins(x=0.01)
    plt.subplots_adjust(left=0.05, right=0.98, bottom=0.2)
    plt.grid(visible='true', axis='y', color='grey', linestyle='--')
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
    stats = projectStatistics.count_files_and_lines()  # stats is a tuple
    no_of_files.append(stats[0])
    no_of_lines.append(stats[1])
    # print("starting Snyk analysis on: " + current + "...")
    # os.system("snyk code test --json > SnykOut.json")  # store report in a new file "SnykOut.json"
    os.chdir("..")
    # os.system("cp " + project_name + "/SnykOut.json " + project_name + "versionReports/" + str(current) + ".json")
    os.chdir(project_name)
    return


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
    # use "--sort=creatordate" if tags on github already have correct versioning order. E.g. Kapua
    # if not, use "--sort=version:refname", then manually place M-releases & RC-releases before gold releases
    # (e.g. see hono_rearrange())
    list_files = subprocess.check_output(["git", "tag", "--sort=creatordate"])
    # "list_files" stores CLI stdout
    all_versions = list_files.decode("utf-8").strip("\n").split("\n")
    print("No. of versions: " + str(len(all_versions)))
    return all_versions


# swap two elements
def swap(array, low, high):
    e1 = array.pop(high)
    e2 = array.pop(low)
    array.insert(low, e1)
    array.insert(high, e2)
    return


# used specifically for leshan due to branching releases pipeline
def leshan_rearrange(ver_list):
    swap(ver_list, 35, 36)  # 35 at 2.0.0-M1
    swap(ver_list, 36, 38)
    swap(ver_list, 37, 38)
    e = ver_list.pop(42)
    ver_list.insert(37, e)


# used specifically for kura due to branching releases pipeline
def kura_rearrange(ver_list):
    ver_list.pop(65)
    ver_list.pop(63)
    ver_list.pop(61)
    ver_list.remove("BUILD_MARKER")


# used specifically for kapua due to branching releases pipeline
def kapua_rearrange(ver_list):
    ver_list.pop(40)
    ver_list.pop(39)
    ver_list.pop(37)
    swap(ver_list, 21, 22)
    ver_list.pop(0)


# used specifically for hono due to branching releases pipeline
def hono_rearrange(ver_list):
    length = len(ver_list)
    for i in range(1, length):
        if ("-M" in ver_list[i]) and ("-M" not in ver_list[i - 1]):  # need to move previous element
            j = i
            while (ver_list[i - 1] + "-M") in ver_list[j]:
                # keep moving the element forward until pass all Milestones
                j += 1
            gold = ver_list.pop(i - 1)
            ver_list.insert(j - 1, gold)
    ver_list.pop(0)  # snyk error when running 0.5-M1, discard
    return


# used specifically for paho due to branching releases pipeline
def paho_rearrange(ver_list):
    ver_list.remove("help")


if __name__ == '__main__':

    input(" press enter to start automation script: ")  # for safety
    # Initialization
    versions = init()
    leshan_rearrange(versions)
    # kura_rearrange(versions)
    # hono_rearrange(versions)
    # kapua_rearrange(versions)
    # paho_rearrange(versions)
    count = len(versions)
    print(versions[0])
    print("total no. of releases (tags): " + str(count))
    count_add_and_del(versions)
    # print(str(versions.index("1.1.0-M1")))
    print("\n============================Initialization Complete!=============================\n")
    input("press enter to continue:")

    # Analysis
    for i in range(0, count):
        snyk_analysis(versions, i)
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

    verify_stat.append(no_of_lines[0])  # first version same
    addition_btw_tags.insert(0, no_of_lines[0]) # first version, use total no. of lines as "addition"
    deletion_btw_tags.insert(0, 0)  # first version, use 0 as no. of deleted lines
    for i in range(0, count):
        # compute ratio
        file_ratio.append(total[i] / float(no_of_files[i]))
        loc_ratio.append(total[i] / float(no_of_lines[i]))
        new_issue_new_line_ratio.append(introduced[i] / float(addition_btw_tags[i]))

        if i != count - 1:
            verify_stat.append(no_of_lines[i] + addition_btw_tags[i] - deletion_btw_tags[i])

    # verification
    print("no of element in addition_btw_tags: " + str(len(addition_btw_tags)))
    print("no of element in deletion_btw_tags: " + str(len(deletion_btw_tags)))
    print("no of element in no_of_lines: " + str(len(no_of_lines)))
    print("no_of_lines: " + str(no_of_lines))
    print("verify_stat: " + str(verify_stat))
    # Expectation: no_of_lines[n+1] = no_of_lines[n] + addition_btw_tags[n] - deletion_btw_tags[n]
    # Plot
    input("pause, press enter to plot graph:")
    print("introduced: " + str(introduced))
    print("addition_btw_tags: : " + str(addition_btw_tags))
    plot_graph(track_lifecycle)

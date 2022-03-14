# author: Zichen

# -------------------------------- import area --------------------------------
from ctypes.wintypes import HACCEL
from ensurepip import version
import os
import subprocess
import re
import json
import matplotlib.pyplot as plt
import numpy as np
import c_projectStatistics


# --------------------------- function definition -----------------------------
# function to compare the outputs produced by PVS-Studio
def pvs_report_compare(old_version, new_version):
    result = [0, 0, 0]  # [old, new, both]
    with open(old_version + ".txt") as old, open(new_version + ".txt") as new:
        old_list = old.read().splitlines()         # read in the lines without the newline char
        new_list = new.read().splitlines()

        # obtain set properties
        both = []
        itr = old_list.copy()
        for item in itr:
            if item in new_list:
                new_list.remove(item)
                old_list.remove(item)
                both.append(item)

        print("fixed" + "(" + str(len(old_list)) + ")" + ": " + str(old_list) + "\n")
        print("introduced" + "(" + str(len(new_list)) + ")" + ": " + str(new_list)+ "\n")
        print("pre-existing" + "(" + str(len(both)) + ")" + ": " + str(both)+ "\n")

        result[0] = len(old_list)
        result[1] = len(new_list)
        result[2] = len(both)
    return result


''' 
Function to count number of appearance for each type of vulnerability

tag: specific release version of the project
path: path to the working directory
Return: total count of issues, severity count, code count
'''
def pvs_num_of_issues_per_type_one_release(tag, path_to_project, verbal=False, include_test=True):
    with open(path_to_project + tag + ".txt") as f:
        lines = f.read().splitlines()         # read in the lines without the newline char  
    # my severity count table    
    severity_table = {
          "High": 0,
          "Medium": 0,
          "Low": 0
    }
    # my code count table
    Vcode_table = {}
    # total issue counter
    total_issues = 0
    # then iterate through each line to parse:
    for line in lines:
        ## FIRST SPLIT THE LINE
        # split[0] is the severity, split[1] is the issue code(VXXX), split[2] is the rest
        split = re.split("\s", line, 2)     # get the severity and issue type info from split
        severity, code = split[0][0:-1], split[1]
        # print the path of the occurrence of the issue
        content_btw_squarebracket = re.findall("\[(.*?)\]", split[2])
        path = re.split(", ", content_btw_squarebracket[-1])    # only at the end of the list is my path
        
        issue_count = 0
        if (include_test == False):
            for p in path:
                if ('test' not in p):
                    issue_count += 1
        else:
            issue_count = len(path)

        ## THEN COUNT
        # totalissues
        total_issues += issue_count
        # severity count
        if severity == "High":
            severity_table["High"] += issue_count
        elif severity == "Medium":
            severity_table["Medium"] += issue_count
        else: 
            severity_table["Low"] += issue_count
        # issue type count
        if code in Vcode_table:
            Vcode_table[code] += issue_count
        else: 
            Vcode_table[code] = issue_count

    if verbal:
        print(f"Total Issues Found: {total_issues} at version: {tag}")
        print(f"================================")
        print(f"Severity Report: ")
        print(f"  High has: {severity_table['High']}")
        print(f"  Medium has: {severity_table['Medium']}")
        print(f"  Low has: {severity_table['Low']}")
        print(f"    =====                       ")
        print(f"Issue Type Found: ")
        print(Vcode_table)
        print("============= done ==============")
    return total_issues, severity_table, Vcode_table


# function to start the pvs analyzer
# Assumption:
## 1. the pom.xml file has been correctly modified
def pvs_run(path_to_project):
    os.chdir(path_to_project)
    os.system("mvn pvsstudio:pvsAnalyze")


'''
Function to calculate changed number of lines between all tags.

path_to_project: path to the working directory
return: the list of tags
'''
def cal_changed_lines(path_to_project):
    str = subprocess.check_output(['git', 'tag', '--sort=creatordate'], cwd=path_to_project)
    tag_lst = str.decode("utf-8").split("\n")[:-1]         ## decode the bytes into string and drop last term

    print(f"Original tag list {tag_lst} with size {len(tag_lst)}")
    leshan_rearrange(tag_lst)

    ## check the changed lines and files information in consecutive versions
    changed_lst = ['null']                                 ## have a null at the first tag since it has no version to compare with
    for i in range(len(tag_lst) - 1):
        str = subprocess.check_output(['git', 'diff', '--shortstat', tag_lst[i], tag_lst[i+1], '*.java'],cwd=path_to_project)
        changed_lst.append(str.decode('utf8').split("\n")[0])

    ## then parse the changed lst:
    file_change = [1]          ## change of files
    add_change = [1]           ## addition of lines
    del_change = [1]           ## deletion of lines
    for i in range(1, len(changed_lst)):
        tmp = [int(s) for s in changed_lst[i].split() if s.isdigit()]
        file_change.append(tmp[0])
        add_change.append(tmp[1])
        del_change.append(tmp[2])
    return tag_lst, changed_lst, file_change, add_change, del_change


'''
Function to plot the result of statistics along versions of project.

version_list: tags of the project
path_to_project: path to the working directory
changed_lst: changed information across the versions
'''
def pvs_plot_comparison(version_list, path_to_output, changed_lst=None, file_change=None, add_change=None, del_change=None
, num_of_lines=None, num_of_files=None):
    ## first create empty statistics lists
    total_list = []
    severity_h_list = []
    severity_m_list = []
    severity_l_list = []
    code_list = []
    pretty_version_list = []   # a prettier version list parsed from the 7th index
    # count the differences between releases:
    last_total = 0
    total_diff = []

    ## count issues per version
    for v in version_list:
        total, severity, code = pvs_num_of_issues_per_type_one_release(v, path_to_output, include_test=False)
        total_diff.append(total - last_total)
        last_total = total
        total_list.append(total)
        severity_h_list.append(severity['High'])
        severity_m_list.append(severity['Medium'])
        severity_l_list.append(severity['Low'])
        code_list.append(code)
        pretty_version_list.append(v[7:])



    # modify the first element of issue_difference is 0
    total_diff[0] = 0

    # calculate a list of new issues:
    new_issues = []
    for i in range(len(total_diff)):
        if total_diff[i] < 0:
            new_issues.append(0)
        else:
            new_issues.append(total_diff[i])
 
    # calculate net lines changed(dirivative)
    net_lines_changed = np.array(add_change)-np.array(del_change)

    # calculate differential of issues/net_line_changed
    issue_differential_per_tag = np.array(total_diff) / np.array(net_lines_changed)

    # calculate total_issues per lines each tag:
    total_issues_per_lines = np.array(total_list) / np.array(num_of_lines)

    # calculate total_issues per java files each tag:
    total_issues_per_java = np.array(total_list) / np.array(num_of_files)

    # calculate new issues per added lines:
    new_issues_per_new_lines = np.array(new_issues) / np.array(add_change)

    # calculate the new issues per files changed
    issue_diff_per_file_changed = np.array(new_issues) / np.array(file_change)

    ## plotting-1
    _, plots_total = plt.subplots(2, 2)
    # plot: total-version
    plots_total[0,0].set_title('Total issues -- version', size=16)
    plots_total[0,0].plot(pretty_version_list, total_list, '.-', label='total issues')
    # plot: severity High-version
    plots_total[1,0].set_title('Severity issues VS version', size=16)
    plots_total[1,0].plot(pretty_version_list, severity_h_list, '.-', label='high')
    plots_total[1,0].plot(pretty_version_list, severity_m_list, '.-', label='medium')
    plots_total[1,0].plot(pretty_version_list, severity_l_list, '.-', label='low')
    plots_total[1,0].legend()
    # plot: total issues differences between releases
    plots_total[0,1].set_title('Total differences -- version', size=16)
    plots_total[0,1].plot(pretty_version_list, total_diff, '.-', label='total differences')
    plt.setp(plots_total[0,0].xaxis.get_majorticklabels(),rotation=90,horizontalalignment='right')
    plt.setp(plots_total[0,1].xaxis.get_majorticklabels(),rotation=90,horizontalalignment='right')
    plt.setp(plots_total[1,0].xaxis.get_majorticklabels(),rotation=90,horizontalalignment='right')
    plt.show() # this is a blocking call; kill the plotting window to continue execution

    
    ## plotting-2: statistics btw versions
    _, plots_new = plt.subplots(2,2)
    plots_new[0,0].set_title('Lines deleted per release', size=16)
    plots_new[0,0].plot(pretty_version_list, del_change, '.-', label='lines deleted')
    # plot: new lines added per release
    plots_new[0,1].set_title('New lines added per release', size=16)
    plots_new[0,1].plot(pretty_version_list, add_change, '.-', label='new lines added')
    # plot: new lines added per release
    plots_new[1,0].set_title('Net lines changed per release', size=16)
    plots_new[1,0].plot(pretty_version_list, net_lines_changed, '.-', label='new lines added')
    # plot: new lines added per release
    plots_new[1,1].set_title('Files changed per release', size=16)
    plots_new[1,1].plot(pretty_version_list, file_change, '.-', label='files')
    plt.setp(plots_new[0,0].xaxis.get_majorticklabels(),rotation=90,horizontalalignment='right')
    plt.setp(plots_new[0,1].xaxis.get_majorticklabels(),rotation=90,horizontalalignment='right')
    plt.setp(plots_new[1,0].xaxis.get_majorticklabels(),rotation=90,horizontalalignment='right')
    plt.xticks(rotation=90)
    plt.show() # this is a blocking call; kill the plotting window to continue execution


    ## plotting3
    _, plots_result1 = plt.subplots(1,2)
    plots_result1[0].set_title('total issues per number of lines', size=16)
    plots_result1[0].plot(pretty_version_list, total_issues_per_lines, '.-', label='total_issues / #lines') 
    plots_result1[1].set_title('Total issues per java files', size=16)
    plots_result1[1].plot(pretty_version_list, total_issues_per_java, '.-', label='total_issues / #javas') 
    plt.setp(plots_result1[0].xaxis.get_majorticklabels(),rotation=90,horizontalalignment='right')
    plt.setp(plots_result1[1].xaxis.get_majorticklabels(),rotation=90,horizontalalignment='right')
    plt.show() # this is a blocking call; kill the plotting window to continue execution


    ## plotting4
    _, plots_result1 = plt.subplots(1,2)
    plots_result1[0].set_title('Differential of issues/1000net_line_changed', size=16)
    plots_result1[0].plot(pretty_version_list, issue_differential_per_tag*1000, '.-', label='differential of issues/net_line_changed') 
    plots_result1[1].set_title('New issues/1000lines added', size=16)
    plots_result1[1].plot(pretty_version_list, new_issues_per_new_lines*1000, '.-', label='New issues/lines added') 
    plt.setp(plots_result1[0].xaxis.get_majorticklabels(),rotation=90,horizontalalignment='right')
    plt.setp(plots_result1[1].xaxis.get_majorticklabels(),rotation=90,horizontalalignment='right')
    plt.show() # this is a blocking call; kill the plotting window to continue execution

    ## plotting5
    _, plots_result2 = plt.subplots(1,2)
    plots_result2[0].set_title('New issues/files added', size=16)
    plots_result2[0].plot(pretty_version_list, issue_diff_per_file_changed, '.-', label='differential of issues/net_line_changed') 
    plt.setp(plots_result2[0].xaxis.get_majorticklabels(),rotation=90,horizontalalignment='right')
    plt.setp(plots_result2[1].xaxis.get_majorticklabels(),rotation=90,horizontalalignment='right')
    plt.show() # this is a blocking call; kill the plotting window to continue executio


#### ===================== HARD CODE HELPERS ===================== ####
# used specifically for leshan due to branching releases pipeline
def leshan_rearrange(ver_list):
    swap(ver_list, 35, 36)  # 35 at 2.0.0-M1
    swap(ver_list, 36, 38)
    swap(ver_list, 37, 38)
    e = ver_list.pop(42)
    ver_list.insert(37, e)

# swap two elements
def swap(array, low, high):
    e1 = array.pop(high)
    e2 = array.pop(low)
    array.insert(low, e1)
    array.insert(high, e2)
    return


if __name__ == '__main__': 
    print("\n================== PVS Analysis Result ==================")
    
    # Run git diff to get version list and changed lines information
    version_list, changed_lst, file_change, add_change, del_change = cal_changed_lines("./leshan")
    
    num_of_files, num_of_lines = [], []   # number of files and lines per tag
    ## Count java_files in each of the version
    for v in version_list:
        files, lines = c_projectStatistics.count_files_and_lines_no_filter(v, "./leshan")
        num_of_files.append(files)
        num_of_lines.append(lines)

    # print(num_of_lines)

    # ## then plot
    pvs_plot_comparison(version_list, "pvs_leshan/", changed_lst, file_change=file_change, add_change=add_change, 
        del_change=del_change, num_of_files=num_of_files, num_of_lines=num_of_lines)      ## the scaling is not very

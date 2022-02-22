# author: Zichen

# -------------------------------- import area --------------------------------
from ctypes.wintypes import HACCEL
import os
import subprocess
import re
import json
import matplotlib.pyplot as plt
import numpy as np


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
def pvs_num_of_issues_per_type(tag, path_to_project):
    with open(path_to_project + tag + ".txt") as f:
        lines = f.read().splitlines()         # read in the lines without the newline char  
    # my severity count table    
    severity_table = {
          "High": 0,
          "Medium": 0,
          "Low": 0
    }
    # my code count table
    code_table = {}
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
        if code in code_table:
            code_table[code] += issue_count
        else: 
            code_table[code] = issue_count
    print(f"Total Issues Found: {total_issues}")
    print(f"================================")
    print(f"Severity Report: ")
    print(f"  High has: {severity_table['High']}")
    print(f"  Medium has: {severity_table['Medium']}")
    print(f"  Low has: {severity_table['Low']}")
    print(f"================================")
    print(f"Issue Type Found: ")
    print(code_table)
    print("======= done =======")
    return total_issues, severity_table, code_table


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
    str = subprocess.check_output(['git', 'tag'], cwd=path_to_project)
    tag_lst = str.decode("utf-8").split("\n")[:-1]         ## decode the bytes into string and drop last term
    
    changed_lst = ['null']                                 ## have a null at the first tag since it has no version to compare with
    for i in range(len(tag_lst) - 1):
        str = subprocess.check_output(['git', 'diff', '--shortstat', tag_lst[i], tag_lst[i+1]], cwd=path_to_project)
        changed_lst.append(str.decode('utf8').split("\n")[0])

    ## then parse the changed lst:
    file_change = ['null']          ## change of files
    add_change = ['null']           ## addition of lines
    del_change = ['null']           ## deletion of lines
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
def pvs_plot_comparison(version_list, path_to_project, changed_lst=None, file_change=None, add_change=None, del_change=None):
    ## first create empty statistics lists
    total_list = []
    severity_h_list = []
    severity_m_list = []
    severity_l_list = []
    code_list = []

    ## count issues per version
    for v in version_list:
        total, severity, code = pvs_num_of_issues_per_type(v, path_to_project)
        total_list.append(total)
        print(f"type of severity value: {type(severity['High'])}")
        severity_h_list.append(severity['High'])
        severity_m_list.append(severity['Medium'])
        severity_l_list.append(severity['Low'])
        code_list.append(code)
    

    newIssues_per_tag = np.array(total_list) / np.array(add_change)
    print(newIssues_per_tag)

    ## plotting
    _, plots = plt.subplots(2, 2)
    # plot: total-version
    plots[0,0].set_title('Total issues -- version', size=8)
    plots[0,0].plot(version_list, total_list, '.-', label='total issues')
    
    # plot: severity High-version
    plots[0,1].set_title('Severity issues VS version', size=8)
    plots[0,1].plot(version_list, severity_h_list, '.-', label='high')
    plots[0,1].plot(version_list, severity_m_list, '.-', label='medium')
    plots[0,1].plot(version_list, severity_l_list, '.-', label='low')
    plots[0,1].legend()

    # plots[1,1].set_title('Issue Code', size=8)
    # plots[1,1].imshow( BlurImage(A, image), cmap, vmin=0, vmax=1)

    # plots[1,0].set_title('deblurred image - computed', size=8)
    # plots[1,0].imshow( DeblurImage(A, blurred_image), cmap, vmin=0, vmax=1)
    plt.show() # this is a blocking call; kill the plotting window to continue execution



if __name__ == '__main__': 
    ## ======================== please keep these for now ========================
    # version_list = ['leshan-1.0.1', 'leshan-1.0.2', 'leshan-1.1.0', 'leshan-1.2.0', 'leshan-1.3.0', 'leshan-1.3.1', 
    # 'leshan-1.3.2']

    # version_list = ['leshan-2.0.0-M1', 'leshan-2.0.0-M2', 'leshan-2.0.0-M3', 'leshan-2.0.0-M4', 'leshan-2.0.0-M5', 
    #     'leshan-2.0.0-M5', 'leshan-2.0.0-M6']

    # version_list = ['leshan1.0.0_M7', 'leshan1.0.0_M8', 'leshan1.0.0_M9', 'leshan1.0.0_RC1', 'leshan1.0.0_RC2', 
    #     'leshan-1.0.1', 'leshan-1.0.2', 'leshan-1.1.0', 'leshan-1.2.0', 'leshan-1.3.0', 'leshan-1.3.1', 'leshan-1.3.2']
    ## ===========================================================================



    # version_list = ['2.1.0', '2.1.1', '2.1.2', '2.1.3', '2.2.0', '2.2.1', '2.2.2', '2.3.0', '2.3.1',
    #     '2.3.2']

    print("\n================== PVS Analysis Result ==================")

    version_list, changed_lst, file_change, add_change, del_change = cal_changed_lines("./leshan")
 
    pvs_plot_comparison(version_list, "pvs_infer/", changed_lst, add_change=add_change, del_change=del_change)

    print("test")

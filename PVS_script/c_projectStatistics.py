import subprocess


def count_files_and_lines_filtered(version, path_to_project):
    # assume pwd is the root of the project, return no. of files and Lines of Code (LOC)
    # only count java codes and exclude test files
    subprocess.run(["git", "reset", "--hard"], cwd=path_to_project)
    subprocess.run(["git", "checkout", "tags/"+version], cwd=path_to_project)
    file_list = subprocess.run(["git", "ls-files"], check=True, stdout=subprocess.PIPE,text=True, cwd=path_to_project).stdout.strip("\n")\
        .split("\n")
    java_file_list = []
    for each in file_list:
        if ("test" not in each) and (".java" in each):
            java_file_list.append(each)
    cyan = "\33[34m"
    file_count = len(java_file_list)
    print(f"At version: {version}")
    print("total no. of files: " + str(len(file_list)))
    print(cyan + "total java files: " + str(file_count) + "\33[0m")
    line_count = 0
    for each in java_file_list:
        f = open("leshan/"+each, encoding="utf8")
        line_count += len(f.readlines())
        f.close()
    print(cyan + "total java lines: " + str(line_count) + "\33[0m")
    return file_count, line_count


def count_files_and_lines_no_filter(version, path_to_project):
    '''
    Function that returns the number of lines and files without filtering out test files

    Return: file_count, line_count
    ''' 
    # assume pwd is the root of the project, return no. of files and Lines of Code (LOC)
    # only count java codes and exclude test files
    subprocess.run(["git", "reset", "--hard"], cwd=path_to_project)
    subprocess.run(["git", "checkout", "tags/"+version], cwd=path_to_project)
    file_list = subprocess.run(["git", "ls-files"], check=True, stdout=subprocess.PIPE,text=True, cwd=path_to_project).stdout.strip("\n")\
        .split("\n")
    java_file_list = []
    for each in file_list:
        if ".java" in each:
            java_file_list.append(each)
    cyan = "\33[34m"
    file_count = len(java_file_list)
    print(f"At version: {version}")
    print("total no. of files: " + str(len(file_list)))
    print(cyan + "total java files: " + str(file_count) + "\33[0m")
    line_count = 0
    for each in java_file_list:
        f = open("leshan/"+each, encoding="utf8")
        line_count += len(f.readlines())
        f.close()
    print(cyan + "total java lines: " + str(line_count) + "\33[0m")
    return file_count, line_count
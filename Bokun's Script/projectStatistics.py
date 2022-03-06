import subprocess


def count_files_and_lines():
    # assume pwd is the root of the project, return no. of files and Lines of Code (LOC)
    # only count java codes and exclude test files
    file_list = subprocess.run(["git", "ls-files"], check=True, stdout=subprocess.PIPE,text=True).stdout.strip("\n")\
        .split("\n")
    filtered_file_list = []
    for each in file_list:
        if ("test" not in each) and (".java" in each):
            filtered_file_list.append(each)
    cyan = "\33[34m"
    file_count = len(filtered_file_list)
    print("total no. of files: " + str(len(file_list)))
    print(cyan + "total non-test java files: " + str(file_count) + "\33[0m")
    line_count = 0
    for each in filtered_file_list:
        f = open(each)
        line_count += len(f.readlines())
        f.close()
    print(cyan + "total non-test java lines: " + str(line_count) + "\33[0m")
    return file_count, line_count

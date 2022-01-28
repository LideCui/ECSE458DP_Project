import os
import re
from InferSnyk import init


def infer_report_compare(old_version, new_version):
    result = [0, 0, 0]  # [old, new, both]
    with open(old_version+".json") as old, open(new_version+".json") as new:
        old = old.readline()
        new = new.readline()
        old_list = re.findall("(\"hash\":\"\\w*\")", old)
        new_list = re.findall("(\"hash\":\"\\w*\")", new)
        print(old_version + " has " + str(len(old_list)) + " issues")
        print(new_version + " has " + str(len(new_list)) + " issues")

        # obtain set properties
        both = []
        itr = old_list.copy()
        for item in itr:
            if item in new_list:
                new_list.remove(item)
                old_list.remove(item)
                both.append(item)

        print("fixed" + "(" + str(len(old_list)) + ")" + ": " + str(old_list))
        print("introduced" + "(" + str(len(new_list)) + ")" + ": " + str(new_list))
        print("pre-existing" + "(" + str(len(both)) + ")" + ": " + str(both))

        result[0] = len(old_list)
        result[1] = len(new_list)
        result[2] = len(both)
    return result


def snyk_report_compare(old_version, new_version):
    result = [0, 0, 0]  # [old, new, both]
    with open(old_version + ".json") as old, open(new_version + ".json") as new:
        old = old.read()
        new = new.read()
        old_list = re.findall("(\"1\": \"[.-z]*\")", old)
        new_list = re.findall("(\"1\": \"[.-z]*\")", new)
        print(old_version + " has " + str(len(old_list)) + " issues")
        print(new_version + " has " + str(len(new_list)) + " issues")

        # obtain set properties
        both = []
        itr = old_list.copy()
        for item in itr:
            if item in new_list:
                new_list.remove(item)
                old_list.remove(item)
                both.append(item)

        print("fixed" + "(" + str(len(old_list)) + ")" + ": " + str(old_list))
        print("introduced" + "(" + str(len(new_list)) + ")" + ": " + str(new_list))
        print("pre-existing" + "(" + str(len(both)) + ")" + ": " + str(both))

        result[0] = len(old_list)
        result[1] = len(new_list)
        result[2] = len(both)
    return result


if __name__ == '__main__':
    version_list = init()
    # after running init(), cwd is /Users/bokunzhao/Downloads/leshan
    os.chdir("../LeShanReports/Infer/")
    print("analyzed versions:")
    version_list = version_list[26:36]
    print(version_list)
    print("\n==================INFER==================\n")
    # result = infer_report_compare(version_list[0], version_list[1])
    for i in range(0, len(version_list)-1):
        print(infer_report_compare(version_list[i], version_list[i+1]))
        print("\n")
    os.chdir("../Snyk/")
    print("\n==================SNYK==================\n")
    for i in range(0, len(version_list) - 1):
        print(snyk_report_compare(version_list[i], version_list[i+1]))

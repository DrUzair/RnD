#@Author Uzair Ahmad
# Data Science Lab, Ryerson University
# 10-02-2017
import urllib2
import os
import backoff
# 733687 files related to 210296 commits

url_prefix_raw = 'https://hg.mozilla.org/mozilla-central/raw-file/'
url_prefix_rawdiff = 'https://hg.mozilla.org/mozilla-central/raw-diff/'
url_prefix_rawrev = 'https://hg.mozilla.org/mozilla-central/raw-rev/'
rawdata_dir = 'C:\\R&D\\Mozilla\\RawData\\'
churn_dir = 'C:\\R&D\\Mozilla\\'

def main():
    file_name = 'C:\\R&D\\Mozilla\\data_for_complexity.csv'
    start = 3061
    end = 10000
    process_commit_ids(start, end)

# @backoff.on_exception(backoff.expo,
#                           urllib2.URLError,
#                           max_value=6)
# def url_open(url):
#     return urllib2.urlopen(url)



def find_commit_line(file_name):
    lines = file_len(file_name)
    f_data_for_complexity = open(file_name, 'r')
    f_data_for_complexity_lines = f_data_for_complexity.readlines()
    for i in range(134064, 150000):
        line = f_data_for_complexity_lines[i].strip()
        commit_id = findnth(line, ',', 0)
        if (commit_id == '87cb1807aab9'):
            print i

def findnth(line, tobefound, n):
    parts = line.split(tobefound, n + 1)
    if len(parts) <= n + 1:
        return -1
    return parts[n]


def file_len(file_name):
    with open(file_name) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

class ChurnMeasurements:
    loc_raw_file = 0
    locmnt_raw_file = 0
    bug_id = None
    difflineminus_count = 0
    difflineplus_count = 0
    diffcommentsminus_count = 0
    diffcommentsplus_count = 0
    hunk_count = 0
    difflinenumber_list = []
    dev_email = None
    dev_name = None
    file_name = None
    file_type = None
    method_names = []
    date = None
    rawdiff_file_name = None

def init_churn_obj():
    churn_obj = ChurnMeasurements()
    churn_obj.difflinenumber_list = []
    churn_obj.method_names = []
    churn_obj.bug_id = None
    churn_obj.loc_raw_file = 0
    churn_obj.locmnt_raw_file = 0
    churn_obj.dev_name = None
    churn_obj.dev_email = None
    churn_obj.date = None
    churn_obj.difflineminus_count = 0
    churn_obj.difflineplus_count = 0
    churn_obj.diffcommentsminus_count = 0
    churn_obj.diffcommentsplus_count = 0
    churn_obj.file_name = None
    churn_obj.file_type = None
    churn_obj.rawdiff_file_name = None
    return churn_obj

def is_last_comment_line(line):
    if (line.startswith("*/") or line.endswith("'''") or line.endswith("-->")):
        return True
    else:
        return False

def is_comment_line(line, prev_line_was_comment, file_type):
    line = line.strip()

    if (file_type.lower() == 'c' or file_type.lower() == 'cpp' or file_type.lower() == 'java'):
        if( line.startswith("//") or line.startswith("/*")  or line.startswith("*/")):
            return True
        elif (prev_line_was_comment & line.startswith("*")):
            return True
        else:
            return False
    if (file_type.lower() == 'xml'):
        if (line.startswith('<!--')):
            return True
        elif (prev_line_was_comment or line.endswith('-->')):
            return True
        else:
            return False
    if (file_type.lower() == 'py'):
        if (line.startswith("'''") or line.startswith('#')):
            return True
        elif (prev_line_was_comment or line.endswith("'''")):
            return True
        else:
            return False

def compressList(csv_list):
    s = e = None
    for item in csv_list:
        if(s is None):
            s = e = item
        elif (item == e or item == e + 1):
            e = item
        else:
            yield (s, e)
            s = e = item
    if s is not None:
        yield (s, e)

def read_raw_file_from_mercurial(commit_id, commit_record_file_name, file_type, the_url_raw_file):
    # to be called from read_diff_from_mercurial
    # saves raw-file on local disk and
    # counts + returns loc and locomment
    raw_file_dir = rawdata_dir + 'raw\\' + commit_id

    if not os.path.exists(raw_file_dir):
        os.makedirs(raw_file_dir)
    f_raw_file = open(raw_file_dir + '\\'+commit_record_file_name.replace('/', '-') + '.raw', 'w')  # overwriting existing file
    lines_of_code = 0
    lines_of_comment = 0
    # the_url_raw_file --> Example -->
    try:
        prev_line_was_comment = False
        for line in urllib2.urlopen(the_url_raw_file):
            f_raw_file.write(line)
            if (len(line.strip()) > 1):
                if (is_comment_line(line, prev_line_was_comment, file_type) == True):
                    lines_of_comment = lines_of_comment + 1
                    if (is_last_comment_line(line) == False):
                        prev_line_was_comment = True
                    else:
                        prev_line_was_comment = False
                else:
                    lines_of_code = lines_of_code + 1
    except urllib2.HTTPError:
        print 'Invalid Raw-File URL or something --> ' + the_url_raw_file

    f_raw_file.close()
    return (lines_of_code, lines_of_comment)



def read_diff_from_mercurial(commit_id, the_url_diff_file):
    churn_obj_list = []# a list of churn objects to be returned by this function, one object per file in the commit/patch/changeset
    #link = 'https://hg.mozilla.org/mozilla-central/raw-rev/e4e55af56102/'
    print the_url_diff_file
    difflineminus_count = 0
    difflineplus_count = 0
    diffcommentsplus_count = 0
    diffcommentsminus_count = 0
    hunk_count = 0
    linenumber = 0
    hunkForOldFileStartsAtLineNumber = 0
    hunkForNewFileStartsAtLineNumber = 0
    removedLinesInThisHunk = 0  # To compensate removed lines
    addedLinesInThisHunk = 0  # To compensate added lines before removing
    hunk_started = False

    f_rawdiff_file = open(rawdata_dir + "\\raw-diffs\\" + commit_id + '.rawdiff', 'w') # overwriting existing file

    file_type_ok = True
    dev_email = ""
    dev_name = ""
    commit_date = ""
    prev_line_was_comment = False
    #is_first_diff = True

    try:
        for line in urllib2.urlopen(the_url_diff_file):
            f_rawdiff_file.write(line)
            line = line.strip()
            if (line.find("# User ") != -1):
                dev_name = line[line.find("# User ") + 7:line.find("<")].strip()
                dev_email = line[line.find("<"):len(line)].strip()

                continue  # to the next line
            if (line.find("# Date ") != -1):
                commit_date = line[line.find("# Date ") + 7:len(line)].strip()

                continue  # to the next line

            if (line.find("---") != -1):  # Start of new file changed in this commit - Get file name
                continue  # Continue to next line

            if (line.find("+++") != -1):  # Start of new hunk- Get file name
                continue  # to the next line

            if(line.startswith('diff --git a/')):
                # Start of new file in this commit/patch/changeset
                # init hunk_count, difflineplus_count, difflineminus_count, diffcommentsminus_count
                difflineminus_count = 0
                difflineplus_count = 0
                diffcommentsplus_count = 0
                diffcommentsminus_count = 0
                hunk_count = 0
                # Determine file name and type
                file_name = line[line.find('diff --git a/')+13:line.find(' b/')]
                file_type = None
                if (file_name.rfind('.') != -1):
                    file_type = file_name[file_name.rfind('.')+1:]
                else:  # if the file name has no extension
                    file_type = file_name[file_name.rfind('/'):]

                if (file_type.lower() != "h" and file_type.lower() != 'cpp' and file_type.lower() != "js" and file_type.lower() != "html" and file_type.lower() != "in" and
                                        file_type.lower() != "c" and file_type.lower() != "build" and file_type.lower() != "java" and file_type.lower() != "py" and file_type.lower() != "php" and
                                        file_type.lower() != "cc" and file_type.lower() != "idl"  and file_type.lower() != "jsm" and  file_type.lower() != "ini" and file_type.lower() != "css" and
                                        file_type.lower() != "xml" and file_type.lower() != "py" and file_type.lower() != "xul" and file_type.lower() != "list" and file_type.lower() != "xhtml" and
                                        file_type.lower() != "mk" and file_type.lower() != "xslt" and file_type.lower() != "mm" and file_type.lower() != "mn" and file_type.lower() != "ipdl" and
                                        file_type.lower() != "json" and file_type.lower() != "dtd" and file_type.lower() != "sh" and file_type.lower() != "ps" and
                                        file_type.lower() != "bash" and file_type.lower() != "shell" and file_type.lower() != "rpc" and file_type.lower() != "nmake" and file_type.lower() != "xsd"
                    ):
                    file_type_ok = False
                    continue # continue to the next file
                else:
                    file_type_ok = True
                the_url_raw_file = url_prefix_raw + commit_id + '/' + file_name
                print the_url_raw_file
                (loc, locmnt) = read_raw_file_from_mercurial(commit_id, file_name, file_type, the_url_raw_file)

                churn_obj = init_churn_obj()

                churn_obj.rawdiff_file_name = file_name
                churn_obj.loc_raw_file = loc
                churn_obj.locmnt_raw_file = locmnt
                churn_obj.dev_name = dev_name
                churn_obj.dev_email = dev_email
                churn_obj.date = commit_date
                churn_obj.file_type = file_type
                churn_obj_list.append(churn_obj)

                continue # to the next line
            if(file_type_ok):
                if(line.startswith("@@")): # Start of new hunk
                    # Example: @@ -1026,17 +1022,23 @@ CanAttachDenseElementHole(JSObject* obj)
                    # The -1026 means line 1026 in old version
                    # 17 means the length(number of lines) of the hunk with respect to old file
                    # Find the index of first -
                    line = line[line.find('-')+1: len(line)]
                    # e.g. 1026,17 +1022,23 @@ CanAttachDenseElementHole(JSObject* obj)
                    # Find the hunkStartsAtLineNumber from 0 to the position of first comma
                    # hunkForOldFileStartsAtLineNumber is the first line of the hunk,
                    hunkForOldFileStartsAtLineNumber = int(line[0:line.find(',')].strip()) - 1

                    # Now find the index of first +
                    line = line[line.find('+') + 1: len(line)]
                    # e.g. +1022,23 @@ CanAttachDenseElementHole(JSObject* obj)
                    # Find the hunkStartsAtLineNumber from 0 to the position of first comma
                    # hunkStartsAtLineNumber is the first line of the hunk,
                    hunkForNewFileStartsAtLineNumber = int(line[0:line.find(',')].strip()) - 1
                    removedLinesInThisHunk = 0 # To compensate removed lines
                    addedLinesInThisHunk = 0 # To compensate added lines before removing
                    method_name = line[line.find('@@') + 2: len(line)].strip()
                    churn_obj.method_names.append(str(method_name).replace(',',' '))
                    hunk_started = True
                    linenumber = 0 # init linenumber to 0
                    hunk_count = hunk_count + 1
                    churn_obj.hunk_count = hunk_count
                    continue  # Continue to next line
                if (hunk_started):
                    linenumber = linenumber + 1 # linenumber will be incremented every line after the hunk (@@) started
                    if (line.startswith("-")):
                        line = line[1:len(line)].strip() # remove the minus sign
                        removedLinesInThisHunk = removedLinesInThisHunk + 1
                        # To ignore the comment line make sure it doesn't start with // or #
                        # To ignore the empty line make sure its length is more than 1
                        if (is_comment_line(line, prev_line_was_comment, file_type)):
                            diffcommentsminus_count = diffcommentsminus_count + 1
                            churn_obj.diffcommentsminus_count = diffcommentsminus_count
                            if(is_last_comment_line(line) == False):
                                prev_line_was_comment = True
                            else:
                                prev_line_was_comment = False
                            continue  # to the next line
                        difflineminus_count = difflineminus_count + 1
                        churn_obj.difflineminus_count = difflineminus_count
                        # removed code line number will be represented as a negative number
                        churn_obj.difflinenumber_list.append(-1*(hunkForOldFileStartsAtLineNumber + linenumber - addedLinesInThisHunk))
                        continue  # Continue to next line
                    if (line.startswith("+")):
                        line = line[1:len(line)].strip() # remove the plus sign
                        addedLinesInThisHunk = addedLinesInThisHunk + 1
                        # To ignore the comment line make sure it doesn't start with // or #
                        if (is_comment_line(line, prev_line_was_comment, file_type)):
                            diffcommentsplus_count = diffcommentsplus_count + 1
                            churn_obj.diffcommentsplus_count = diffcommentsplus_count
                            if (is_last_comment_line(line) == False):
                                prev_line_was_comment = True
                            else:
                                prev_line_was_comment = False
                            continue  # to the next line
                        difflineplus_count = difflineplus_count + 1
                        churn_obj.difflineplus_count = difflineplus_count
                        churn_obj.difflinenumber_list.append((hunkForNewFileStartsAtLineNumber + linenumber - removedLinesInThisHunk))
    except urllib2.HTTPError:
        print 'Invalid Raw-File URL or something --> ' + the_url_diff_file

    f_rawdiff_file.close()
    return (churn_obj_list)

def process_commit_ids(start, end):
    # url_prefix is taken from mercurial
    commit_id_len = 12
    f_commit_ids = open('C:\\R&D\\Mozilla\\commit_ids_mar2017.txt', 'r')
    f_commit_ids_lines = f_commit_ids.readlines()
    for i in range(start, end): #
        print "commit # " + str(i)
        commit_id = f_commit_ids_lines[i].split('\t')[0].strip()
        bug_id = f_commit_ids_lines[i].split('\t')[1].strip()

        # length of commit id is 12 chars as in --> f897399fb28a

        try:
            the_url_of_diff = url_prefix_rawrev + commit_id
            churn_obj_list = read_diff_from_mercurial(commit_id, the_url_of_diff)
        except urllib2.HTTPError:
            print 'Invalid URL or something'
        method_names = ""
        for churn_obj in churn_obj_list:
            for index, method_name in enumerate(churn_obj.method_names):
                method_names = str(method_name) + '<>' + method_names

            csv_list = []
            for index, diff_line_num in enumerate(churn_obj.difflinenumber_list):
                csv_list.append(diff_line_num)
            diff_line_numbers = ""
            csv_list = sorted(csv_list)
            for (s, e) in compressList(csv_list):
                if s == e:
                    x = '%d' % s
                else:
                    x = '%d~%d' % (s, e)
                diff_line_numbers = diff_line_numbers + ',' + x
            diff_line_numbers = diff_line_numbers[1:len(diff_line_numbers)] #Strip first comma
            f_churn_data = None
            if (not os.path.isfile(churn_dir + 'Churn_Data_'+str(start)+'-'+str(end)+'.tdl')):
                f_churn_data = open(churn_dir + 'Churn_Data_' + str(start) + '-' + str(end) + '.tdl', 'a')
                f_churn_data.write("index" + '\t' +
                           "bug_id" + '\t' +
                           "commit_id" + '\t' +
                           "rawdiff_file_name" + '\t' +
                           "loc_raw_file" + '\t' +
                           "locmnt_raw_file" + '\t' +
                           "date" + '\t' +
                           "dev_name" + '\t' +
                           "dev_email" + '\t' +
                           "file_type" + '\t' +
                           "hunk_count" + '\t' +
                           "difflineminus_count" + '\t' +
                           "difflineplus_count" + '\t' +
                           "diffcommentsminus_count" + '\t' +
                           "diffcommentsplus_count" + '\t' +
                           "diff_line_numbers" + '\t' +
                           "method_names" + '\n')
            else:
                f_churn_data = f_churn_data = open(churn_dir + 'Churn_Data_' + str(start) + '-' + str(end) + '.tdl', 'a')
            f_churn_data.write(str(i) + '\t' +
                           bug_id + '\t' +
                           commit_id + '\t' +
                           churn_obj.rawdiff_file_name + '\t' +
                           str(churn_obj.loc_raw_file) + '\t' +
                           str(churn_obj.locmnt_raw_file) + '\t' +
                           churn_obj.date + '\t' +
                           churn_obj.dev_name + '\t' +
                           churn_obj.dev_email + '\t' +
                           str(churn_obj.file_type) + '\t' +
                           str(churn_obj.hunk_count) + '\t' +
                           str(churn_obj.difflineminus_count) + '\t' +
                           str(churn_obj.difflineplus_count) + '\t' +
                           str(churn_obj.diffcommentsminus_count) + '\t' +
                           str(churn_obj.diffcommentsplus_count) + '\t' +
                           diff_line_numbers + '\t' +
                           method_names + '\n')
            f_churn_data.close()

    print (str(i) + ' commits ' + 'completed')

    f_commit_ids.close()

if __name__ == "__main__":
    main()

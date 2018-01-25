import sys
import re
import logging
from whatthepatch import parse_patch

class MyGitPatch:
    def __init__(self, text):

        # list of dictionaries containing the following keys:
        # {old={file, date, time}, new={file, date, time}, diff={old_chunk, new_chunk, context}}
        self.hunks = self.load_hunks_from_text(text)

    # obsoleted?
    def get_old_files(self):
        files = set()

        for hunk in self.hunks:
            files.add(hunk.old.file)

        return files


    def get_files_with_chunks(self):
        ret_list = []
        current_file = self.hunks[0].old
        hunks_for_file = []

        for hunk in self.hunks:
            if hunk.old == current_file:
                hunks_for_file.append(hunk.diff)
            else:
                if hunks_for_file:
                    ret_list.append((current_file, hunks_for_file))
                current_file = hunk.old
                hunks_for_file = None
                hunks_for_file.append(hunk.diff)

        if hunks_for_file:
            ret_list.append((current_file, hunks_for_file))

        return ret_list


    # obsoleted?
    def get_chunks_for_old_file(self, old_file):
        return [item.diff for item in self.hunks if item.old.file == old_file]


    def load_hunks_from_text(self, input):
        ret_list = []

        old = None
        new = None
        diff = None

        for line in input:


            line.strip()

            if line.startwith("+++"):
                #new = line.split()[1]
                match = re.match(r"\+\+\+\s+(?P<file>[^\s]+)\s+(?P<date>[^\s]+)\s(?P<time>[^\s]+)", line)
                new = match.groupdict()

            if line.startswith("---"):
                #old = line.split()[1]
                match = re.match(r"\-\-\-\s+(?P<file>[^\s]+)\s+(?P<date>[^\s]+)\s(?P<time>[^\s]+)", line)
                old = match.groupdict()

            if line.startswith("@@") and new and old:
                match = re.match(r"@@\s+\-(?P<old_chunk>[^\s]+)\s+\+(?P<new_chunk>[^\s]+)[@\s]+(?P<context>.*$)", line)
                diff = match.groupdict()

            ret_list.append({'old':old,'new':new,'diff':diff})

        return ret_list



def get_relevant_commits_from_diffs(file_chunks_pair):
    # - extract context file and context from hunk
    # - let git list history for a file extracted from context
    # - in list, search for commits with the same context
    # - to obtain those contexts, run each commit's diff through get_hunks_from
    # - then compare hunk.context with commit.context



    pass


def main():
    patch_file = None
    relevant_commits = None

    if len(sys.argv) > 1:
        patch_file = sys.argv[1]
    else:
        #print_usage()
        logging.info("No argument given")
        return

    with open(patch_file) as f:
        lines = f.readlines
        patch_obj = MyGitPatch(lines)
        if not patch_obj:
            logging.info("No diff found in given source")
            return

    for file_chunks_pair in patch_obj.get_files_with_chunks():
        # magic sh*t to lookup all relevant commits
        relevant_commits.append(get_relevant_commits_from_diffs(file_chunks_pair))

    print(relevant_commits)

if __name__ == "__main__":
    main()
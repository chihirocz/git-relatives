import sys
import re
import logging
from whatthepatch import parse_patch

class myGitPatch:
    def __init__(self, text):

        # list of dictionaries containing the following keys:
        # {old={file, date, time}, new={file, date, time}, diff={old_chunk, new_chunk, context}}
        self.hunks = get_hunks_from(text)


    def get_old_files(self):
        files = set()

        for hunk in hunks::
            files.add(hunk.old.file)
        
        return files


    def get_hunks_from(self, input):

        
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



def get_relevant_commits_from_diff(hunk):
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
        patch_obj = get_hunks_from(lines)
        if not patch_obj:
            logging.info("No diff found in given source")
            return
    
    for hunk in patch_obj:
        # magic sh*t to lookup all relevant commits
        relevant_commits.append(get_relevant_commits_from_diff(hunk))
        pass


if __name__ == "__main__":
    main()
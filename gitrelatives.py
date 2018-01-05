import sys
import re
import logging
from whatthepatch import parse_patch

def get_hunks_from(input):

    # list of dictionaries containing the following keys:
    # {old={file, date, time}, new={file, date, time}, diff={old_chunk, new_chunk, context}}
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
    


def main():
    patch_file = None

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
        pass


if __name__ == "__main__":
    main()
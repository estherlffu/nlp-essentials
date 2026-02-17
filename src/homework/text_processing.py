import re

def chronicles_of_naria(filename):

    filename = 'dat/chronicles_of_narnia.txt'

    books = {} # dict to be returned
    book_track = None # to keep track of current book
    chapter_track = None # to keep track of current chapter

    # Identify books & chapters
    book_identify = re.compile(r'^(.*)\s+\(\s(\d{4})\s\)$') # Before ( 4 digit number )
    chapter_identify = re.compile(r'^CHAPTER\s([IVX]+)$') # Line after CHAPTER _

    # Convert roman numeral to integer
    def chapter_number(rn):
        roman = {'I': 1, 'V': 5, 'X':10} # All books have less than 20 chapters
        output = 0
        previous = 0

        # traverse input from end
        for i in reversed(rn):
            t = roman[i] # use current char (temp)
            if t < previous: # smaller before larger ex. IV = 4
                output -= t
            else: # else ex. VI = 5
                output += t
            previous = t

        return output

    # To isolate lines
    with open(filename, 'r') as f: # read input file
        lines = f.readlines()
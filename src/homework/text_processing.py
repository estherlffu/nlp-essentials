import re

def chronicles_of_narnia(filename):

    books = {} # dict to be returned

    # Identify books & chapters
    book_identify = re.compile(r'^(.*)\s+\(\s(\d{4})\s\)$') # Before ( 4 digit number )
    chapter_identify = re.compile(r'^CHAPTER\s([IVX]+)$', flags=re.IGNORECASE) # Line after CHAPTER/Chapter _ (case insensitive), used ChatGPT & Gemini to find function that ignores case

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

    # Determine whether each line is book title, chapter # or title, or text
    f_out = open(filename, 'r') # read input file

    book_track = None  # to keep track of current book
    chapter_track = None  # to keep track of current chapter
    chapter_tokens = 0

    for line in f_out:

        # For book information
        book_line = book_identify.match(line)
        if book_line: # match() regular expression of book title

            # marks end of chapter, need to save
            if chapter_track: # if not empty, append chapter info to chapters
                book_track['chapters'].append({
                    'number': chapter_track['number'],
                    'title': chapter_track['title'],
                    'token_count': chapter_tokens # stores number of tokens
                })
                chapter_tokens = 0 # reset
                chapter_track = None # reset

            # Save book information to dictionary
            title = book_line.group(1)  # title within first parenthesis
            year = int(book_line.group(2))  # year in second parenthesis, cast to int
            book_track = {'title': title, 'year': year, 'chapters': []}  # chapters is array
            books[title] = book_track

            # Go to next line
            continue

        # For chapter number
        chapter_line = chapter_identify.match(line)
        if chapter_line: # match() re of chapter number

            # marks end of chapter, need to save again
            if chapter_track: # if not empty, append chapter info to chapters
                book_track['chapters'].append({
                    'number': chapter_track['number'],
                    'title': chapter_track['title'],
                    'token_count': chapter_tokens # stores number of tokens
                })
                chapter_tokens = 0 # reset

            chapter_track = {'number': chapter_number(chapter_line.group(1)), 'title': ''}

            # Go to next line
            continue

        # Extract chapter title, next line after chapter number
        if chapter_track and chapter_track['title'] == '':
            chapter_track['title'] = line.strip() # to remove '\n'
            continue

        # Count tokens
        if chapter_track: # if not empty
            chapter_tokens += len(line.split()) # add length of list of words in each line to counter
            continue

    # After for loop, last chapter has yet to be saved
    book_track['chapters'].append({
        'number': chapter_track['number'],
        'title': chapter_track['title'],
        'token_count': chapter_tokens  # stores number of tokens
    })

    f_out.close() # must close output stream

    return books

# Test for Task 1: Chronicles of Narnia
task_1 = chronicles_of_narnia('/Users/esther/Documents/Emory/Classes/2026 Spring/cs329/nlp-essentials/dat/chronicles_of_narnia.txt')
print(task_1)
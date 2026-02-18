import re

# Task 1: Chronicles of Narnia
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
# task_1 = chronicles_of_narnia('/Users/esther/Documents/Emory/Classes/2026 Spring/cs329/nlp-essentials/dat/chronicles_of_narnia.txt')
# print(task_1)

# Task 2: Regular Expressions
def regular_expressions(string):
    # Returns email, date, url, cite, or None

    # Email
    # Must start & end with letter or number (^[])
    # Optional: contains letters, numbers, ., _, - ()?
    # @
    # Must start & end with letter or number (^[])
    # Optional: contains letters, numbers, ., _, - ()?
    # \.
    # Ends with com, org, edu, or gov

    email_identify = re.compile(r'^[A-Za-z0-9]([\w.-]*[A-Za-z0-9])?@[A-Za-z0-9]([\w.-]*[A-Za-z0-9])?\.(com|org|edu|gov)$')

    # Date
    # Format YYYY/MM/DD, YY/MM/DD, YYYY-MM-DD, YY-MM-DD
    # Year: 1951-2050 or 00-99
    # Month: (0)?1-12
    # Day: (0)?1-31 (need to check if day is in month)

    date_identify = re.compile(r'^((19[5-9][0-9]|20[0-4][0-9]|2050)|([5-9][0-9]|[0-4][0-9]|50))' # year
                               r'[/-]((0?[13578]|1[02])[/-](0?[1-9]|[12][0-9]|3[01])|' # mm-dd for months with 31 days
                               r'((0?[469]|11)[/-](0?[1-9]|[12][0-9]|30))|' # mm-dd for months with 30 days max
                               r'(0?2[/-](0?[1-9]|[12][0-9])))$') # mm-dd for February

    # url
    # http or https
    # ://
    # Must start with letter/number
    # Must include at least one dot
    # Optional: contain letters, -, .

    url_identify = re.compile(r'^(https?)://[A-Za-z0-9][A-Za-z.-]*\.[A-Za-z-.]*$')

    # cite
    # Single author Lastname, YYYY (authors with two-word last names or multiple capital letters ex. McGowan)
    # Two authors Lastname and Lastname, YYYY
    # Lastname et al., YYYY

    cite_identify = re.compile(r'^[A-Z][a-zA-Z]*([A-Z][a-zA-Z]*)*( and [A-Z][a-zA-Z]*([A-Z][a-zA-Z]*)*)?( et al\.)?, (19[0-9][0-9]|20[01][0-9]|202[0-4])$')

    if email_identify.match(string):
        return 'email'
    elif date_identify.match(string):
        return 'date'
    elif url_identify.match(string):
        return 'url'
    elif cite_identify.match(string):
        return 'cite'
    else:
        return None

# Test for Task 2: Regular Expressions
# test = ['esther.fu@emory.edu', 'email@domain.abc', 'username@hostname.gov', '1958/1/2', '2024-2-31', 'https://testweb.com', 'Smith, 2023', 'Smith and Jones, 2023', 'Smith et al., 2023']
# for t in test:
    # print(regular_expressions(t))
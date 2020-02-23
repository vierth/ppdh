'''
This script will break apart the annotated catolog and create a csv file
'''

import re

'''
The average page starts with a pattern that indicates the four treasuries
classification, which looks like this:

卷二 經部二

In this example we want to extract the 經 character
'''
# regex that matches siku category
siku_regex = re.compile(r'''
    卷 # matches scroll (juan)
    [一二三四五六七八九十百千]+ # match numbers
    \s? # optionally match a whitespace
    ([經史子集]) # match category data
    部 # match category "bu"
    [一二三四五六七八九十百千]+ # numbers
    ''', re.X)

'''
The subcategory information tends to follow one of two patterns:

==春秋類二==
or
○孝經類

'''

subcat_regex = re.compile(r'''
    ^ # the pattern will appear at the beginning of a line
    (?: # this will indicate that the group should not return anything
    == # matches ==
    (.+) # match the category value
    類 # matches the character for category (lei)
    [一二三四五六七八九十百千]+ # numbers
    == # matches ==
    )
    | # or match this pattern
    (?:
    ○ # match the circle
    (.+)
    類
    )
    ''', re.X|re.M)

'''
Now let's write a regex that matches information on books:

==《[[東坡易傳]]》•九卷{{*|副都御史黃登賢家藏本}}==

宋蘇軾撰。是書一名《毗陵易傳》。陸遊《老學庵筆記》謂其書初遭元祐黨禁，不敢顯題軾名...

This format is essentially this:
==《[[Title]]》•Length卷{{*|Edition}}==

Book Information
'''

book_regex = re.compile(r'''
    ^ # beginning of a line
    (?:
    == # match ==
    | # or
    △ # match △
    ) 
    《 # open quotation mark
    (.+) # title information
    》 # close quotation mark
    [•\s]? # match circle or a space (optionally)
    (?: # start non-capture group
    ([一二三四五六七八九十百千]+) # numbers
    卷 # scroll
    )? # close it, but match optionally

    (?: # start non-capture group
    \{\{ # matches {{
    \* # match *
    \| # match |
    (.+?) # match contents (non-greedy) and capture
    \}\} # match }}
    )? # close the group and make it optional

    ={2}? # optionally match ==

    (?: # non-capture group
    \n # match a new line
    (.+?)
    )? # close the group make optional

    \n{2} # match two new lines to get to book info
    (.+) # collect the book info
    ''', re.X | re.M)

'''
The bibliographic description often contains info on people involved in the
production of the book. It usually looks like this:
DynastyPersonRole
'''

person_regex = re.compile(r'''
    ^ # beginning of line
    (.+?) # get the info
    ([撰編纂選輯注述]) # get the role
    ''', re.X|re.M)

# load in the text
with open('四庫全書總目提要.txt', 'r', encoding='utf8') as rf:
    text = rf.read()

# divide the text into pages
pages = text.split("~~~NEXT~~~")[1:-5]

# current value for the siku category
current_siku = '經'

# current value for the subcategory
current_subcat = '易'

# variable to hold results
results = []

# iterate through each page
for page in pages:
    # use the siku regex to search for the patern
    siku_info = siku_regex.search(page)

    if siku_info:
        current_siku = siku_info.group(1)

    # use the subcategory to search for the pattern
    subcat_info = subcat_regex.search(page)

    if subcat_info:
        if subcat_info.group(1):
            current_subcat = subcat_info.group(1)
        else:
            current_subcat = subcat_info.group(2)

    # get book info on each page
    info_on_books = book_regex.finditer(page)

    # iterate through each result
    for book_info in info_on_books:
        # if there is a result, then get it
        if book_info:
            title = book_info.group(1).replace('[', '').replace(']', '')
            length = book_info.group(2)
            supplemental = str(book_info.group(3)) + str(book_info.group(4))
            supplemental = supplemental.replace('None', '')
            book_description = book_info.group(5)

            # get personal info
            person_info = person_regex.search(book_description)

            # if person exists save the info
            if person_info:
                person = person_info.group(1)
                role = person_info.group(2)
            else:
                person = ''
                role = ''

            # list of information on the current book
            information = [title, current_siku, current_subcat, length, 
                person, role, supplemental, book_description]

            information = ",".join([str(i) for i in information])
            results.append(information)

with open('output.csv', 'w', encoding='utf8') as wf:
    wf.write("Title,Siku,SubCat,Length,Person,Role,Supp,Desc\n")
    wf.write("\n".join(results))








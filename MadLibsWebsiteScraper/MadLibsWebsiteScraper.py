import requests
import re
from bs4 import BeautifulSoup


def remove_non_ascii(s):
    return "".join(c for c in s if ord(c) < 128)


story_count = 188

story_lib = []

for story_number in range(1, story_count + 1):
    URL = "https://www.madtakes.com/printglib.php?glibid=" + str(story_number)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    story_title = soup.title.string
    # print("Title: " + story_title)  # test

    tr_list = soup.find_all("tr")

    td_list = tr_list[4].find_all("td", attrs={"align": "right"})  # 5th element (index = 4) has stuff for entering
    # words (parts of speech). In addition, the td tags I'm searching for seem to have right-hand-side alignment

    words_pos = []  # list of parts of speech descriptions

    # print("Words POS:")  # test
    for td in td_list:
        words_pos.append(td.text)
        # print(td.text)  #test

    story = tr_list[-2].text  # extracting the story from html

    story = remove_non_ascii(story)  # remove non-ascii characters (they end up as gibberish)

    punctuation_marks = [" .", " ,", " !", " ?", " :", " ;", " )", "( "]  # most common punctuation marks with extra
    # whitespaces that might have appeared after the previous operation

    for mark in punctuation_marks:
        no_space_mark = mark.replace(' ', '')
        story = story.replace(mark, no_space_mark)

    # taking into account br tags. Check each letter for isupper() and for preceding it non-whitespace character
    story = list(story)
    # print(story)
    for i in range(len(story)):
        if story[i].isupper() or story[i] == "[":
            if i != 0 and story[i - 1] != " ":
                story[i] = " " + story[i]
    story = "".join(story)
    # print(story)  # test

    story = " ".join(story.split())  # removing repeating whitespaces

    # print("Story: " + story)  # test

    '''
    # example output for story #2
    story_title = "Hail to the Chief!"
    words_pos = ["PLACE [1]", "NOUN (PLURAL) [6]", "AMOUNT OF TIME [2]", "NOUN (PLURAL)  [7]", "ADJECTIVE [3]", "VERB [8]",
                 "NOUN [4]", "VERB [9]", "NOUN [5]", "OCCUPATION [10]"]
    story = "The president of the [1] is elected every [2] by a group of people called the [3] College. Each [4] casts " \
            "votes in a preliminary hearing called a [5]. Throughout the campaign, the candidates participate in [6] and " \
            "[7]. Many people try to [8] the outcome using polls and statistics. In the end, only one person is selected " \
            "to [9] the country as [10] in Chief. "
    '''

    # ordering elements by their number
    ordered_words_pos = []
    for i in range(len(words_pos)):
        number = "[" + str(i + 1) + "]"
        for word_pos in words_pos:
            if number in word_pos:
                ordered_words_pos.append(word_pos)

    # sorting elements into dictionary
    words_pos_dict = {}
    for word_pos in ordered_words_pos:
        key_no = "[" + word_pos.split(" [")[1]  # separating each entry into pos and the number, then assigning the
        # number into key_no variable

        pos_value = " ".join(word_pos.split(" [")[0].split())  # taking the first entry (pos) and removing redundant
        # whitespaces

        words_pos_dict[key_no] = pos_value

    # save the story to a file
    with open("stories/story" + str(story_number) + ".txt", "w", encoding="utf-8") as file:
        file.write(story_title)
        file.write('\n' + str(words_pos_dict))
        file.write('\n' + story)
        file.close()

    # add a new entry in the stories list
    story_lib.append(story_title)

    # progress control
    progress = round((story_number/story_count)*100, 2)
    print(str(progress) + "%")

with open("stories/library.txt", 'w') as lib:
    lib.write(str(story_lib))
    lib.close()

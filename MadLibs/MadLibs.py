from math import *


def display_menu():
    """
    Function opens file with list of all stories and allows user to choose one.

    :return: story number
    """

    # getting the library file and cleaning it up
    with open("stories/library.txt", "r") as stories_list:
        library = stories_list.read()
        library = library[1:-1]  # remove starting and ending brackets ('[' and ']')
        library = library.split("', '")  # split into list elements
        # remove apostrophes from the first and the last entry
        library[0] = library[0][1:len(library[0])]
        library[-1] = library[-1][0:-1]

    # greeting
    username = input("What is your name: ")
    print("\nHi " + username + "!")
    print("You can choose from " + str(len(library)) + " ad-lib word games. Have fun!\n")

    print("Each of those was taken from https://www.madtakes.com/ (est. 2004 Nathanael\n"
          "Huddleson) website. Visit it for full experience!\n")

    print("Choose number (1-" + str(len(library)) + ") of the story you'd like to explore.\n"
          "To view more titles type '<' or '>' for previous and next\n"
          "page respectively. If you want to choose certain page type\n"
          "'p#', e.g. for page number 11 type p11. Enter '*' at any\n"
          "point to exit.\n")

    # display the list of stories in a loop to 'refresh' it if user changes the page
    current_page = 1
    while True:
        # set limits to story number and page number respectively
        first_element = ((current_page - 1) * 10)
        last_element = current_page * 10
        max_page = ceil(len(library) / 10)

        # last_element set to the number of the last story if the user selects the last page. E.g. we have 188 stories
        # which gives 19 pages, 10 stories each except the last one which has only 8 stories. If that wouldn't be
        # considered the previous equation for last_element would set it to 190 - it would exceed the index limit
        if last_element >= len(library):
            last_element = len(library)

        # print list of stories
        for i in range(first_element, last_element):
            print(str(i+1) + ". " + library[i])

        # user input and input validation in a loop from obvious reasons
        while True:
            user_input = input("\nType here: ")

            # specify allowed inputs as 2d list
            allowed_input = [
                ["<", ">"],
                [],
                []
            ]

            # generate allowed inputs for story numbers and page numbers respectively
            for i in range(1, len(library)):
                allowed_input[1].append(str(i))
            for page_number in range(1, max_page):
                allowed_input[2].append("p" + str(page_number))

            # using if/elif/else instead of match/case as I need to verify few things on the way
            if user_input in allowed_input[0]:
                # if user selected to switch the page check if he's not @ the 1st one and wants to go to 0th or @ max
                # and wants to go to the max+1
                if user_input == "<" and current_page != 1:
                    current_page -= 1
                    break
                elif user_input == ">" and current_page != max_page:
                    current_page += 1
                    break
                else:
                    print("Cannot switch pages.")  # continue
            elif user_input in allowed_input[1]:
                print(library[int(user_input) - 1])
                return user_input
            elif user_input in allowed_input[2]:
                current_page = int(user_input[1:])
                break
            elif user_input == "*":
                return user_input  # that's for exiting the game
            else:
                print("Incorrect input.")  # continue


def read_file(story_no):
    """
    Function finds the story chosen by the user, reads it and extract, cleans and separates pos_words and story.

    :param story_no: number of the story that's going to be used to localise the user's choice
    :return:    dict_pos_words: dictionary containing numbers of part-of-speech words in order as keys and
                                part-of-speech words itself as values.
                str_story:      string containing the story.
    """

    story_dir = "stories/story" + str(story_no) + ".txt"

    with open(story_dir, "r") as story_file:
        story = story_file.readlines()
        str_pos_words = story[1]
        str_story = story[2]

    # split the string into elements of list
    list_pos_words = str_pos_words.split("', '")

    # remove redundant braces '{' and '}'
    list_pos_words[0] = list_pos_words[0][1:]
    list_pos_words[-1] = list_pos_words[-1][:-2]
    # remove apostrophes from the first and last element of the list
    list_pos_words[0] = list_pos_words[0][1:]
    list_pos_words[-1] = list_pos_words[-1][:-1]

    # create empty dictionary
    dict_pos_words = {}

    for pos_word in list_pos_words:
        # split into list of the number of pos word and the word itself
        pos_word_sublist = pos_word.split("': '")
        # add key-value pair to the dictionary
        dict_pos_words[pos_word_sublist[0]] = pos_word_sublist[1]

    return dict_pos_words, str_story


def words_input(dict_pos_words):
    """
    Function extracts part-of-speech words from the dictionary and asks user to fill them up or randomise.

    :param dict_pos_words:  dictionary containing numbers of part-of-speech words in order as keys and
                            part-of-speech words itself as values.
    :return:
    list_words: list of words to fill up the story with.
    user_input: a boolean string that decides outside the function whether the user wants to exit the game, go back to
    menu or not.
    """

    list_words = []
    user_input = None

    # tell user how many words the is to fill up
    print("The story has " + str(len(dict_pos_words)) + " gaps to fill up.")

    # define iterator
    i = 1

    while i <= len(dict_pos_words):
        # predefine key
        key = "[" + str(i) + "]"

        user_input = input(key + " " + dict_pos_words[key] + ": ")
        # here I need to stop and figure out how to get a complete list of parts of speech from the whole game and
        # then how to make user input validation based on that list.
        # I did, and it doesn't make sense to go through 239 "PoS's". Peoples are making up their own "PoS's".
        # Well, I kinda should, but later. I will update the game at some point.

        if user_input == "*" or user_input == "<":
            # user wants to exit the game or go back to menu
            return list_words, user_input
        elif user_input == "^":
            # user wants to change the previous word
            if i != 1:
                i -= 1
            else:
                print("Cannot go back.")
            continue
        else:
            # else it's probably a word
            word = user_input
            user_input = None

        # add word to the list
        list_words.append(word)
        # increment the iterator
        i += 1

    return list_words, user_input


def fill_up_story(list_words, empty_story):
    """
    Function replaces numbers (gaps) in the story with words given by the user.

    :param list_words: list of words to replace numbers with.
    :param empty_story: story with gaps.
    :return: story without gaps
    """
    for i in range(1, len(list_words) + 1):
        empty_story = empty_story.replace("[" + str(i) + "]", "*" + list_words[i-1] + "*")

    return empty_story


while True:
    # define flags for basic game functions
    exit_game = False
    back_to_menu = False
    repeat_story = False

    # display menu for the user
    usr_input = display_menu()
    if usr_input == "*":
        # exit game if the input is '*'
        break
    else:
        # carry on if he inputs a story number
        story_number = usr_input

    while True:
        pos_words, story = read_file(story_number)
        words, usr_input = words_input(pos_words)

        if usr_input == "*":
            # exit game
            exit_game = True
            break
        elif usr_input == "<":
            # go back to the menu
            break
        else:
            # fill up the story with words given by the user
            story = fill_up_story(words, story)
            print(story)
            print("Type 'r' to repeat the story, '*' to exit the game or '<' to go back to main menu.")

            while True:
                usr_input = input("What would you like to do now: ")

                if usr_input == "*":
                    # exit game
                    exit_game = True
                elif usr_input == "<":
                    # go back to menu
                    back_to_menu = True
                elif usr_input == "r":
                    # repeat the story
                    repeat_story = True
                else:
                    print("Wrong input")
                    continue
                break

            # checking flags after filling up and displaying the story
            if exit_game or back_to_menu:
                break
            elif repeat_story:
                repeat_story = False
                continue
            else:
                pass

    # checking flags outside the end-game. it also checks them again after breaking the previous loop - also caused by
    # the same flags.
    if exit_game:
        break
    elif back_to_menu:
        continue
    else:
        pass

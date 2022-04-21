def get_all_pos():
    """
    Function extracts all part-of-speech terms from every story.

    :return: all_pos: list of all pos across all stories.
    """

    all_pos = []

    # getting the library file and finding out its size
    with open("stories/library.txt", "r") as stories_list:
        library = stories_list.read()
        library = library.split("', '")  # split into list elements
        no_of_stories = len(library)  # get number of stories

    for i in range(1, no_of_stories):
        with open("stories/story" + str(i) + ".txt", "r") as story_file:
            # get only the second line - part-of-speech with numbers
            story_file_content = story_file.readlines()
            str_pos = story_file_content[1]

            # separate each pos (and number) into elements of a list
            list_pos = str_pos.split("', '")

            # remove bracket and apostrophe from the ending of the last element
            list_pos[-1] = list_pos[-1][:-3]

            # remove numbers from the elements fo the list and save pos to all_pos list
            for pos in list_pos:
                pos = pos.split("': '")
                all_pos.append(pos[1])

    return all_pos


# right, it doesn't make sense
print(len(list(set(get_all_pos()))))

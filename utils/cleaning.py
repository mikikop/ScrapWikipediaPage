def cleaning_list(word_list: list):
    """
    Returns a list cleaned from [, ] and what is between.
    For example if in the list there is a key-value like the following one:
    'Cattle': ['bovine', '[', 'd', ']', 'taurine (male)', 'vaccine (female)', 'vituline (young)']
    the function will remove'[', 'd', ']' and will return:
    'Cattle': ['bovine', 'taurine (male)', 'vaccine (female)', 'vituline (young)']

    :param word_list: list of the adjectives
    :return: cleaned_list: list of the adjectives cleaned of the references
    """

    cleaned_list = []
    skip = False

    for adj in word_list:
        if adj == '[':
            skip = True
        elif adj == ']':
            skip = False
        elif not skip:
            cleaned_list.append(adj)
    return cleaned_list


lexicon = {
    'directions': ['north', 'south', 'east', 'west', 'up', 'down', 'left',
                   'right', 'back'],
    'verbs': ['shoot', 'dodge', 'tell', 'throw', 'place', 'help'],
    # stop words: words which do not contain important significance
    # to be used in Search Queries
    # http://xpo6.com/list-of-english-stop-words/
    'stopwords': ['a', 'an', 'the', 'this', 'that', 'slowly'],
    'nouns': ['joke', 'bomb'],
}


def scan(text):
    result = []
    words = text.split()
    for word in words:
        word = word.strip('!').lower()
        if word in lexicon['directions']:
            result.append(('direction', word))
        elif word in lexicon['verbs']:
            result.append(('verb', word))
        elif word in lexicon['stopwords']:
            result.append(('stop', word))
        elif word in lexicon['nouns']:
            result.append(('noun', word))
        elif convert_numbers(word) and len(word) < 9:
            result.append(('number', word))
        else:
            result.append(('error', word))

    return result


def convert_numbers(s):
    try:
        return int(s)
    except ValueError:
        return None
class ParserError(Exception):
    def __init__(self, description):
        self.description = description

    def __str__(self):
        return repr(self.description)


class Sentence(object):

    def __init__(self, subject, verb, object=None):
        # remember we take ('noun', 'princess') tuples and convert them
        if not subject:
            self.subject = ''
        else:
            self.subject = subject[1]
        if not verb:
            self.verb = ''
        else:
            self.verb = verb[1]
        if not object:
            self.object = ''
        else:
            self.object = object[1]

    def build_string(self):
        return (self.subject + ' ' + self.verb + ' ' + self.object).strip(' ')


def peek(word_list):
    """peek at a list of words and return what type of word it is

    :param word_list: list of words (list of tuple)
    :return: word type (string)
    """
    if word_list:
        word = word_list[0]
        return word[0]
    else:
        return None


def match(word_list, expecting):
    """ pop (remove) word from list and return word,
    if your expectation matches the word type, None otherwise

    :param word_list: list of words (list of tuple)
    :param expecting: word type (string)
    :return: word (tuple)
    """
    if word_list:
        word = word_list.pop(0)

        if word[0] == expecting:
            return word
        else:
            return None
    else:
        return None


def skip(word_list, word_type):
    """skip stop words

    :param word_list: list of words (list of tuple)
    :param word_type: word type to skip (e.g. stop)
    :return: return word
    """
    while peek(word_list) == word_type:
        match(word_list, word_type)


def parse_verb(word_list):
    skip(word_list, 'stop')
    if peek(word_list) == 'verb':
        return match(word_list, 'verb')
    if peek(word_list) == 'number':
        return None
    else:
        raise ParserError("Expected a verb next.")


def parse_object(word_list):
    skip(word_list, 'stop')
    next_word = peek(word_list)
    if next_word == 'noun':
        return match(word_list, 'noun')
    elif next_word == 'direction':
        return match(word_list, 'direction')
    elif not next_word:
        return None
    elif next_word == 'number':
        return word_list[0]
    else:
        raise ParserError("Expected a noun or direction next.")


def parse_subject(word_list):
    skip(word_list, 'stop')
    next_word = peek(word_list)
    if next_word == 'noun':
        return match(word_list, 'noun')
    elif next_word == 'verb':
        return None
    elif next_word == 'number':
        return None
    else:
        raise ParserError("Expected a verb next.")


def parse_sentence(word_list):
    subj = parse_subject(word_list)
    verb = parse_verb(word_list)
    obj = parse_object(word_list)

    return Sentence(subj, verb, obj)

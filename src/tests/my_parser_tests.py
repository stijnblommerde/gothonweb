"""
wanneer heb je voldoende getest?
goede tests doorlopen 100% van de te testen code
"""

from nose.tools import *

# add src to paths
# http://stackoverflow.com/questions/19885821/how-do-i-import-modules-in-pycharm
from src.bin.my_parser import *


def test_peek():
    assert_equals(None, peek([]))
    assert_equals('verb', peek([('verb', 'run'), ('direction', 'north')]))


def test_match():
    assert_equals(None, match([], 'verb'))
    sentence = [('verb', 'run'), ('direction', 'north')]
    assert_equals(('verb', 'run'),
                  match(sentence, 'verb'))
    assert_equals([('direction', 'north')], sentence)
    assert_equals(None,
                  match([('verb', 'run'), ('direction', 'north')], 'direction'))


def test_parse_subject():
    # check for an exception
    # syntax assert_raises([error class], [function], [function arguments])
    assert_raises(ParserError, parse_subject, [])


def test_parse_sentence():
    sentence = parse_sentence([('verb', 'run'), ('direction', 'north')])
    assert_equal('player', sentence.subject)
    assert_equal('run', sentence.verb)
    assert_equal('north', sentence.object)



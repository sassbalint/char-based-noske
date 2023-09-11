"""
Convert classic word-basd corpus to a char-based corpus.
"""


import re
import sys

from itertools import chain, islice
from more_itertools import consume, map_if


SEP = '\t'


def skip(it, n):
    """Skip first n element of an iterator."""
    yield from islice(it, n, None)


def sar(it, search, replace):
    """A general search-and-replace funcionality for iterators."""
    for elem in it:
        yield re.sub(search, replace, elem)


def process_field(line, index, func, sep='\t'):
    """Split line by `sep` then apply `func` to field `index`."""
    fields = line.split(sep)
    fields[index] = func(fields[index])
    return sep.join(fields)


def append(it, cond, new_elem):
    """If `cond` is True append a `new_elem` at that point."""
    for elem in it:
        yield elem
        if cond(elem): yield new_elem


def process(it):
    """Process one file as an iterator."""

    fileid = ":)"

    # no newline
    it = map(lambda x: x.rstrip('\n'), it)

    TAGNAME = 'w' # XML tag name for words (containing several lines for chars)

    def is_dataline(elem):
        return SEP in elem

    def toxml(fields): # XXX to be implemented :)
        return f'<{TAGNAME} attrs="' + ' '.join(fields) + '">' # XXX to be refactored

    # TODO XXX
    #  * combining karakatereket ne válassza le!
    #  * rendesen megcsinálni az illesztést!
    #    ugy sokszo 2 char vs 1 char van!
    #  * rendesen megcsinálni az eredeti attribútumok megjelenítését

    # egy iterátor feldolgozása során hogyan tudok úgy egy elemből egy iterátort csinálni úgy, hogy szépen belesimuljon az eredeti iterátor elemeinek sorába? hát pl. így! :)
    def split_elems(it, cond, sep='\t'):
        ORIG, NORM = 2, 4 # XXX to be refactored
        for elem in it:
            if cond(elem):
                fields = elem.split(sep)
                yield toxml(fields) # XXX to be refactored
                for ch1, ch2 in zip(fields[ORIG], fields[NORM]):
                    yield f"{ch1}\t{ch2}"
                yield f"</{TAGNAME}>" # XXX to be refactored
            else:
                yield elem
    it = split_elems(it, is_dataline)
    consume(map(print, it))


def main():
    """Main."""
    process(sys.stdin)


if __name__ == '__main__':
    main()


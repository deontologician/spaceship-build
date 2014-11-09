'''Utility functions used elsewhere'''

import re
import string

# This is what is exported from the module
__all__ = ['fprint', 'caps_to_hyphens', 'letterer', 'unletterer']


def fprint(template, *args, **kwargs):
    '''prints to stdout, using format syntax
    
    Example:
    >>> fprint('Oh, hi {name}!', name='Mark')
    Oh, hi Mark!
    '''
    print(template.format(*args, **kwargs))


def caps_to_hyphens(name):
    '''Turns 'SpaceShip' into 'space-ship' '''
    chunks = re.findall(r'[A-Z]+[a-z]*', name)
    return '-'.join(s.lower() for s in chunks)


_letters = chars = string.ascii_lowercase + '234567'


def letterer(num):
    r'''Creates a short (base 32) string for any positive integer passed in.

    >>> letterer(0)
    'a'
    >>> letterer(25)
    'z'
    >>> letterer(26)
    '2'
    >>> letterer(32)
    'aa'
    >>> letterer(1055), letterer(1056)
    >>> '77', 'aaa'
    >>> try:
    ...     letterer(-1)
    ... except ValueError as ve:
    ...     str(ve)
    'Number must be 0 or greater'
    '''
    charlen = len(_letters)  # should be 32
    if num < 0:
        raise ValueError("Number must be 0 or greater")
    letters = [_letters[num % charlen]]
    while num >= charlen:
        num = (num // charlen) - 1
        letters.append(_letters[num % charlen])
    return ''.join(reversed(letters))

_unletters = {_lett: x for x, _lett in enumerate(_letters)}
_unletters['1'] = _unletters['l']
_unletters['0'] = _unletters['o']


def unletterer(letters):
    r'''Converts lowercase letters encoded by letterer back into a number
    >>> unletterer('a')
    0
    >>> unletterer('aa')
    32
    >>> unletterer('a0')  # a0 => ao
    35
    >>> unletterer('a1')  # a1 => al
    '''
    letters = letters.lower()
    bad_chars = set(letters).difference(_unletters.keys())
    if bad_chars:
        raise ValueError('{} are not valid characters'.format(
            ','.join(bad_chars)))
    revnums = [_unletters[let] for let in reversed(letters)]
    revnums.append(0)  # extra value for carries
    value = revnums[0]
    for power, num in enumerate(revnums[1:], 1):
        if power < len(revnums) - 1:
            num += 1
        if num > 31:
            carry, num = divmod(num, 32)
            revnums[power] += carry
        value += num * 32 ** power
    return value
from random import choice, randint, sample, shuffle, gauss, random
import re
from collections import namedtuple

COMPANY_STEMS = [
    "arch",
    ('atom', ['', 'i', 'ic']),
    ('agis', ['']),
    "aur",
    ("ban", ['a', 'i', 'u',]),
    "bio",
    ("chron", ['a', 'i', '']),
    "col",
    "com",
    'deka',
    "gen",
    ("jov", ['a','i','ia']),
    ("kang", ['u','a']),
    ("mal", ['a', 'e', 'i']),
    ("met", ['a']),
    ("mil", ['a', 'io', 'i', 'li']),
    ("lun", ['a', 'ar', 'i']),
    ("nan", ['o', 'i']),
    ("ner", ['']),
    ("on", ['o', 'a', 'i', 'u']),
    ("plex", ['i', 'a', '', 'o']),
    "prot",
    ("pur", ['a', 'i', 'e']),
    ("sec", ['u', 'ure']),
    ("sk", ['y']),
    ("sol", ['a','i']),
    "star",
    ("sun", ['']),
    ("tel", ['e', 'a']),
    ("ter", ['a', 'ra', 'ra ', 'i', 'u', 'o']),
    "tir",
    ("tok", ['a', 'u', 'i']),
    ('ton', ['i', 'a', 'u', 'o']),
    "tren",
    ("un", ['i', 'a', 'e']),
    ("verd", ['u', 'a', 'ant']),
    ("w", ['eis', 'yl', 'y', 'ey', 'eyl']),
    "yut",
]

PRE_TERMINALS = [
    "Design",
    "Dynamics",
    "Engineering",
    "Enterprises",
    "Foundation",
    "Galactic",
    "Incorporated",
    "Industries",
    "International",
    "Interplanetary",
    "Laboratories",
    "Limited",
    "Manufacturing",
    "Orbital",
    "Products",
    "Supply",
    "Syndicate",
    "Universal",
    "Ventures",
]

TERMINALS = [
    "Co.",
    "Llc.",
    "Ltd.",
    "Inc.",
    "Corp.",
    "Company",
    "Corporation",
]

RARE_PREFIXES = [
    'epi',
    'meta',
    'hyper',
    'itsu',
    'astral',
    'sub',
]

JOINERS = [
    'a',
    'e',
    'i',
    'o',
    'u',
    ' ',
    '',
]

SUFFIXES = [
    'al',
    'dyn',
    'ex',
    'dev',
    'gen',
    'ogia',
    'hama',
    'hiko',
    'hito',
    'ia',
    'ic',
    'ine',
    'is',
    'logic',
    'man',
    'ology',
    'sec',
    'tech',
    'uko',
    'us',
    'tron',
    'land',
    'ani',
    'tor',
]

FIELDS = {
    'ammunition': 1,
    'armor': 1,
    'cabling': 1,
    'cooling': 1,
    'electronics': 1,
    'ftl-cores': 2,
    'life-support': 2,
    'power': 2,
    'propulsion': 2,
    'sensors': 1,
    'shield generators': 2,
    'structural': 2,
    'waste-disposal': 1,
    'weaponry': 1,
    'wiring': 1,
}

class Name(str):
    '''A string subclass that keeps track of its constituent parts'''
    def __init__(self, piece=None):
        self.pieces = [piece] if piece is not None else []

    def __add__(self, other):
        new = Name(super().__add__(other))
        if hasattr(other, 'pieces'):
            new.pieces = self.pieces + other.pieces
        else:
            new.pieces = self.pieces + [other]
        return new

    def title(self):
        x = Name(super().title())
        x.pieces = self.pieces[:]
        return x


def with_probability(x):
    '''Returns true with probability x'''
    return random() <= x

def extract(stem):
    '''Extract a stem and joiners'''
    if isinstance(stem, tuple):
        joiners = stem[1]
        stem = stem[0]
    else:
        joiners = JOINERS
        stem = stem
    return stem, joiners

def corp_name(stems=None, suffixes=None):
    '''Creates the non-sensical part of the name'''
    if stems is None:
        stems = COMPANY_STEMS[:]
        shuffle(stems)
    if suffixes is None:
        suffixes = SUFFIXES[:]
        shuffle(suffixes)
    name = Name()
    first_stem = None
    second_stem = None

    if with_probability(1/16):
        name += choice(RARE_PREFIXES)
    first_stem, joiners = extract(stems.pop())
    name += first_stem
    if with_probability(1/3):
        name += choice(joiners)
        second_stem, joiners = extract(stems.pop())
        name += second_stem
    if len(name) <= 9:
        name += choice(list(set(joiners) - {' '}))
        name += suffixes.pop()
    return normalize(name)

def normalize(name):
    '''Fixes several weirdnesses in final names'''

    name_final = name\
        .replace('ao', choice('ao'))\
        .replace('uo', choice('uo'))\
        .replace('aeo', 'o')\
        .replace('ea', 'e a')\
        .replace('oex', 'ex')\
        .replace('ii', 'i')\
        .replace('oo', 'o')\
        .replace('aa', 'a')\
        .replace('uu', 'u')\
        .replace('hh', 'h')\
        .replace('ee', 'e')\

    ret = Name(name_final)
    ret.pieces = name.pieces[:]
    return ret

def company_name(stems=None, suffixes=None, pre_terminals=None):
    '''Creates a random company name. Deletes items from stems and
    suffixes, so don't pass in the global versions or you'll quickly
    run out!
    '''
    if pre_terminals is None:
        pre_terminals = PRE_TERMINALS[:]
        shuffle(pre_terminals)
    name = corp_name(stems, suffixes)
    name = name.title()
    if with_probability(1/2):
        name += ' ' + choice(pre_terminals)
    if with_probability(2/3):
        name += ' ' + choice(TERMINALS)
    return name

def buy_fields(name, field_markets):
    total_points = max(round(gauss(6, 4)), 1)
    points = total_points
    fields = {}
    while points > 0 and field_markets:
        (field, market), cost = choice(list(field_markets.items()))
        fields[field] = market
        del field_markets[(field, market)]
        points -= cost
    return fields


class Company:
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields


def make_companies():
    '''Creates several companies'''
    stems = COMPANY_STEMS[:]
    suffixes = SUFFIXES[:]
    pre_terminals = PRE_TERMINALS[:]
    shuffle(stems)
    shuffle(suffixes)
    shuffle(pre_terminals)
    markets = {
        'high-end': 4,
        'mid-market': 2,
        'low-end': 1,
    }
    field_markets = {(field, market): fp * mp
                     for field, fp in FIELDS.items()
                     for market, mp in markets.items()}
    companies = []
    while field_markets:
        name = company_name(stems, suffixes, pre_terminals)
        fields = buy_fields(name, field_markets)
        companies.append(Company(name, fields))
    return companies

def build_trie():
    assoc = {}
    while True:
        try:
            suggested = corp_name()
            answer = input(suggested.title() + ' [y/N]: ')
            if answer in ('Y','y','yes'):
                if len(suggested.pieces) > 1:
                    for fst, snd in zip(suggested.pieces[:-1], suggested.pieces[1:]):
                        assoc[fst] = snd
                else:
                    assoc[fst] = ''

        except KeyboardInterrupt:
            break
    return assoc

if __name__ == '__main__':
    companies = make_companies()
    for company in companies:
        print(company.name)
        print('    ', company.name.pieces)
        #for field, market in company.fields.items():
        #    print('  ', market, field)
    print(len(companies), 'created')

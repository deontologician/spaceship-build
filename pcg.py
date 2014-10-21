from random import choice, randint, sample, shuffle, gauss, random
from itertools import product
from copy import deepcopy
import string
from pcg_data import (COMPANY_STEMS, PRE_TERMINALS, TERMINALS,
                      RARE_PREFIXES, JOINERS, SUFFIXES, WORD_GROUPS,
                      GREEK_LETTERS)

# Each field has a point cost. Companies that specialize in higher
# point-cost fields will have less fields overall (usually)

# Naming schemes
# Something ending in "Pro"
# - Chiron, Chiron Pro
# - '{} {}Pro'.format(noun(), adjective())
# Something with 2-3 letters ending with X
# - ATX, DX, MX, LX
# - upper_letters(randint(1, 2)) + 'X'
# number schemes
# - 2511, 8511, 9511 # ending numbers the same
# - '{{}}{}'.format(digits(3)).format(model_level + 1)
# - 9512, 9524, 9550 # starting numbers the same
# - 
# - 50, 60, 70 # Just some sort of sequential numbers
# Letter and number
# - M23, F13, X-23
# - Always using the same letter, or letter per line
# Names based on provocative stuff
# - dragoon, python, peacemaker, cobra, defender
# Letters hyphen numbers letter
# - FRD-1020R
# Letters, hyphen then single number
# - GE10-1, GE10-2
# Series Roman numeral
# - Series II, Series III
# Mark Roman numeral
# - Mark I, Mark II
# Compound neologisms
# - Nightreaver
# - SandTamer
# And of course: Names that have something to do with the product and its attributes
# - 200mm long-range rifle
# - 400MW Generator


def digits(n):
    '''Yields an n digit number'''
    return ('{}'*n).format(randint(1, 9), *(randint(0,9) for _ in range(n-1)))


def upper_letters(n):
    '''Yields a random string of uppercase letters n characters long'''
    return ''.join(sample(string.ascii_uppercase, n))


# Heirarchy of objects:
# Company -> Field -> Market -> ProductLine -> Model
# each relationship is one to many


# TODO: define durability in terms of hours of expected usage

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

def corp_name(stems, suffixes):
    '''Creates the non-sensical part of the name'''
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
        .replace('oo', 'oö')\
        .replace('aa', 'a')\
        .replace('uu', 'u')\
        .replace('hh', 'h')\
        .replace('ee', 'e')\

    ret = Name(name_final)
    ret.pieces = name.pieces[:]
    return ret


class NameParts:
    def __init__(self):
        self.stems = COMPANY_STEMS[:]
        shuffle(self.stems)
        self.suffixes = SUFFIXES[:]
        shuffle(self.suffixes)
        self.pre_terminals = PRE_TERMINALS[:]
        shuffle(self.pre_terminals)


class Company:
    '''Represents a producer of goods'''
    def __init__(self, parts, field_markets):
        self.initial_points = max(round(gauss(6, 4)), 1)
        self.name = self._create_name(parts)
        self.fields, self.point_debt = self._buy_fields(field_markets)

    @property
    def points(self):
        return self.initial_points - self.point_debt

    def _create_name(self, parts):
        '''Creates a random company name. Deletes items from stems and
        suffixes, so don't pass in the global versions or you'll quickly
        run out!
        '''
        name = corp_name(parts.stems, parts.suffixes)
        name = name.title()
        if with_probability(1/2):
            name += ' ' + choice(parts.pre_terminals)
        if with_probability(2/3):
            name += ' ' + choice(TERMINALS)
        return name

    def _buy_fields(self, field_markets):
        '''Purchases several fields for the company based on the
        number of points it received'''
        points = self.initial_points
        fields = []
        while points > 0 and field_markets:
            index = randint(0, len(field_markets) - 1)
            fieldmarket = field_markets[index]
            fields.append(fieldmarket)
            del field_markets[index]
            points -= fieldmarket.cost
        return fields, points

    def create_lines(self, word_groups):
        '''Create all product lines, given the provided word_groups'''
        

class FieldMarket:
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
    
    MARKETS = {
        'high-end': 4,
        'mid-market': 2,
        'low-end': 1,
    }

    def __init__(self, field, market):
        self.field = field
        self.market = market
        self.cost = self.FIELDS[field] * self.MARKETS[market]

    def __str__(self):
        return '{} {}'.format(self.level, self.field)

    @staticmethod
    def all_combinations():
        '''Create a list of all combinations of fields and markets'''
        return [FieldMarket(field, market)
                for field, market in 
                product(FieldMarket.FIELDS, FieldMarket.MARKETS)]

def make_companies():
    '''Creates companies'''
                     
    parts = NameParts()
    field_markets = FieldMarket.all_combinations()
    companies = [Company(parts, field_markets)
                 for _ in range(100) if field_markets]
    word_groups = deepcopy(WORD_GROUPS)
    companies.sort(key=lambda c: c.points, reverse=True)
    for company in companies:
        company.create_lines(word_groups)
    return companies


if __name__ == '__main__':
    companies = make_companies()
    for company in companies:
        print(company.name, ':', company.points)
        for fieldmarket in company.fields:
            print('  ', fieldmarket.market, fieldmarket.field, ':', fieldmarket.cost)
    print(len(companies), 'created')

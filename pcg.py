from random import choice, randint, sample, shuffle, gauss
from collections import namedtuple

COMPANY_STEMS = [
    "arch",
    "aur",
    "ban",
    "bio",
    "chron",
    "col",
    "com",
    'deka',
    'dev',
    "drov",
    "gen",
    "jov",
    "kam",
    "kang",
    "mal",
    "meta",
    "mil",
    "lun",
    "nano",
    "ner",
    "ono",
    "plex",
    "prot",
    "pur",
    "secu",
    "sky",
    "sol",
    "star",
    "sun",
    "tel",
    "ter",
    "tir",
    "tok",
    'ton',
    "tren",
    "uni",
    "verdu",
    "weis",
    "yut",
]

COMPANY_TYPES_LONG = [
    "Company",
    "Corporation",
    "Dynamics",
    "Enterprises",
    "Foundation",
    "Galactic",
    "Incorporated",
    "Industries",
    "International",
    "Interplanetary",
    "Universal",
    "Ventures",
    "Laboratories",
    "Syndicate",
]

COMPANY_TYPES_SHORT = [
    "Co.",
    "Llc.",
    "Ltd.",
    "GmbH",
    "Inc.",
    "Corp.",
]

RARE_PREFIXES = [
    'epi',
    'meta',
    'hyper',
    'itsu',
]

PREFIXES = [
    'am',
    'ano',
    'a',
    'e',
    'i',
    'o',
]

JOINERS = [
    'a',
    'o',
    'u',
    'i',
    ' ',
]

SUFFIXES = [
    'agis',
    'al',
    'dyn',
    'ex',
    'gen',
    'ogia',
    'hama',
    'hiko',
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
    ' supply',
    ' products',
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

def company_name(stems, suffixes, long_types):
    '''Creates a random company name. Deletes items from stems and
    suffixes, so don't pass in the global versions or you'll quickly
    run out!
    '''
    name = ''
    used_stems = []
    if not randint(0, 3):
        if not randint(0, 3):
            name += choice(RARE_PREFIXES)
        else:
            name += choice(PREFIXES)
    used_stems.append(stems.pop())
    name += used_stems[-1]
    if not randint(0, 2):
        if randint(0, 1) and name[-1] not in 'aeiouy':
            # prevent the hawaiian problem
            name += choice(JOINERS)
        used_stems.append(stems.pop())
        name += used_stems[-1]
    if not randint(0, 2) or name in used_stems:
        if name.endswith('v'):
            name += choice(JOINERS + ['e'])
        name += suffixes.pop()
    name = name.title()
    if randint(0, 1) and len(name) <= 7:
        name += ' ' + long_types.pop()
    elif randint(0, 1) and len(name) >= 7:
        name += ' ' + choice(COMPANY_TYPES_SHORT)
    return name

def buy_fields(name, field_markets):
    total_points = max(round(gauss(6, 3)), 1)
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
    long_types = COMPANY_TYPES_LONG[:]
    shuffle(stems)
    shuffle(suffixes)
    shuffle(long_types)
    markets = {
        'high-end': 3,
        'mid-market': 2,
        'low-end': 1,
    }
    field_markets = {(field, market): fp * mp
                     for field, fp in FIELDS.items()
                     for market, mp in markets.items()}
    companies = []
    while field_markets:
        name = company_name(stems, suffixes, long_types)
        fields = buy_fields(name, field_markets)
        companies.append(Company(name, fields))
    return companies


if __name__ == '__main__':
    companies = make_companies()
    for company in companies:
        print(company.name)
        for field, market in company.fields.items():
            print('  ', market, field)
    print(len(companies), 'created')
    
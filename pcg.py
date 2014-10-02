from random import choice, randint, sample, shuffle

COMPANY_STEMS = [
    "arch",
    "aur",
    "bio",
    "ban",
    "chron",
    "col",
    "com",
    'dev',
    'deka',
    "drov",
    "gen",
    "jov",
    "kam",
    "kang",
    "mal",
    "meta",
    "mil",
    "nano",
    "ner",
    "ono",
    "plex",
    "prot",
    "pur",
    "secu",
    "sky",
    "star",
    "sun",
    "tel",
    "ter",
    "tok",
    "tren",
    "tyc",
    "tir",
    "uni",
    "verdu",
    "weis",
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
    'u',
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

]

FIELDS = [
    'propulsion',
    'power',
    'cooling',
    'ammunition',
    'weaponry',
    'life-support',
    'waste-removal',
    'sensors',
]

def company_name(stems, suffixes, long_types):
    '''Creates a random company name. Deletes items from stems and
    suffixes, so don't pass in the global versions or you'll quickly
    run out!
    '''
    name = ''
    has_suffix = False
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
            name += choice(JOINERS)
        used_stems.append(stems.pop())
        name += used_stems[-1]
    if not randint(0, 2) or name in used_stems:
        name += suffixes.pop()
    name = name.title()
    if randint(0, 1) and len(name) <= 7:
        name += ' ' + long_types.pop()
    elif randint(0, 1) and len(name) >= 7:
        name += ' ' + choice(COMPANY_TYPES_SHORT)
    return name

def make_companies():
    '''Creates 15 companies'''
    stems = COMPANY_STEMS[:]
    suffixes = SUFFIXES[:]
    long_types = COMPANY_TYPES_LONG[:]
    shuffle(stems)
    shuffle(suffixes)
    shuffle(long_types)
    return [company_name(stems, suffixes, long_types) for _ in range(15)]

if __name__ == '__main__':
    for company in make_companies():
        print(company)
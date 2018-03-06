#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tools for extracting phonetic information from words using cmudict
"""

from nltk.corpus import cmudict
from itertools import tee

__author__ = 'drisme'

dct = cmudict.dict()

consonants = {
    'sto': ['P', 'B', 'T', 'D', 'K', 'G'],
    'aff': ['CH', 'JH'],
    'fri': ['F', 'V', 'TH', 'DH', 'S', 'Z', 'SH', 'ZH', 'HH'],
    'nas': ['M', 'EM', 'N', 'EN', 'NG', 'ENG'],
    'liq': ['L', 'EL', 'R', 'DX', 'NX'],
    'sem': ['Y', 'W', 'Q']
}

vowels = {
    'monophthongs':
        ['AO', 'AA', 'IY', 'UW', 'EH', 'IH', 'UH', 'AH', 'AX', 'AE'],
    'diphthongs': ['AY', 'EY', 'OY', 'AW', 'OW'],
    'r-colored': ['', '', '', '', '', '', '', '', '']

}

voiced = ['B', 'V', 'D', 'Z', 'DH', 'ZH', 'JH', 'G'] +\
    consonants['nas'] + consonants['liq'] + consonants['sem']
voiceless = ['P', 'F', 'T', 'S', 'TH', 'SH', 'CH', 'K', 'HH']


def create_reverse_consonant_dict():
    result_dict = {}
    for key, values in consonants.items():
        for consonant in values:
            result_dict[consonant] = key
    return result_dict


reverse_consonants = create_reverse_consonant_dict()


def get_consonant_types(consonant_list):
    result = [reverse_consonants[x] for x in consonant_list]
    if None in result:
        raise Exception("Nonetype found in list")
    return result


def get_voicing(phoneme):

    if phoneme in voiced:
        return 1
    elif phoneme in voiceless:
        return 0
    else:
        pass
        # raise Exception("Phoneme '%s' doesn't
        # match any known consonants" % phoneme)


def is_stress(phoneme):
    return any((char == '1' or char == '2') for char in phoneme)


def has_numbers(string):
    return any(char.isdigit() for char in string)


def remove_numbers(string):
    result = ''
    for char in string:
        if not char.isdigit():
            result += char
    return result


def pure_phonemes(phonemes):
    results = []
    for phoneme in phonemes:
        results.append(remove_numbers(phoneme))
    return results

def pairwise(iterable):
    """
    from itertools recipes
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def extract_tuples(phonemes):
    return list(''.join(pair) for pair in pairwise(pure_phonemes(phonemes)))


def extract_number(string):
    for char in string:
        if char.isdigit():
            return int(char)


def to_affricative(phoneme):
    return 'front'


def extract_vowels(phonemes):
    results = []
    for phoneme in phonemes:
        if has_numbers(phoneme):
            results.append(remove_numbers(phoneme))
    return results


def extract_consonants(phonemes):
    results = []
    for phoneme in phonemes:
        if not has_numbers(phoneme):
            results.append(phoneme)
    return results


def extract_rhyme(phonemes):
    result = ''
    for neme in reversed(phonemes):
        if is_stress(neme):
            return remove_numbers(neme) + result
        result = remove_numbers(neme) + result
    pass


def extract_slight_rhyme(phonemes):
    result = ''
    for neme in reversed(phonemes):
        if has_numbers(neme):
            return remove_numbers(neme) + result
        result = remove_numbers(neme) + result
    pass


def vowel_string(phonemes):
    results = ''
    for vowel in extract_vowels(phonemes):
        results += vowel
    return results


def extract_consonant_voicing(phonemes):
    lst = map(get_voicing, phonemes)
    result = ''
    for num in lst:
        result += str(num)
    return result


def extract_syllable_count(phonemes):
    result = len(extract_vowels(phonemes))
    return result


def extract_stress_pattern(phonemes):
    result = ''
    for phoneme in phonemes:
        if has_numbers(phoneme):
            result += str(extract_number(phoneme))
    return result

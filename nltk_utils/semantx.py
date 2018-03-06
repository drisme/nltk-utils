#!/usr/bin/env python3
# -*- coding: utf-8 -*-'
"""
Utilities for extracting lemmas from WordNet objects
"""

from nltk.corpus.reader import wordnet as wn

__author__ = 'drisme'

fncs = ['hyponyms', 'hypernyms', 'lemma_names', 'root_hypernyms',
        'member_holonyms', 'substance_holonyms', 'member_meronyms',
        'substance_meronyms', 'part_meronyms', 'topic_domains',
        'region_domains', 'usage_domains', 'attributes',
        'entailments', 'causes', 'also_sees', 'verb_groups',
        'similar_tos']


def merge_dicts(x, y):
    """
    Given two dicts, merge them into a new dict as a shallow copy.
    """
    # python 3.5 provides a more elegant way of doing this,
    # but at the cost of backwards compatibility
    z = x.copy()
    z.update(y)
    return z


def lemma_names(obj):
    # if list given, recursively call this function on each list element
    if isinstance(obj, list):
        return {ln for l in obj for ln in lemma_names(l)}
    # base case - call lemma_names of WordNetObject
    if isinstance(obj, wn._WordNetObject):
        return (ln for ln in obj.lemma_names())
    raise TypeError("Object of invalid iype given: " +
                    "Must be WordNetObject or list of WNO")


def extract_lemma_names(synset_list, func=None):
    if func is None:
        return lemma_names(synset_list)
    else:
        result = [ln for synset in synset_list
                  for func_ss in getattr(synset, func)()
                  for ln in func_ss.lemma_names()]
        if len(result) == 0:
            return []
        else:
            if isinstance(result[0], wn._WordNetObject):
                return [ln for ss in result for ln in ss.lemma_names()]
            else:
                return result


def extract_and_join_function(ss_lst, func=None):
    if func is None:
        return [ln for ss in ss_lst for ln in ss.lemma_names()]
    else:
        return [func_ss for ss in ss_lst for func_ss in getattr(ss, func)()]


def finalize_dct(d):
    return map(list, d.values())

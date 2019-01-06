import json
from typing import List

import numpy as np
import pandas as pd
import spacy
from spacy.matcher import PhraseMatcher

from input_providers import Speech, Terminal, Provider


class Context(object):
    def __init__(self, gen=0, user_symptoms: List[str] = [], possible_diseases: List[str] = [],
                 possible_add_symptoms: List[str] = []):
        self.gen = gen
        self.user_symptoms = user_symptoms
        self.possible_diseases = possible_diseases
        self.possible_add_symptoms = possible_add_symptoms
        self.error = None

    def set_error(self, error: str):
        self.error = error

    def __repr__(self):
        return {
            'gen': self.gen,
            'user described symptoms': self.user_symptoms,
            'possible diseases': self.possible_diseases,
            'possible additional symptoms': self.possible_add_symptoms
        }

    def __str__(self):
        return json.dumps(self.__repr__(), indent=2)


def create_sym_matcher():
    print("creating sym matcher")
    sym_series = sym['symptom']
    sym_list = sym_series.tolist()
    print("sym list:", sym_list)
    matcher = PhraseMatcher(nlp.vocab)

    for sym_phrase in sym_list:
        if sym_phrase != '':
            matcher.add('Symptoms', None, nlp(sym_phrase))


def get_user_syms(user_input) -> List[str]:
    user_syms = []
    doc = nlp(user_input)
    matches = sym_matcher(doc)

    for match_id, start, end in matches:
        rule_id = nlp.vocab.strings[match_id]
        span = doc[start: end]
        user_syms.append(span.text)

    return user_syms


def process_input(user_input: str, context: Context) -> Context:
    print('processing user input:', user_input)

    user_syms = get_user_syms(user_input)

    if len(user_syms) > 0:
        all_user_syms = context.user_symptoms + user_syms
        possible_diseases = []
        all_diseases_syms = set()

        for disease in dia['diagnose']:
            disease_syms = sym_dia_joined_table.loc[sym_dia_joined_table['diagnose'] == disease]['symptom'].unique()

            if set(all_user_syms).issubset(set(disease_syms)):
                possible_diseases.append(disease)
                for entry in disease_syms:
                    all_diseases_syms.add(entry)

        possible_additional_sym_list = [entry for entry in all_diseases_syms if
                                        entry not in all_user_syms]

        new_context = Context(context.gen + 1, all_user_syms,
                              possible_diseases, possible_additional_sym_list)

        return new_context
    else:
        context.set_error("no recognized symptoms in user input")

    return context


def create_metcher():
    print("creating symptoms matcher")
    sym_series = sym['symptom']
    sym_list = sym_series.tolist()
    print("sym list:", sym_list)
    matcher = PhraseMatcher(nlp.vocab)

    for sym_phrase in sym_list:
        if sym_phrase != '':
            matcher.add('Symptoms', None, nlp(sym_phrase))

    return matcher


def get_input_provider() -> Provider:
    input_method = input("would you like to use speech base input(y/<eny-key>\n")

    if input_method == 'y':
        input_provider = Speech()
    else:
        input_provider = Terminal()

    return input_provider


def diagnose(input_provider: Provider):
    context = Context()
    user_input = input_provider.get("Hi there, How are you feeling today?\n")

    while user_input is not None:
        new_context = process_input(user_input, context)

        if new_context.gen == context.gen:
            # something went wrong
            print(context.error)
        else:
            context = new_context
            print("you have specified the following symptoms:", context.user_symptoms)
            print("other related symptoms are:", context.possible_add_symptoms)

        if len(context.possible_diseases) > 1:
            user_input = input_provider.get("are you experiencing additional symptoms from the above?\n")

            if user_input == 'no':
                user_input = None
        else:
            user_input = None

    if len(context.possible_diseases) > 0:
        print('\nhealth condition diagnosis finished\n')
        print("possible condition(s) you might suffer from:", context.possible_diseases)
    else:
        print("possible health condition is not diagnosed. sorry.")

    print("bye for now. i am glad to be of help")


nlp = spacy.load('en_core_web_sm')

# load data sources
dia = pd.read_csv('sdsort/dia_t.csv')
sym = pd.read_csv('sdsort/sym_t.csv')
sym = sym.replace(np.nan, '', regex=True)
sym_dia = pd.read_csv('sdsort/diffsydiw.csv')

sym_dia_joined_table = sym.join(sym_dia.set_index('syd'), on='syd', how='inner') \
    .join(dia.set_index('did'), on='did', how='inner')

sym_matcher = create_metcher()

diagnose(get_input_provider())

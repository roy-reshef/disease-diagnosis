import json
from typing import List

from input_providers import Provider


class Context(object):
    def __init__(self, nlp, diagnosis_ds, symptoms_ds, dia_sym_ds, sym_matcher, user_symptoms: List[str] = [],
                 possible_diseases: List[str] = [],
                 possible_add_symptoms: List[str] = []):
        self.nlp = nlp
        self.diagnosis_ds = diagnosis_ds
        self.symptoms_ds = symptoms_ds
        self.dia_sym_ds = dia_sym_ds
        self.sym_matcher = sym_matcher

        self.user_symptoms = user_symptoms
        self.possible_diseases = possible_diseases
        self.possible_add_symptoms = possible_add_symptoms
        self.error = None
        self.input_provider = None
        self.in_conversation = True

    def set_input_provider(self, input_provider: Provider):
        self.input_provider = input_provider

    def set_error(self, error):
        self.error = error

    def set_is_in_conversation(self, val: bool):
        self.in_conversation = val

    def __repr__(self):
        return {
            'error': self.error,
            'user described symptoms': self.user_symptoms,
            'possible diseases': self.possible_diseases,
            'possible additional symptoms': self.possible_add_symptoms
        }

    def __str__(self):
        return json.dumps(self.__repr__(), indent=2)

import numpy as np
import pandas as pd
import spacy
from spacy.matcher import PhraseMatcher

from actions.actions import Action, AdditionalSymptomsAction, GreetingAction
from actions.handlers import GreetingHandler, AdditionalSymptomsHandler
from context import Context
from input_providers import Speech, Terminal, Provider
from intents.intent_req_handlers import UserInputReqHandler, TerminateReqHandler
from intents.intent_reqs import IntentReq, UserInputIntentReq, TerminateIntentReq
from intents.intents import UserInputIntent, Intent


def process_intent(intent: Intent) -> Action:
    print('processing intent:', intent)
    ctx: Context = intent.ctx

    if type(intent) == UserInputIntent:
        action = AdditionalSymptomsAction(intent, ctx)
    else:
        raise Exception("unsupported intent type:", type(intent))

    return action


def create_metcher(nlp, symptoms_ds):
    print("creating symptoms matcher")
    sym_series = symptoms_ds['symptom']
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


def handle_action(action: Action) -> IntentReq:
    if type(action) == GreetingAction:
        intent_req = GreetingHandler().handle(action)
    elif type(action) == AdditionalSymptomsAction:
        intent_req = AdditionalSymptomsHandler().handle(action)
    else:
        raise Exception("no action handler was found for")

    return intent_req


def handle_intent_req(req: IntentReq) -> Intent:
    if type(req) == UserInputIntentReq:
        intent = UserInputReqHandler().handle(req)
    elif type(req) == TerminateIntentReq:
        intent = TerminateReqHandler().handle(req)
    else:
        raise Exception("no action handler was found for")

    return intent


def diagnose(context: Context):
    intent_req = handle_action(GreetingAction(ctx))
    intent = handle_intent_req(intent_req)

    while intent.ctx.in_conversation:
        if intent.ctx.error is not None:
            print("error - ", intent.ctx.error)
            intent.ctx.set_error(None)

        action: Action = process_intent(intent)
        intent = handle_intent_req(handle_action(action))

    if len(context.possible_diseases) > 0:
        print('\nhealth condition diagnosis finished\n')
        print("possible condition(s) you might suffer from:", context.possible_diseases)
    else:
        print("possible health condition is not diagnosed. sorry.")

    print("bye for now. i am glad to be of help")


def init() -> Context:
    nlp = spacy.load('en_core_web_sm')
    # load data sources
    diagnosis_ds = pd.read_csv('sdsort/dia_t.csv')
    symptoms_ds = pd.read_csv('sdsort/sym_t.csv')
    symptoms_ds = symptoms_ds.replace(np.nan, '', regex=True)
    sym_dia_join_table = pd.read_csv('sdsort/diffsydiw.csv')

    sym_dia_ds = symptoms_ds.join(sym_dia_join_table.set_index('syd'), on='syd', how='inner') \
        .join(diagnosis_ds.set_index('did'), on='did', how='inner')

    sym_matcher = create_metcher(nlp, symptoms_ds)

    return Context(nlp, diagnosis_ds, symptoms_ds, sym_dia_ds, sym_matcher)


if __name__ == '__main__':
    ctx = init()
    ctx.set_input_provider(get_input_provider())
    diagnose(ctx)

from abc import abstractmethod

import utils
from actions.actions import Action, AdditionalSymptomsAction, GreetingAction, ShowSymsAction
from intents.intent_reqs import IntentReq, TerminateIntentReq, UserInputIntentReq
from intents.intents import UserInputIntent


class ActionHandler(object):
    @abstractmethod
    def handle(self, action: Action) -> IntentReq:
        pass


class GreetingHandler(ActionHandler):
    def handle(self, action: GreetingAction) -> IntentReq:
        print("Hi there, How are you feeling today?")
        return UserInputIntentReq(action.ctx)


class ShowSymsHandler(ActionHandler):
    def handle(self, action: ShowSymsAction) -> IntentReq:
        print("here is the complete symptoms list\n", action.ctx.symptoms_ds['symptom'].tolist())
        return UserInputIntentReq(action.ctx)


class HelpHandler(ActionHandler):
    def handle(self, action: ShowSymsAction) -> IntentReq:
        print("HELP:\n", "* show symptoms - lists all known symptoms\n", \
              "* bye/quit/exit - terminates conversation")
        return UserInputIntentReq(action.ctx)


class TerminateHandler(ActionHandler):
    def handle(self, action: ShowSymsAction) -> IntentReq:
        utils.end_session(action.ctx)

        return TerminateIntentReq(action.ctx)


class AdditionalSymptomsHandler(ActionHandler):
    def handle(self, action: AdditionalSymptomsAction) -> IntentReq:
        ctx = action.ctx
        user_input_intent: UserInputIntent = action.triggering_intent
        user_syms = utils.get_user_syms(user_input_intent.user_input, ctx)

        if len(user_syms) > 0:
            all_user_syms = user_input_intent.ctx.user_symptoms + user_syms
            possible_diseases = []
            all_diseases_syms = set()

            for disease in ctx.diagnosis_ds['diagnose']:
                disease_syms = ctx.dia_sym_ds.loc[ctx.dia_sym_ds['diagnose'] == disease]['symptom'].unique()

                if set(all_user_syms).issubset(set(disease_syms)):
                    possible_diseases.append(disease)
                    for entry in disease_syms:
                        all_diseases_syms.add(entry)

            possible_additional_sym_list = [entry for entry in all_diseases_syms if
                                            entry not in all_user_syms]

            ctx.user_symptoms = all_user_syms
            ctx.possible_diseases = possible_diseases
            ctx.possible_add_symptoms = possible_additional_sym_list

            if len(ctx.possible_diseases) == 1:
                return TerminateIntentReq(ctx)
            else:
                if ctx.user_symptoms:
                    print("you have specified the following symptoms:", ctx.user_symptoms)

                if ctx.possible_diseases:
                    print("Possible causes:", ctx.possible_diseases)
                if ctx.possible_add_symptoms:
                    print("other possible related symptoms are:", ctx.possible_add_symptoms)
                    print("are you experiencing additional symptoms from the above?")
                return UserInputIntentReq(ctx)
        else:
            print("symptoms not recognized!")
            ctx.set_error("no recognized symptoms in user input")
            return UserInputIntentReq(ctx)

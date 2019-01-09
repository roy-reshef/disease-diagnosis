from abc import abstractmethod

import utils
from intents.intent_reqs import IntentReq, UserInputIntentReq, TerminateIntentReq
from intents.intents import Intent, UserInputIntent, NoIntent


class IntentReqHandler(object):
    @abstractmethod
    def handle(self, intent_req: IntentReq) -> Intent:
        pass


class UserInputReqHandler(IntentReqHandler):
    def handle(self, intent_req: UserInputIntentReq) -> Intent:
        user_input = intent_req.ctx.input_provider.get("What symptoms do you have?\n")

        if user_input is None:
            print("no information provided")
            ctx = intent_req.ctx
            ctx.set_is_in_conversation(False)
            return NoIntent(ctx)
        else:
            return UserInputIntent(intent_req.ctx, user_input)


class TerminateReqHandler(IntentReqHandler):
    def handle(self, intent_req: TerminateIntentReq) -> Intent:
        ctx = intent_req.ctx
        ctx.set_is_in_conversation(False)

        utils.end_session(intent_req.ctx)
        return NoIntent(ctx)
